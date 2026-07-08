import oracledb

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status
)
from fastapi.middleware.cors import (
    CORSMiddleware
)

from backend.core.auth_dependencies import (
    require_any_permission,
    require_method_permissions,
    require_permission
)
from backend.core.exception_handlers import (
    register_exception_handlers
)
from backend.core.logger import (
    get_logger,
    setup_logging
)
from backend.database import get_db

from backend.middleware.audit_logging import (
    AuditLoggingMiddleware
)
from backend.middleware.request_logging import (
    RequestLoggingMiddleware
)

from backend.routes.audit_admin_routes import (
    router as audit_admin_router
)
from backend.routes.auth_routes import (
    router as auth_router
)
from backend.routes.cirugia_routes import (
    router as cirugia_router
)
from backend.routes.cita_routes import (
    router as cita_router
)
from backend.routes.compra_routes import (
    router as compra_router
)
from backend.routes.comprobante_routes import (
    router as comprobante_router
)
from backend.routes.consulta_routes import (
    router as consulta_router
)
from backend.routes.detalle_compra_routes import (
    router as detalle_compra_router
)
from backend.routes.detalle_factura_routes import (
    router as detalle_factura_router
)
from backend.routes.disponibilidad_doctor_routes import (
    router as disponibilidad_doctor_router
)
from backend.routes.doctor_routes import (
    router as doctor_router
)
from backend.routes.especialidad_routes import (
    router as especialidad_router
)
from backend.routes.factura_routes import (
    router as factura_router
)
from backend.routes.historial_medico_routes import (
    router as historial_medico_router
)
from backend.routes.horario_doctor_routes import (
    router as horario_doctor_router
)
from backend.routes.insumo_routes import (
    router as insumo_router
)
from backend.routes.inventario_stock_routes import (
    router as inventario_stock_router
)
from backend.routes.metodo_pago_routes import (
    router as metodo_pago_router
)
from backend.routes.movimiento_inventario_routes import (
    router as movimiento_inventario_router
)
from backend.routes.paciente_routes import (
    router as paciente_router
)
from backend.routes.pago_routes import (
    router as pago_router
)
from backend.routes.proveedor_routes import (
    router as proveedor_router
)
from backend.routes.security_routes import (
    router as security_router
)
from backend.routes.tratamiento_consulta_routes import (
    router as tratamiento_consulta_router
)
from backend.routes.tratamiento_routes import (
    router as tratamiento_router
)


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

setup_logging()

logger = get_logger(
    "app"
)


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="SmileCare API",
    description=(
        "Backend FastAPI conectado a Oracle "
        "para el proyecto SmileCare."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# EXCEPTION HANDLERS
# ---------------------------------------------------------

register_exception_handlers(
    app
)


# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------

app.add_middleware(
    RequestLoggingMiddleware
)


app.add_middleware(
    AuditLoggingMiddleware
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ---------------------------------------------------------
# PUBLIC ROUTES
# ---------------------------------------------------------

app.include_router(
    auth_router
)


# ---------------------------------------------------------
# CLINICAL ROUTES
# ---------------------------------------------------------

app.include_router(
    paciente_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "PACIENTES_VER",
                    "PACIENTES_GESTIONAR"
                ),
                write_permissions=(
                    "PACIENTES_GESTIONAR",
                )
            )
        )
    ]
)


app.include_router(
    especialidad_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "DOCTORES_GESTIONAR",
                    "CITAS_GESTIONAR",
                    "CONSULTAS_GESTIONAR",
                    "AGENDA_GESTIONAR"
                ),
                write_permissions=(
                    "DOCTORES_GESTIONAR",
                )
            )
        )
    ]
)


app.include_router(
    doctor_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "DOCTORES_GESTIONAR",
                    "CITAS_GESTIONAR",
                    "CONSULTAS_GESTIONAR",
                    "AGENDA_GESTIONAR"
                ),
                write_permissions=(
                    "DOCTORES_GESTIONAR",
                )
            )
        )
    ]
)


app.include_router(
    cita_router,
    dependencies=[
        Depends(
            require_any_permission(
                "CITAS_GESTIONAR"
            )
        )
    ]
)


app.include_router(
    consulta_router,
    dependencies=[
        Depends(
            require_any_permission(
                "CONSULTAS_GESTIONAR"
            )
        )
    ]
)


app.include_router(
    tratamiento_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "TRATAMIENTOS_GESTIONAR",
                    "CONSULTAS_GESTIONAR",
                    "CAJA_USAR"
                ),
                write_permissions=(
                    "TRATAMIENTOS_GESTIONAR",
                )
            )
        )
    ]
)


app.include_router(
    tratamiento_consulta_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "CONSULTAS_GESTIONAR",
                    "EXPEDIENTE_GESTIONAR"
                ),
                write_permissions=(
                    "CONSULTAS_GESTIONAR",
                )
            )
        )
    ]
)


app.include_router(
    historial_medico_router,
    dependencies=[
        Depends(
            require_any_permission(
                "EXPEDIENTE_GESTIONAR"
            )
        )
    ]
)


app.include_router(
    cirugia_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "CONSULTAS_GESTIONAR",
                    "EXPEDIENTE_GESTIONAR"
                ),
                write_permissions=(
                    "CONSULTAS_GESTIONAR",
                )
            )
        )
    ]
)


app.include_router(
    horario_doctor_router,
    dependencies=[
        Depends(
            require_any_permission(
                "AGENDA_GESTIONAR",
                "CITAS_GESTIONAR"
            )
        )
    ]
)


