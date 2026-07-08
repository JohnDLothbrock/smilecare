from datetime import (
    datetime,
    time,
    timedelta
)

from fastapi import (
    HTTPException,
    status
)

from backend.repositories.audit_admin_repository import (
    AuditAdminRepository
)


class AuditAdminService:

    def __init__(
        self,
        connection
    ):
        self.connection = connection

        self.audit_repository = (
            AuditAdminRepository(
                connection
            )
        )


    # -----------------------------------------------------
    # DATE PARSING
    # -----------------------------------------------------

    @staticmethod
    def parse_date(
        value: str | None,
        field_name: str
    ):
        if not value:
            return None

        try:
            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            raise HTTPException(
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
                detail=(
                    f"{field_name} debe usar "
                    "el formato YYYY-MM-DD."
                )
            )


    def build_date_range(
        self,
        fecha_desde: str | None,
        fecha_hasta: str | None
    ):
        start_date = self.parse_date(
            fecha_desde,
            "fecha_desde"
        )

        end_date = self.parse_date(
            fecha_hasta,
            "fecha_hasta"
        )


        if (
            start_date is not None
            and end_date is not None
            and start_date > end_date
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
                detail=(
                    "La fecha inicial no puede "
                    "ser posterior a la fecha final."
                )
            )


        start_datetime = None

        if start_date is not None:
            start_datetime = datetime.combine(
                start_date,
                time.min
            )


        end_datetime_exclusive = None

        if end_date is not None:
            end_datetime_exclusive = (
                datetime.combine(
                    end_date,
                    time.min
                )
                + timedelta(days=1)
            )


        return (
            start_datetime,
            end_datetime_exclusive
        )


    # -----------------------------------------------------
    # NORMALIZATION
    # -----------------------------------------------------

    @staticmethod
    def normalize_filter(
        value: str | None
    ):
        if value is None:
            return None

        normalized = value.strip()

        return (
            normalized
            if normalized
            else None
        )


    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------

    def get_dashboard(
        self,
        fecha_desde=None,
        fecha_hasta=None,
        usuario=None,
        modulo=None,
        accion=None,
        resultado=None,
        limite: int = 500
    ):
        if limite < 1 or limite > 1000:
            raise HTTPException(
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
                detail=(
                    "El límite debe estar "
                    "entre 1 y 1000."
                )
            )


        (
            start_datetime,
            end_datetime_exclusive
        ) = self.build_date_range(
            fecha_desde,
            fecha_hasta
        )


        usuario = self.normalize_filter(
            usuario
        )

        modulo = self.normalize_filter(
            modulo
        )

        accion = self.normalize_filter(
            accion
        )

        resultado = self.normalize_filter(
            resultado
        )


        if resultado:
            allowed_results = {
                "EXITOSO",
                "FALLIDO",
                "DENEGADO"
            }

            normalized_result = (
                resultado.upper()
            )

            if (
                normalized_result
                not in allowed_results
            ):
                raise HTTPException(
                    status_code=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                    detail=(
                        "Resultado inválido."
                    )
                )

            resultado = normalized_result


        return {
            "resumen":
                self.audit_repository
                .get_summary(
                    fecha_desde=(
                        start_datetime
                    ),
                    fecha_hasta_exclusiva=(
                        end_datetime_exclusive
                    )
                ),

            "auditoria_sistema":
                self.audit_repository
                .get_system_audit(
                    fecha_desde=(
                        start_datetime
                    ),
                    fecha_hasta_exclusiva=(
                        end_datetime_exclusive
                    ),
                    usuario=usuario,
                    modulo=modulo,
                    accion=accion,
                    resultado=resultado,
                    limite=limite
                ),

            "historial_accesos":
                self.audit_repository
                .get_access_history(
                    fecha_desde=(
                        start_datetime
                    ),
                    fecha_hasta_exclusiva=(
                        end_datetime_exclusive
                    ),
                    usuario=usuario,
                    accion=accion,
                    resultado=resultado,
                    limite=limite
                ),

            "auditoria_triggers":
                self.audit_repository
                .get_trigger_audit(
                    fecha_desde=(
                        start_datetime
                    ),
                    fecha_hasta_exclusiva=(
                        end_datetime_exclusive
                    ),
                    usuario=usuario,
                    accion=accion,
                    limite=limite
                )
        }