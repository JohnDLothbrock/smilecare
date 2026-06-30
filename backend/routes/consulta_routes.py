from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import ConsultaCreate, ConsultaUpdate
from backend.services.consulta_service import ConsultaService


router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)


@router.get("")
def get_consultas(connection=Depends(get_db)):
    consulta_service = ConsultaService(connection)

    return consulta_service.get_all_consultas()


@router.get("/por-cita/{cita_id}")
def get_consulta_by_cita_id(cita_id: int, connection=Depends(get_db)):
    consulta_service = ConsultaService(connection)

    return consulta_service.get_consulta_by_cita_id(cita_id)


@router.get("/{consulta_id}")
def get_consulta(consulta_id: int, connection=Depends(get_db)):
    consulta_service = ConsultaService(connection)

    return consulta_service.get_consulta_by_id(consulta_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_consulta(
    consulta: ConsultaCreate,
    connection=Depends(get_db)
):
    consulta_service = ConsultaService(connection)

    consulta_data = consulta.model_dump()

    return consulta_service.create_consulta(consulta_data)


@router.put("/{consulta_id}")
def update_consulta(
    consulta_id: int,
    consulta: ConsultaUpdate,
    connection=Depends(get_db)
):
    consulta_service = ConsultaService(connection)

    consulta_data = consulta.model_dump(exclude_unset=True)

    return consulta_service.update_consulta(
        consulta_id,
        consulta_data
    )


@router.delete("/{consulta_id}")
def delete_consulta(consulta_id: int, connection=Depends(get_db)):
    consulta_service = ConsultaService(connection)

    return consulta_service.delete_consulta(consulta_id)