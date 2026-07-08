import os

from fastapi import (
    HTTPException,
    status
)

from backend.core.logger import (
    get_logger
)
from backend.core.security import (
    create_access_token,
    generate_password_reset_token,
    hash_password,
    hash_password_reset_token,
    is_modern_password_hash,
    verify_hashed_password,
    verify_legacy_password
)
from backend.repositories.auth_repository import (
    AuthRepository
)
from backend.services.audit_service import (
    AuditService
)
from backend.services.outlook_mail_service import (
    OutlookMailService
)


logger = get_logger(
    "auth"
)


PASSWORD_RESET_EXPIRE_MINUTES = int(
    os.getenv(
        "PASSWORD_RESET_EXPIRE_MINUTES",
        "30"
    )
)


class AuthService:

    def __init__(
        self,
        connection
    ):
        self.connection = connection

        self.auth_repository = (
            AuthRepository(
                connection
            )
        )

        self.audit_service = (
            AuditService(
                connection
            )
        )

    # -----------------------------------------------------
    # ERRORS
    # -----------------------------------------------------

    def raise_invalid_credentials(
        self
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Nombre de usuario o "
                "contraseña incorrectos."
            ),
            headers={
                "WWW-Authenticate":
                    "Bearer"
            }
        )

    # -----------------------------------------------------
    # ACCOUNT STATUS
    # -----------------------------------------------------

    def validate_account_status(
        self,
        user: dict
    ):
        if (
            str(
                user["usuario_estado"]
            ).upper()
            != "ACTIVO"
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
                detail=(
                    "La cuenta de usuario "
                    "no está activa."
                )
            )

        if (
            str(
                user["rol_estado"]
            ).upper()
            != "ACTIVO"
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
                detail=(
                    "El rol asignado a la "
                    "cuenta no está activo."
                )
            )

    # -----------------------------------------------------
    # SESSION USER
    # -----------------------------------------------------

    def build_session_user(
        self,
        user: dict
    ) -> dict:
        permissions = (
            self.auth_repository
            .get_permissions_by_role(
                user["rol_id"]
            )
        )

        return {
            "usuario_id":
                user["usuario_id"],

            "rol_id":
                user["rol_id"],

            "nombre_rol":
                user["nombre_rol"],

            "nombre_usuario":
                user["nombre_usuario"],

            "estado":
                user["usuario_estado"],

            "permisos":
                permissions
        }

    # -----------------------------------------------------
    # PASSWORD VERIFICATION
    # -----------------------------------------------------

    @staticmethod
    def verify_password(
        user: dict,
        password: str
    ):
        stored_password = str(
            user["password_hash"]
        )

        if is_modern_password_hash(
            stored_password
        ):
            return (
                verify_hashed_password(
                    password,
                    stored_password
                )
            )

        return verify_legacy_password(
            password,
            stored_password
        )

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    def login(
        self,
        nombre_usuario: str,
        password: str,
        ip_origen=None,
        user_agent=None,
        request_id=None
    ) -> dict:
        normalized_username = (
            nombre_usuario.strip()
        )

        try:
            user = (
                self.auth_repository
                .get_user_by_username(
                    normalized_username
                )
            )

            if user is None:
                self.audit_service.record_access_event(
                    evento="LOGIN_FAILED",
                    resultado="FALLIDO",
                    nombre_usuario=(
                        normalized_username
                    ),
                    detalle=(
                        "Credenciales incorrectas."
                    ),
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                    request_id=request_id
                )

                self.connection.commit()

                self.raise_invalid_credentials()

            try:
                self.validate_account_status(
                    user
                )

            except HTTPException as error:
                self.audit_service.record_access_event(
                    evento="LOGIN_FAILED",
                    resultado="DENEGADO",
                    usuario_id=(
                        user["usuario_id"]
                    ),
                    nombre_usuario=(
                        user["nombre_usuario"]
                    ),
                    nombre_rol=(
                        user["nombre_rol"]
                    ),
                    detalle=error.detail,
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                    request_id=request_id
                )

                self.connection.commit()

                raise

            if not self.verify_password(
                user,
                password
            ):
                self.audit_service.record_access_event(
                    evento="LOGIN_FAILED",
                    resultado="FALLIDO",
                    usuario_id=(
                        user["usuario_id"]
                    ),
                    nombre_usuario=(
                        user["nombre_usuario"]
                    ),
                    nombre_rol=(
                        user["nombre_rol"]
                    ),
                    detalle=(
                        "Credenciales incorrectas."
                    ),
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                    request_id=request_id
                )

                self.connection.commit()

                self.raise_invalid_credentials()

            stored_password = str(
                user["password_hash"]
            )

            if not is_modern_password_hash(
                stored_password
            ):
                new_password_hash = (
                    hash_password(
                        password
                    )
                )

                self.auth_repository.update_password_hash(
                    user["usuario_id"],
                    new_password_hash
                )

            session_user = (
                self.build_session_user(
                    user
                )
            )

            access_token = (
                create_access_token(
                    subject=str(
                        session_user[
                            "usuario_id"
                        ]
                    ),
                    additional_claims={
                        "username":
                            session_user[
                                "nombre_usuario"
                            ]
                    }
                )
            )

            self.audit_service.record_access_event(
                evento="LOGIN_SUCCESS",
                resultado="EXITOSO",
                usuario_id=(
                    session_user[
                        "usuario_id"
                    ]
                ),
                nombre_usuario=(
                    session_user[
                        "nombre_usuario"
                    ]
                ),
                nombre_rol=(
                    session_user[
                        "nombre_rol"
                    ]
                ),
                detalle=(
                    "Inicio de sesión correcto."
                ),
                ip_origen=ip_origen,
                user_agent=user_agent,
                request_id=request_id
            )

            self.connection.commit()

            return {
                "access_token":
                    access_token,

                "token_type":
                    "bearer",

                "user":
                    session_user
            }

        except HTTPException:
            raise

        except Exception:
            self.connection.rollback()
            raise

    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    def logout(
        self,
        current_user: dict,
        ip_origen=None,
        user_agent=None,
        request_id=None
    ):
        try:
            self.audit_service.record_access_event(
                evento="LOGOUT",
                resultado="EXITOSO",
                usuario_id=(
                    current_user[
                        "usuario_id"
                    ]
                ),
                nombre_usuario=(
                    current_user[
                        "nombre_usuario"
                    ]
                ),
                nombre_rol=(
                    current_user[
                        "nombre_rol"
                    ]
                ),
                detalle=(
                    "Cierre de sesión registrado."
                ),
                ip_origen=ip_origen,
                user_agent=user_agent,
                request_id=request_id
            )

            self.connection.commit()

            return {
                "message":
                    "Sesión cerrada correctamente."
            }

        except Exception:
            self.connection.rollback()
            raise

    # -----------------------------------------------------
    # FORGOT PASSWORD
    # -----------------------------------------------------

    def request_password_reset(
        self,
        identifier: str,
        ip_origen=None,
        user_agent=None,
        request_id=None
    ) -> dict:
        neutral_response = {
            "message": (
                "Si la cuenta existe y tiene un correo "
                "de recuperación configurado, recibirá "
                "un enlace para restablecer la contraseña."
            )
        }

        normalized_identifier = (
            identifier.strip()
        )

        try:
            user = (
                self.auth_repository
                .get_user_by_identifier(
                    normalized_identifier
                )
            )

            if user is None:
                self.audit_service.record_access_event(
                    evento=(
                        "PASSWORD_RESET_REQUESTED"
                    ),
                    resultado="FALLIDO",
                    nombre_usuario=(
                        normalized_identifier
                    ),
                    detalle=(
                        "Solicitud para una cuenta "
                        "no identificada."
                    ),
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                    request_id=request_id
                )

                self.connection.commit()

                return neutral_response

            try:
                self.validate_account_status(
                    user
                )

            except HTTPException as error:
                self.audit_service.record_access_event(
                    evento=(
                        "PASSWORD_RESET_REQUESTED"
                    ),
                    resultado="DENEGADO",
                    usuario_id=(
                        user["usuario_id"]
                    ),
                    nombre_usuario=(
                        user["nombre_usuario"]
                    ),
                    nombre_rol=(
                        user["nombre_rol"]
                    ),
                    detalle=error.detail,
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                    request_id=request_id
                )

                self.connection.commit()

                return neutral_response

            correo = user.get(
                "correo"
            )

            if not correo:
                self.audit_service.record_access_event(
                    evento=(
                        "PASSWORD_RESET_REQUESTED"
                    ),
                    resultado="FALLIDO",
                    usuario_id=(
                        user["usuario_id"]
                    ),
                    nombre_usuario=(
                        user["nombre_usuario"]
                    ),
                    nombre_rol=(
                        user["nombre_rol"]
                    ),
                    detalle=(
                        "La cuenta no tiene un correo "
                        "de recuperación configurado."
                    ),
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                    request_id=request_id
                )

                self.connection.commit()

                return neutral_response

            reset_token = (
                generate_password_reset_token()
            )

            token_hash = (
                hash_password_reset_token(
                    reset_token
                )
            )

            self.auth_repository.invalidate_unused_reset_tokens(
                user["usuario_id"]
            )

            self.auth_repository.create_password_reset_token(
                usuario_id=(
                    user["usuario_id"]
                ),
                token_hash=token_hash,
                expire_minutes=(
                    PASSWORD_RESET_EXPIRE_MINUTES
                ),
                solicitud_ip=ip_origen,
                request_id=request_id
            )

            self.connection.commit()

            try:
                mail_service = (
                    OutlookMailService()
                )

                mail_service.send_password_reset_email(
                    to_email=str(correo),
                    username=(
                        user["nombre_usuario"]
                    ),
                    reset_token=reset_token,
                    expire_minutes=(
                        PASSWORD_RESET_EXPIRE_MINUTES
                    )
                )

            except Exception as error:
                logger.exception(
                    "No se pudo enviar el correo "
                    "de recuperación: %s",
                    str(error)
                )

                self.auth_repository.invalidate_unused_reset_tokens(
                    user["usuario_id"]
                )

                self.audit_service.record_access_event(
                    evento=(
                        "PASSWORD_RESET_REQUESTED"
                    ),
                    resultado="FALLIDO",
                    usuario_id=(
                        user["usuario_id"]
                    ),
                    nombre_usuario=(
                        user["nombre_usuario"]
                    ),
                    nombre_rol=(
                        user["nombre_rol"]
                    ),
                    detalle=(
                        "No se pudo enviar el correo "
                        "de recuperación."
                    ),
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                    request_id=request_id
                )

                self.connection.commit()

                return neutral_response

            self.audit_service.record_access_event(
                evento=(
                    "PASSWORD_RESET_REQUESTED"
                ),
                resultado="EXITOSO",
                usuario_id=(
                    user["usuario_id"]
                ),
                nombre_usuario=(
                    user["nombre_usuario"]
                ),
                nombre_rol=(
                    user["nombre_rol"]
                ),
                detalle=(
                    "Se envió un enlace de "
                    "recuperación al correo configurado."
                ),
                ip_origen=ip_origen,
                user_agent=user_agent,
                request_id=request_id
            )

            self.connection.commit()

            return neutral_response

        except Exception:
            self.connection.rollback()
            raise

    # -----------------------------------------------------
    # RESET PASSWORD
    # -----------------------------------------------------

    def reset_password(
        self,
        token: str,
        new_password: str,
        ip_origen=None,
        user_agent=None,
        request_id=None
    ) -> dict:
        token_hash = (
            hash_password_reset_token(
                token
            )
        )

        try:
            reset_data = (
                self.auth_repository
                .get_valid_password_reset_token(
                    token_hash
                )
            )

            if reset_data is None:
                self.audit_service.record_access_event(
                    evento=(
                        "PASSWORD_RESET_FAILED"
                    ),
                    resultado="FALLIDO",
                    detalle=(
                        "Se intentó utilizar un enlace "
                        "inválido, vencido o ya utilizado."
                    ),
                    ip_origen=ip_origen,
                    user_agent=user_agent,
                    request_id=request_id
                )

                self.connection.commit()

                raise HTTPException(
                    status_code=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                    detail=(
                        "El enlace de recuperación es "
                        "inválido, venció o ya fue utilizado."
                    )
                )

            self.validate_account_status(
                reset_data
            )

            new_password_hash = (
                hash_password(
                    new_password
                )
            )

            self.auth_repository.update_password_hash(
                reset_data["usuario_id"],
                new_password_hash
            )

            self.auth_repository.mark_password_reset_token_used(
                reset_data["reset_token_id"]
            )

            self.auth_repository.invalidate_other_reset_tokens(
                usuario_id=(
                    reset_data["usuario_id"]
                ),
                reset_token_id=(
                    reset_data[
                        "reset_token_id"
                    ]
                )
            )

            self.audit_service.record_access_event(
                evento=(
                    "PASSWORD_RESET_COMPLETED"
                ),
                resultado="EXITOSO",
                usuario_id=(
                    reset_data["usuario_id"]
                ),
                nombre_usuario=(
                    reset_data["nombre_usuario"]
                ),
                nombre_rol=(
                    reset_data["nombre_rol"]
                ),
                detalle=(
                    "La contraseña fue restablecida "
                    "correctamente."
                ),
                ip_origen=ip_origen,
                user_agent=user_agent,
                request_id=request_id
            )

            self.connection.commit()

            return {
                "message": (
                    "La contraseña fue restablecida "
                    "correctamente. Ya puede iniciar sesión."
                )
            }

        except HTTPException:
            raise

        except Exception:
            self.connection.rollback()
            raise

    # -----------------------------------------------------
    # CURRENT USER
    # -----------------------------------------------------

    def get_current_user(
        self,
        usuario_id: int
    ) -> dict:
        user = (
            self.auth_repository
            .get_user_by_id(
                usuario_id
            )
        )

        if user is None:
            raise HTTPException(
                status_code=(
                    status.HTTP_401_UNAUTHORIZED
                ),
                detail=(
                    "La sesión ya no "
                    "es válida."
                ),
                headers={
                    "WWW-Authenticate":
                        "Bearer"
                }
            )

        self.validate_account_status(
            user
        )

        return self.build_session_user(
            user
        )