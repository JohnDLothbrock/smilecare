import oracledb
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from backend.core.exception_handlers import register_exception_handlers
from backend.core.logger import get_logger, setup_logging
from backend.database import get_db
from backend.middleware.request_logging import RequestLoggingMiddleware

from backend.routes.cirugia_routes import router as cirugia_router
from backend.routes.cita_routes import router as cita_router
from backend.routes.compra_routes import router as compra_router
from backend.routes.comprobante_routes import router as comprobante_router
from backend.routes.consulta_routes import router as consulta_router
from backend.routes.detalle_compra_routes import router as detalle_compra_router
from backend.routes.detalle_factura_routes import router as detalle_factura_router
from backend.routes.doctor_routes import router as doctor_router
from backend.routes.especialidad_routes import router as especialidad_router
from backend.routes.factura_routes import router as factura_router
from backend.routes.historial_medico_routes import router as historial_medico_router
from backend.routes.insumo_routes import router as insumo_router
from backend.routes.inventario_stock_routes import router as inventario_stock_router
from backend.routes.metodo_pago_routes import router as metodo_pago_router
from backend.routes.movimiento_inventario_routes import (
    router as movimiento_inventario_router
)
from backend.routes.paciente_routes import router as paciente_router
from backend.routes.pago_routes import router as pago_router
from backend.routes.proveedor_routes import router as proveedor_router
from backend.routes.tratamiento_consulta_routes import (
    router as tratamiento_consulta_router
)
from backend.routes.tratamiento_routes import router as tratamiento_router
from backend.routes.disponibilidad_doctor_routes import (
    router as disponibilidad_doctor_router
)
from backend.routes.horario_doctor_routes import router as horario_doctor_router
from backend.routes.security_routes import router as security_router

setup_logging()

logger = get_logger("app")


app = FastAPI(
    title="SmileCare API",
    description="Backend FastAPI conectado a Oracle para el proyecto SmileCare.",
    version="1.0.0"
)


register_exception_handlers(app)


app.add_middleware(RequestLoggingMiddleware)


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
    allow_headers=["*"],
)


app.include_router(paciente_router)
app.include_router(especialidad_router)
app.include_router(doctor_router)
app.include_router(cita_router)
app.include_router(consulta_router)
app.include_router(tratamiento_router)
app.include_router(tratamiento_consulta_router)
app.include_router(factura_router)
app.include_router(detalle_factura_router)
app.include_router(metodo_pago_router)
app.include_router(pago_router)
app.include_router(comprobante_router)
app.include_router(historial_medico_router)
app.include_router(cirugia_router)
app.include_router(proveedor_router)
app.include_router(insumo_router)
app.include_router(inventario_stock_router)
app.include_router(compra_router)
app.include_router(detalle_compra_router)
app.include_router(movimiento_inventario_router)
app.include_router(horario_doctor_router)
app.include_router(disponibilidad_doctor_router)
app.include_router(security_router)


def raise_database_error(error: Exception):
    logger.exception("Database error: %s", str(error))

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {str(error)}"
    )


@app.get("/")
def home():
    return {
        "message": "SmileCare API funcionando correctamente."
    }


@app.get("/health")
def health_check(connection=Depends(get_db)):
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
        raise_database_error(error)

    finally:
        cursor.close()


@app.get("/db/test")
def test_database_connection(connection=Depends(get_db)):
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
            "database": "Oracle",
            "connection": "success",
            "usuario_actual": row[0],
            "fecha_base_datos": str(row[1])
        }

    except oracledb.Error as error:
        raise_database_error(error)

    finally:
        cursor.close()


@app.get("/db/tables")
def get_database_tables(connection=Depends(get_db)):
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
            "tables": [row[0] for row in rows]
        }

    except oracledb.Error as error:
        raise_database_error(error)

    finally:
        cursor.close()