import oracledb
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from backend.database import get_db
from backend.routes.doctor_routes import router as doctor_router
from backend.routes.especialidad_routes import router as especialidad_router
from backend.routes.paciente_routes import router as paciente_router


app = FastAPI(
    title="SmileCare API",
    description="Backend FastAPI conectado a Oracle para el proyecto SmileCare.",
    version="1.0.0"
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
    allow_headers=["*"],
)


app.include_router(paciente_router)
app.include_router(especialidad_router)
app.include_router(doctor_router)


def raise_database_error(error: Exception):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {str(error)}"
    )


@app.get("/")
def home():
    return {
        "message": "SmileCare API funcionando correctamente."
    }


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