from typing import Optional


def row_to_dict(
    cursor,
    row
) -> Optional[dict]:
    if row is None:
        return None

    columns = [
        column[0].lower()
        for column in cursor.description
    ]

    return dict(
        zip(
            columns,
            row
        )
    )


class AuthRepository:

    def __init__(
        self,
        connection
    ):
        self.connection = connection

    def get_user_by_username(
        self,
        nombre_usuario: str
    ) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    u.usuario_id,
                    u.rol_id,
                    r.nombre_rol,
                    u.nombre_usuario,
                    u.correo,
                    u.password_hash,
                    u.estado AS usuario_estado,
                    r.estado AS rol_estado
                FROM usuarios u
                INNER JOIN roles r
                    ON r.rol_id = u.rol_id
                WHERE UPPER(u.nombre_usuario)
                    = UPPER(:nombre_usuario)
                """,
                {
                    "nombre_usuario":
                        nombre_usuario
                }
            )

            row = cursor.fetchone()

            return row_to_dict(
                cursor,
                row
            )

        finally:
            cursor.close()

    def get_user_by_identifier(
        self,
        identifier: str
    ) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    u.usuario_id,
                    u.rol_id,
                    r.nombre_rol,
                    u.nombre_usuario,
                    u.correo,
                    u.password_hash,
                    u.estado AS usuario_estado,
                    r.estado AS rol_estado
                FROM usuarios u
                INNER JOIN roles r
                    ON r.rol_id = u.rol_id
                WHERE
                    UPPER(u.nombre_usuario)
                        = UPPER(:identifier)
                    OR
                    UPPER(u.correo)
                        = UPPER(:identifier)
                """,
                {
                    "identifier":
                        identifier
                }
            )

            row = cursor.fetchone()

            return row_to_dict(
                cursor,
                row
            )

        finally:
            cursor.close()

    def get_user_by_id(
        self,
        usuario_id: int
    ) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    u.usuario_id,
                    u.rol_id,
                    r.nombre_rol,
                    u.nombre_usuario,
                    u.correo,
                    u.password_hash,
                    u.estado AS usuario_estado,
                    r.estado AS rol_estado
                FROM usuarios u
                INNER JOIN roles r
                    ON r.rol_id = u.rol_id
                WHERE u.usuario_id = :usuario_id
                """,
                {
                    "usuario_id":
                        usuario_id
                }
            )

            row = cursor.fetchone()

            return row_to_dict(
                cursor,
                row
            )

        finally:
            cursor.close()

    def get_permissions_by_role(
        self,
        rol_id: int
    ) -> list[str]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    p.codigo_permiso
                FROM rol_permisos rp
                INNER JOIN permisos p
                    ON p.permiso_id =
                       rp.permiso_id
                WHERE rp.rol_id = :rol_id
                ORDER BY p.codigo_permiso
                """,
                {
                    "rol_id":
                        rol_id
                }
            )

            rows = cursor.fetchall()

            return [
                row[0]
                for row in rows
            ]

        finally:
            cursor.close()

    def update_password_hash(
        self,
        usuario_id: int,
        new_password_hash: str
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE usuarios
                SET password_hash =
                    :password_hash
                WHERE usuario_id =
                    :usuario_id
                """,
                {
                    "usuario_id":
                        usuario_id,

                    "password_hash":
                        new_password_hash
                }
            )

        finally:
            cursor.close()

    def invalidate_unused_reset_tokens(
        self,
        usuario_id: int
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE password_reset_tokens
                SET fecha_uso = SYSTIMESTAMP
                WHERE usuario_id = :usuario_id
                AND fecha_uso IS NULL
                """,
                {
                    "usuario_id":
                        usuario_id
                }
            )

        finally:
            cursor.close()

    def create_password_reset_token(
        self,
        usuario_id: int,
        token_hash: str,
        expire_minutes: int,
        solicitud_ip=None,
        request_id=None
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO password_reset_tokens (
                    usuario_id,
                    token_hash,
                    fecha_expiracion,
                    solicitud_ip,
                    request_id
                )
                VALUES (
                    :usuario_id,
                    :token_hash,
                    SYSTIMESTAMP
                        + NUMTODSINTERVAL(
                            :expire_minutes,
                            'MINUTE'
                        ),
                    :solicitud_ip,
                    :request_id
                )
                """,
                {
                    "usuario_id":
                        usuario_id,

                    "token_hash":
                        token_hash,

                    "expire_minutes":
                        expire_minutes,

                    "solicitud_ip":
                        solicitud_ip,

                    "request_id":
                        request_id
                }
            )

        finally:
            cursor.close()

    def get_valid_password_reset_token(
        self,
        token_hash: str
    ) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    prt.reset_token_id,
                    prt.usuario_id,
                    u.rol_id,
                    r.nombre_rol,
                    u.nombre_usuario,
                    u.correo,
                    u.password_hash,
                    u.estado AS usuario_estado,
                    r.estado AS rol_estado,
                    prt.fecha_expiracion
                FROM password_reset_tokens prt
                INNER JOIN usuarios u
                    ON u.usuario_id =
                       prt.usuario_id
                INNER JOIN roles r
                    ON r.rol_id = u.rol_id
                WHERE prt.token_hash = :token_hash
                AND prt.fecha_uso IS NULL
                AND prt.fecha_expiracion > SYSTIMESTAMP
                """,
                {
                    "token_hash":
                        token_hash
                }
            )

            row = cursor.fetchone()

            return row_to_dict(
                cursor,
                row
            )

        finally:
            cursor.close()

    def mark_password_reset_token_used(
        self,
        reset_token_id: int
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE password_reset_tokens
                SET fecha_uso = SYSTIMESTAMP
                WHERE reset_token_id =
                    :reset_token_id
                AND fecha_uso IS NULL
                """,
                {
                    "reset_token_id":
                        reset_token_id
                }
            )

        finally:
            cursor.close()

    def invalidate_other_reset_tokens(
        self,
        usuario_id: int,
        reset_token_id: int
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE password_reset_tokens
                SET fecha_uso = SYSTIMESTAMP
                WHERE usuario_id = :usuario_id
                AND reset_token_id <>
                    :reset_token_id
                AND fecha_uso IS NULL
                """,
                {
                    "usuario_id":
                        usuario_id,

                    "reset_token_id":
                        reset_token_id
                }
            )

        finally:
            cursor.close()