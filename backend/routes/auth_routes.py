from fastapi import (
    APIRouter,
    Depends,
    Request
)
from pydantic import (
    BaseModel,
    Field
)

from backend.core.auth_dependencies import (
    get_current_user
)
from backend.database import get_db
from backend.services.auth_service import (
    AuthService
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


class LoginRequest(BaseModel):
    nombre_usuario: str = Field(
        min_length=1,
        max_length=50
    )

    password: str = Field(
        min_length=1,
        max_length=128
    )


class ForgotPasswordRequest(BaseModel):
    identificador: str = Field(
        min_length=1,
        max_length=150
    )


class ResetPasswordRequest(BaseModel):
    token: str = Field(
        min_length=20,
        max_length=500
    )

    new_password: str = Field(
        min_length=8,
        max_length=128
    )


def get_request_context(
    request: Request
):
    forwarded_for = (
        request.headers.get(
            "x-forwarded-for"
        )
    )

    if forwarded_for:
        ip_origen = (
            forwarded_for
            .split(",")[0]
            .strip()
        )

    elif request.client is not None:
        ip_origen = (
            request.client.host
        )

    else:
        ip_origen = None

    user_agent = (
        request.headers.get(
            "user-agent"
        )
    )

    request_id = getattr(
        request.state,
        "request_id",
        None
    )

    return {
        "ip_origen":
            ip_origen,

        "user_agent":
            user_agent,

        "request_id":
            request_id
    }


@router.post("/login")
def login(
    login_data: LoginRequest,
    request: Request,
    connection=Depends(get_db)
):
    auth_service = AuthService(
        connection
    )

    request_context = (
        get_request_context(
            request
        )
    )

    return auth_service.login(
        login_data.nombre_usuario,
        login_data.password,
        **request_context
    )


@router.post("/logout")
def logout(
    request: Request,
    current_user=Depends(
        get_current_user
    ),
    connection=Depends(get_db)
):
    auth_service = AuthService(
        connection
    )

    request_context = (
        get_request_context(
            request
        )
    )

    return auth_service.logout(
        current_user,
        **request_context
    )


@router.post("/forgot-password")
def forgot_password(
    reset_request: ForgotPasswordRequest,
    request: Request,
    connection=Depends(get_db)
):
    auth_service = AuthService(
        connection
    )

    request_context = (
        get_request_context(
            request
        )
    )

    return auth_service.request_password_reset(
        reset_request.identificador,
        **request_context
    )


@router.post("/reset-password")
def reset_password(
    reset_request: ResetPasswordRequest,
    request: Request,
    connection=Depends(get_db)
):
    auth_service = AuthService(
        connection
    )

    request_context = (
        get_request_context(
            request
        )
    )

    return auth_service.reset_password(
        token=reset_request.token,
        new_password=(
            reset_request.new_password
        ),
        **request_context
    )


@router.get("/me")
def get_authenticated_user(
    current_user=Depends(
        get_current_user
    )
):
    return current_user