from backend.core.logger import (
    get_logger
)
from backend.core.security import (
    decode_access_token
)
from backend.database import (
    get_connection
)
from backend.services.audit_service import (
    AuditService
)


logger = get_logger(
    "audit"
)


WRITE_METHODS = {
    "POST",
    "PUT",
    "PATCH",
    "DELETE"
}


class AuditLoggingMiddleware:

    def __init__(
        self,
        app
    ):
        self.app = app


    async def __call__(
        self,
        scope,
        receive,
        send
    ):
        if scope["type"] != "http":
            await self.app(
                scope,
                receive,
                send
            )

            return


        method = (
            scope.get(
                "method",
                ""
            )
            .upper()
        )

        path = scope.get(
            "path",
            ""
        )


        # Authentication events are stored separately
        # in HISTORIAL_ACCESOS.
        should_skip_path = (
            path.startswith("/auth/")
        )


        response_status = 500


        async def send_wrapper(
            message
        ):
            nonlocal response_status

            if (
                message["type"]
                == "http.response.start"
            ):
                response_status = (
                    message["status"]
                )

            await send(
                message
            )


        try:
            await self.app(
                scope,
                receive,
                send_wrapper
            )

        finally:
            should_audit = (
                not should_skip_path
                and (
                    method in WRITE_METHODS
                    or response_status in (
                        401,
                        403
                    )
                )
            )

            if should_audit:
                self._write_audit(
                    scope=scope,
                    method=method,
                    path=path,
                    status_code=response_status
                )


    def _write_audit(
        self,
        scope,
        method: str,
        path: str,
        status_code: int
    ):
        connection = None

        try:
            usuario_id = (
                self._extract_user_id(
                    scope
                )
            )

            ip_origen = (
                self._extract_client_ip(
                    scope
                )
            )

            request_id = (
                self._extract_request_id(
                    scope
                )
            )

            connection = (
                get_connection()
            )

            audit_service = (
                AuditService(
                    connection
                )
            )

            audit_service.record_request(
                method=method,
                path=path,
                status_code=status_code,
                usuario_id=usuario_id,
                ip_origen=ip_origen,
                request_id=request_id
            )

            connection.commit()

        except Exception as error:
            if connection is not None:
                connection.rollback()

            logger.exception(
                "No se pudo registrar "
                "la auditoría automática: %s",
                str(error)
            )

        finally:
            if connection is not None:
                connection.close()


    @staticmethod
    def _extract_user_id(
        scope
    ):
        headers = {
            key.decode(
                "latin-1"
            ).lower():
            value.decode(
                "latin-1"
            )

            for key, value
            in scope.get(
                "headers",
                []
            )
        }

        authorization = headers.get(
            "authorization",
            ""
        )

        if not authorization.lower().startswith(
            "bearer "
        ):
            return None

        token = authorization[
            7:
        ].strip()

        if not token:
            return None

        try:
            payload = decode_access_token(
                token
            )

            subject = payload.get(
                "sub"
            )

            if subject is None:
                return None

            return int(
                subject
            )

        except Exception:
            return None


    @staticmethod
    def _extract_client_ip(
        scope
    ):
        headers = {
            key.decode(
                "latin-1"
            ).lower():
            value.decode(
                "latin-1"
            )

            for key, value
            in scope.get(
                "headers",
                []
            )
        }

        forwarded_for = headers.get(
            "x-forwarded-for"
        )

        if forwarded_for:
            return (
                forwarded_for
                .split(",")[0]
                .strip()
            )

        client = scope.get(
            "client"
        )

        if client:
            return client[0]

        return None


    @staticmethod
    def _extract_request_id(
        scope
    ):
        state = scope.get(
            "state",
            {}
        )

        if isinstance(
            state,
            dict
        ):
            return state.get(
                "request_id"
            )

        return getattr(
            state,
            "request_id",
            None
        )