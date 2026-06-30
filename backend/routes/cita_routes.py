from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import CitaCreate, CitaUpdate
from backend.services.cita_service import CitaService


router = APIRouter(
    prefix="/citas",
    tags=["Citas"]
)


@router.get("")
def get_citas(connection=Depends(get_db)):
    cita_service = CitaService(connection)

    return cita_service.get_all_citas()


@router.get("/{cita_id}")
def get_cita(cita_id: int, connection=Depends(get_db)):
    cita_service = CitaService(connection)

    return cita_service.get_cita_by_id(cita_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_cita(
    cita: CitaCreate,
    connection=Depends(get_db)
):
    cita_service = CitaService(connection)

    cita_data = cita.model_dump()

    return cita_service.create_cita(cita_data)


@router.put("/{cita_id}")
def update_cita(
    cita_id: int,
    cita: CitaUpdate,
    connection=Depends(get_db)
):
    cita_service = CitaService(connection)

    cita_data = cita.model_dump(exclude_unset=True)

    return cita_service.update_cita(
        cita_id,
        cita_data
    )


@router.delete("/{cita_id}")
def delete_cita(cita_id: int, connection=Depends(get_db)):
    cita_service = CitaService(connection)

    return cita_service.delete_cita(cita_id)