app.include_router(
    disponibilidad_doctor_router,
    dependencies=[
        Depends(
            require_any_permission(
                "AGENDA_GESTIONAR",
                "CITAS_GESTIONAR"
            )
        )
    ]
)


# ---------------------------------------------------------
# FINANCE ROUTES
# ---------------------------------------------------------

app.include_router(
    factura_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "FACTURAS_VER",
                    "CAJA_USAR"
                ),
                write_permissions=(
                    "CAJA_USAR",
                )
            )
        )
    ]
)


app.include_router(
    detalle_factura_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "FACTURAS_VER",
                    "CAJA_USAR"
                ),
                write_permissions=(
                    "CAJA_USAR",
                )
            )
        )
    ]
)


app.include_router(
    metodo_pago_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "METODOS_PAGO_GESTIONAR",
                    "CAJA_USAR"
                ),
                write_permissions=(
                    "METODOS_PAGO_GESTIONAR",
                )
            )
        )
    ]
)


app.include_router(
    pago_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "PAGOS_VER",
                    "CAJA_USAR"
                ),
                write_permissions=(
                    "CAJA_USAR",
                )
            )
        )
    ]
)


app.include_router(
    comprobante_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "FACTURAS_VER",
                    "PAGOS_VER",
                    "CAJA_USAR"
                ),
                write_permissions=(
                    "CAJA_USAR",
                )
            )
        )
    ]
)


# ---------------------------------------------------------
# INVENTORY ROUTES
# ---------------------------------------------------------

app.include_router(
    proveedor_router,
    dependencies=[
        Depends(
            require_any_permission(
                "PROVEEDORES_GESTIONAR"
            )
        )
    ]
)


app.include_router(
    insumo_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "INVENTARIO_VER",
                    "INVENTARIO_GESTIONAR",
                    "COMPRAS_GESTIONAR"
                ),
                write_permissions=(
                    "INVENTARIO_GESTIONAR",
                    "COMPRAS_GESTIONAR"
                )
            )
        )
    ]
)


app.include_router(
    inventario_stock_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "INVENTARIO_VER",
                    "INVENTARIO_GESTIONAR"
                ),
                write_permissions=(
                    "INVENTARIO_GESTIONAR",
                )
            )
        )
    ]
)


app.include_router(
    compra_router,
    dependencies=[
        Depends(
            require_any_permission(
                "COMPRAS_GESTIONAR"
            )
        )
    ]
)


app.include_router(
    detalle_compra_router,
    dependencies=[
        Depends(
            require_any_permission(
                "COMPRAS_GESTIONAR"
            )
        )
    ]
)


app.include_router(
    movimiento_inventario_router,
    dependencies=[
        Depends(
            require_method_permissions(
                read_permissions=(
                    "INVENTARIO_VER",
                    "INVENTARIO_GESTIONAR"
                ),
                write_permissions=(
                    "INVENTARIO_GESTIONAR",
                )
            )
        )
    ]
)


# ---------------------------------------------------------
# ADMINISTRATION ROUTES
# ---------------------------------------------------------

admin_dependencies = [
    Depends(
        require_permission(
            "ADMIN_GESTIONAR"
        )
    )
]


app.include_router(
    security_router,
    dependencies=admin_dependencies
)


app.include_router(
    audit_admin_router,
    dependencies=admin_dependencies
)


# ---------------------------------------------------------
# DATABASE ERROR HELPER
# ---------------------------------------------------------

def raise_database_error(
    error: Exception
):
    logger.exception(
        "Database error: %s",
        str(error)
    )

    raise HTTPException(
        status_code=(
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ),
        detail=(
            "Error de base de datos: "
            f"{str(error)}"
        )
    )


# ---------------------------------------------------------
# PUBLIC SYSTEM ENDPOINTS
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "message":
            "SmileCare API funcionando "
            "correctamente."
    }


@app.get("/health")
def health_check(
    connection=Depends(get_db)
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT 1
            FROM dual
            """
        )

        cursor.fetchone()

        return {
            "status": "ok",
            "api": "running",
            "database": "connected"
        }

    except oracledb.Error as error:
        raise_database_error(
            error
        )

    finally:
        cursor.close()


# ---------------------------------------------------------
# ADMIN-ONLY SYSTEM ENDPOINTS
# ---------------------------------------------------------

@app.get("/db/test")
def test_database_connection(
    connection=Depends(get_db),
    _current_user=Depends(
        require_permission(
            "ADMIN_GESTIONAR"
        )
    )
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                USER AS usuario_actual,
                SYSDATE AS fecha_base_datos
            FROM dual
            """
        )

        row = cursor.fetchone()

        return {
            "database":
                "Oracle",

            "connection":
                "success",

            "usuario_actual":
                row[0],

            "fecha_base_datos":
                str(row[1])
        }

    except oracledb.Error as error:
        raise_database_error(
            error
        )

    finally:
        cursor.close()


@app.get("/db/tables")
def get_database_tables(
    connection=Depends(get_db),
    _current_user=Depends(
        require_permission(
            "ADMIN_GESTIONAR"
        )
    )
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT table_name
            FROM user_tables
            ORDER BY table_name
            """
        )

        rows = cursor.fetchall()

        return {
            "tables": [
                row[0]
                for row in rows
            ]
        }

    except oracledb.Error as error:
        raise_database_error(
            error
        )

    finally:
        cursor.close()