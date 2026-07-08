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


class AuditRepository:

    def __init__(
        self,
        connection
    ):
        self.connection = connection


    # -----------------------------------------------------
    # AUTHENTICATED USER INFORMATION
    # -----------------------------------------------------

    def get_actor_by_id(
        self,
        usuario_id: int
    ) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    u.usuario_id,
                    u.nombre_usuario,
                    r.nombre_rol
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


    # -----------------------------------------------------
    # ACCESS HISTORY
    # -----------------------------------------------------

    def create_access_event(
        self,
        access_data: dict
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO historial_accesos (
                    usuario_id,
                    nombre_usuario,
                    nombre_rol,
                    evento,
                    resultado,
                    detalle,
                    ip_origen,
                    user_agent,
                    request_id
                )
                VALUES (
                    :usuario_id,
                    :nombre_usuario,
                    :nombre_rol,
                    :evento,
                    :resultado,
                    :detalle,
                    :ip_origen,
                    :user_agent,
                    :request_id
                )
                """,
                {
                    "usuario_id":
                        access_data.get(
                            "usuario_id"
                        ),

                    "nombre_usuario":
                        access_data.get(
                            "nombre_usuario"
                        ),

                    "nombre_rol":
                        access_data.get(
                            "nombre_rol"
                        ),

                    "evento":
                        access_data.get(
                            "evento"
                        ),

                    "resultado":
                        access_data.get(
                            "resultado"
                        ),

                    "detalle":
                        access_data.get(
                            "detalle"
                        ),

                    "ip_origen":
                        access_data.get(
                            "ip_origen"
                        ),

                    "user_agent":
                        access_data.get(
                            "user_agent"
                        ),

                    "request_id":
                        access_data.get(
                            "request_id"
                        )
                }
            )

        finally:
            cursor.close()


    # -----------------------------------------------------
    # APPLICATION AUDIT
    # -----------------------------------------------------

    def create_system_audit(
        self,
        audit_data: dict
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO auditoria_sistema (
                    usuario_id,
                    nombre_usuario,
                    nombre_rol,
                    modulo,
                    entidad,
                    accion,
                    metodo_http,
                    ruta,
                    valor_llave,
                    resultado,
                    status_code,
                    detalle,
                    ip_origen,
                    request_id
                )
                VALUES (
                    :usuario_id,
                    :nombre_usuario,
                    :nombre_rol,
                    :modulo,
                    :entidad,
                    :accion,
                    :metodo_http,
                    :ruta,
                    :valor_llave,
                    :resultado,
                    :status_code,
                    :detalle,
                    :ip_origen,
                    :request_id
                )
                """,
                {
                    "usuario_id":
                        audit_data.get(
                            "usuario_id"
                        ),

                    "nombre_usuario":
                        audit_data.get(
                            "nombre_usuario"
                        ),

                    "nombre_rol":
                        audit_data.get(
                            "nombre_rol"
                        ),

                    "modulo":
                        audit_data.get(
                            "modulo"
                        ),

                    "entidad":
                        audit_data.get(
                            "entidad"
                        ),

                    "accion":
                        audit_data.get(
                            "accion"
                        ),

                    "metodo_http":
                        audit_data.get(
                            "metodo_http"
                        ),

                    "ruta":
                        audit_data.get(
                            "ruta"
                        ),

                    "valor_llave":
                        audit_data.get(
                            "valor_llave"
                        ),

                    "resultado":
                        audit_data.get(
                            "resultado"
                        ),

                    "status_code":
                        audit_data.get(
                            "status_code"
                        ),

                    "detalle":
                        audit_data.get(
                            "detalle"
                        ),

                    "ip_origen":
                        audit_data.get(
                            "ip_origen"
                        ),

                    "request_id":
                        audit_data.get(
                            "request_id"
                        )
                }
            )

        finally:
            cursor.close()