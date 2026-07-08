import re

from backend.repositories.audit_repository import (
    AuditRepository
)


class AuditService:

    def __init__(
        self,
        connection
    ):
        self.connection = connection

        self.audit_repository = (
            AuditRepository(
                connection
            )
        )


    # -----------------------------------------------------
    # VALUE HELPERS
    # -----------------------------------------------------

    @staticmethod
    def truncate(
        value,
        max_length: int
    ):
        if value is None:
            return None

        return str(value)[
            :max_length
        ]


    # -----------------------------------------------------
    # ACTOR INFORMATION
    # -----------------------------------------------------

    def get_actor(
        self,
        usuario_id
    ):
        if usuario_id is None:
            return None

        return (
            self.audit_repository
            .get_actor_by_id(
                usuario_id
            )
        )


    # -----------------------------------------------------
    # ACCESS HISTORY
    # -----------------------------------------------------

    def record_access_event(
        self,
        evento: str,
        resultado: str,
        usuario_id=None,
        nombre_usuario=None,
        nombre_rol=None,
        detalle=None,
        ip_origen=None,
        user_agent=None,
        request_id=None
    ):
        access_data = {
            "usuario_id":
                usuario_id,

            "nombre_usuario":
                self.truncate(
                    nombre_usuario,
                    50
                ),

            "nombre_rol":
                self.truncate(
                    nombre_rol,
                    50
                ),

            "evento":
                self.truncate(
                    evento,
                    50
                ),

            "resultado":
                self.truncate(
                    resultado,
                    20
                ),

            "detalle":
                self.truncate(
                    detalle,
                    500
                ),

            "ip_origen":
                self.truncate(
                    ip_origen,
                    64
                ),

            "user_agent":
                self.truncate(
                    user_agent,
                    500
                ),

            "request_id":
                self.truncate(
                    request_id,
                    100
                )
        }

        self.audit_repository.create_access_event(
            access_data
        )


    # -----------------------------------------------------
    # MODULE AND ENTITY
    # -----------------------------------------------------

    @staticmethod
    def resolve_module_and_entity(
        path: str
    ):
        path_mapping = [
            (
                "/tratamientos-consulta",
                "CLINICA",
                "TRATAMIENTOS_CONSULTA"
            ),
            (
                "/historial-medico",
                "CLINICA",
                "HISTORIAL_MEDICO"
            ),
            (
                "/horarios-doctores",
                "CLINICA",
                "HORARIOS_DOCTORES"
            ),
            (
                "/horario-doctor",
                "CLINICA",
                "HORARIOS_DOCTORES"
            ),
            (
                "/disponibilidad-doctores",
                "CLINICA",
                "DISPONIBILIDAD_DOCTORES"
            ),
            (
                "/disponibilidad-doctor",
                "CLINICA",
                "DISPONIBILIDAD_DOCTORES"
            ),
            (
                "/pacientes",
                "CLINICA",
                "PACIENTES"
            ),
            (
                "/doctores",
                "CLINICA",
                "DOCTORES"
            ),
            (
                "/especialidades",
                "CLINICA",
                "ESPECIALIDADES"
            ),
            (
                "/citas",
                "CLINICA",
                "CITAS"
            ),
            (
                "/consultas",
                "CLINICA",
                "CONSULTAS"
            ),
            (
                "/cirugias",
                "CLINICA",
                "CIRUGIAS"
            ),
            (
                "/tratamientos",
                "TRATAMIENTOS",
                "TRATAMIENTOS"
            ),

            (
                "/detalle-factura",
                "FINANZAS",
                "DETALLE_FACTURA"
            ),
            (
                "/metodos-pago",
                "FINANZAS",
                "METODOS_PAGO"
            ),
            (
                "/comprobantes",
                "FINANZAS",
                "COMPROBANTES"
            ),
            (
                "/facturas",
                "FINANZAS",
                "FACTURAS"
            ),
            (
                "/pagos",
                "FINANZAS",
                "PAGOS"
            ),

            (
                "/movimientos-inventario",
                "INVENTARIO",
                "MOVIMIENTOS_INVENTARIO"
            ),
            (
                "/inventario-stock",
                "INVENTARIO",
                "INVENTARIO_STOCK"
            ),
            (
                "/detalle-compra",
                "INVENTARIO",
                "DETALLE_COMPRA"
            ),
            (
                "/proveedores",
                "INVENTARIO",
                "PROVEEDORES"
            ),
            (
                "/insumos",
                "INVENTARIO",
                "INSUMOS"
            ),
            (
                "/compras",
                "INVENTARIO",
                "COMPRAS"
            ),

            (
                "/rol-permisos",
                "ADMINISTRACION",
                "ROL_PERMISOS"
            ),
            (
                "/usuarios",
                "ADMINISTRACION",
                "USUARIOS"
            ),
            (
                "/roles",
                "ADMINISTRACION",
                "ROLES"
            ),
            (
                "/permisos",
                "ADMINISTRACION",
                "PERMISOS"
            )
        ]

        for (
            route_prefix,
            module,
            entity
        ) in path_mapping:
            if path.startswith(
                route_prefix
            ):
                return (
                    module,
                    entity
                )

        first_path_part = (
            path
            .strip("/")
            .split("/")[0]
        )

        entity = (
            first_path_part
            .replace("-", "_")
            .upper()
            or "SISTEMA"
        )

        return (
            "SISTEMA",
            entity
        )


    # -----------------------------------------------------
    # ACTION
    # -----------------------------------------------------

    @staticmethod
    def resolve_action(
        method: str,
        path: str
    ):
        normalized_path = (
            path.lower()
        )

        if "restaurar" in normalized_path:
            return "RESTAURAR"

        if "revertir" in normalized_path:
            return "REVERTIR"

        if normalized_path.endswith(
            "/estado"
        ):
            return "CAMBIAR_ESTADO"

        if normalized_path.endswith(
            "/producto"
        ):
            return "ACTUALIZAR_PRODUCTO"

        method_actions = {
            "POST": "CREAR",
            "PUT": "ACTUALIZAR",
            "PATCH": "ACTUALIZAR",
            "DELETE": "ELIMINAR"
        }

        return method_actions.get(
            method.upper(),
            "ACCESO"
        )


    # -----------------------------------------------------
    # RECORD IDENTIFIER
    # -----------------------------------------------------

    @staticmethod
    def extract_record_key(
        path: str
    ):
        numeric_segments = re.findall(
            r"/(\d+)",
            path
        )

        if not numeric_segments:
            return None

        return "/".join(
            numeric_segments
        )


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    @staticmethod
    def resolve_result(
        status_code: int
    ):
        if status_code in (
            401,
            403
        ):
            return "DENEGADO"

        if 200 <= status_code < 400:
            return "EXITOSO"

        return "FALLIDO"


    # -----------------------------------------------------
    # REQUEST AUDIT
    # -----------------------------------------------------

    def record_request(
        self,
        method: str,
        path: str,
        status_code: int,
        usuario_id=None,
        ip_origen=None,
        request_id=None
    ):
        actor = self.get_actor(
            usuario_id
        )

        module, entity = (
            self.resolve_module_and_entity(
                path
            )
        )

        action = self.resolve_action(
            method,
            path
        )

        result = self.resolve_result(
            status_code
        )

        record_key = (
            self.extract_record_key(
                path
            )
        )

        if result == "EXITOSO":
            detail = (
                f"Solicitud {method.upper()} "
                f"{path} completada "
                f"correctamente."
            )

        elif result == "DENEGADO":
            detail = (
                f"Acceso denegado a "
                f"{method.upper()} {path}."
            )

        else:
            detail = (
                f"Solicitud {method.upper()} "
                f"{path} finalizó con "
                f"HTTP {status_code}."
            )

        audit_data = {
            "usuario_id":
                actor.get(
                    "usuario_id"
                )
                if actor
                else None,

            "nombre_usuario":
                actor.get(
                    "nombre_usuario"
                )
                if actor
                else None,

            "nombre_rol":
                actor.get(
                    "nombre_rol"
                )
                if actor
                else None,

            "modulo":
                self.truncate(
                    module,
                    50
                ),

            "entidad":
                self.truncate(
                    entity,
                    100
                ),

            "accion":
                self.truncate(
                    action,
                    50
                ),

            "metodo_http":
                self.truncate(
                    method.upper(),
                    10
                ),

            "ruta":
                self.truncate(
                    path,
                    250
                ),

            "valor_llave":
                self.truncate(
                    record_key,
                    100
                ),

            "resultado":
                result,

            "status_code":
                status_code,

            "detalle":
                self.truncate(
                    detail,
                    1000
                ),

            "ip_origen":
                self.truncate(
                    ip_origen,
                    64
                ),

            "request_id":
                self.truncate(
                    request_id,
                    100
                )
        }

        self.audit_repository.create_system_audit(
            audit_data
        )