from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import (
    TratamientoConsultaCreate,
    TratamientoConsultaUpdate
)
from backend.services.tratamiento_consulta_service import (
    TratamientoConsultaService
)


router = APIRouter(
    prefix="/tratamientos-consulta",
    tags=["Tratamientos Consulta"]
)


@router.get("")
def get_tratamientos_consulta(connection=Depends(get_db)):
    tratamiento_consulta_service = TratamientoConsultaService(connection)

    return tratamiento_consulta_service.get_all_tratamientos_consulta()


@router.get("/por-consulta/{consulta_id}")
def get_tratamientos_by_consulta_id(
    consulta_id: int,
    connection=Depends(get_db)
):
    tratamiento_consulta_service = TratamientoConsultaService(connection)

    return tratamiento_consulta_service.get_tratamientos_by_consulta_id(
        consulta_id
    )


@router.get("/{tratamiento_consulta_id}")
def get_tratamiento_consulta(
    tratamiento_consulta_id: int,
    connection=Depends(get_db)
):
    tratamiento_consulta_service = TratamientoConsultaService(connection)

    return tratamiento_consulta_service.get_tratamiento_consulta_by_id(
        tratamiento_consulta_id
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_tratamiento_consulta(
    tratamiento_consulta: TratamientoConsultaCreate,
    connection=Depends(get_db)
):
    tratamiento_consulta_service = TratamientoConsultaService(connection)

    tratamiento_consulta_data = tratamiento_consulta.model_dump()

    return tratamiento_consulta_service.create_tratamiento_consulta(
        tratamiento_consulta_data
    )


@router.put("/{tratamiento_consulta_id}")
def update_tratamiento_consulta(
    tratamiento_consulta_id: int,
    tratamiento_consulta: TratamientoConsultaUpdate,
    connection=Depends(get_db)
):
    tratamiento_consulta_service = TratamientoConsultaService(connection)

    tratamiento_consulta_data = tratamiento_consulta.model_dump(exclude_unset=True)

    return tratamiento_consulta_service.update_tratamiento_consulta(
        tratamiento_consulta_id,
        tratamiento_consulta_data
    )


@router.delete("/{tratamiento_consulta_id}")
def delete_tratamiento_consulta(
    tratamiento_consulta_id: int,
    connection=Depends(get_db)
):
    tratamiento_consulta_service = TratamientoConsultaService(connection)

    return tratamiento_consulta_service.delete_tratamiento_consulta(
        tratamiento_consulta_id
    )