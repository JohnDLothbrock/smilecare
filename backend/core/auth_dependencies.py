from collections.abc import Callable

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from jwt import (
    ExpiredSignatureError,
    InvalidTokenError
)

from backend.core.security import (
    decode_access_token
)
from backend.database import get_db
from backend.services.auth_service import (
    AuthService
)


bearer_scheme = HTTPBearer(
    auto_error=False
)


SAFE_HTTP_METHODS = {
    "GET",
    "HEAD",
    "OPTIONS"
}


def get_current_user(
    credentials: (
        HTTPAuthorizationCredentials
        | None
    ) = Depends(bearer_scheme),
    connection=Depends(get_db)
):
    if credentials is None:
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Debe iniciar sesión para "
                "acceder a este recurso."
            ),
            headers={
                "WWW-Authenticate":
                    "Bearer"
            }
        )

    try:
        payload = decode_access_token(
            credentials.credentials
        )

        subject = payload.get(
            "sub"
        )

        if subject is None:
            raise InvalidTokenError()

        usuario_id = int(
            subject
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "La sesión ha expirado. "
                "Inicie sesión nuevamente."
            ),
            headers={
                "WWW-Authenticate":
                    "Bearer"
            }
        )

    except (
        InvalidTokenError,
        ValueError,
        TypeError
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Token de autenticación inválido."
            ),
            headers={
                "WWW-Authenticate":
                    "Bearer"
            }
        )

    auth_service = AuthService(
        connection
    )

    return auth_service.get_current_user(
        usuario_id
    )


def user_has_any_permission(
    current_user: dict,
    permission_codes
) -> bool:
    user_permissions = set(
        current_user.get(
            "permisos",
            []
        )
    )

    required_permissions = set(
        permission_codes
    )

    return bool(
        user_permissions.intersection(
            required_permissions
        )
    )


def raise_forbidden():
    raise HTTPException(
        status_code=(
            status.HTTP_403_FORBIDDEN
        ),
        detail=(
            "No tiene permiso para "
            "realizar esta acción."
        )
    )


def require_permission(
    permission_code: str
) -> Callable:

    def permission_dependency(
        current_user=Depends(
            get_current_user
        )
    ):
        if not user_has_any_permission(
            current_user,
            [permission_code]
        ):
            raise_forbidden()

        return current_user

    return permission_dependency


def require_any_permission(
    *permission_codes: str
) -> Callable:

    if not permission_codes:
        raise ValueError(
            "Debe indicar al menos un permiso."
        )

    def permission_dependency(
        current_user=Depends(
            get_current_user
        )
    ):
        if not user_has_any_permission(
            current_user,
            permission_codes
        ):
            raise_forbidden()

        return current_user

    return permission_dependency


def require_method_permissions(
    read_permissions,
    write_permissions=None
) -> Callable:

    read_permissions = tuple(
        read_permissions
    )

    if write_permissions is None:
        write_permissions = (
            read_permissions
        )

    write_permissions = tuple(
        write_permissions
    )

    if not read_permissions:
        raise ValueError(
            "Debe indicar al menos un permiso "
            "de lectura."
        )

    if not write_permissions:
        raise ValueError(
            "Debe indicar al menos un permiso "
            "de escritura."
        )

    def permission_dependency(
        request: Request,
        current_user=Depends(
            get_current_user
        )
    ):
        method = request.method.upper()

        if method in SAFE_HTTP_METHODS:
            required_permissions = (
                read_permissions
            )
        else:
            required_permissions = (
                write_permissions
            )

        if not user_has_any_permission(
            current_user,
            required_permissions
        ):
            raise_forbidden()

        return current_user

    return permission_dependency