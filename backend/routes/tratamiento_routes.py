from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import TratamientoCreate, TratamientoUpdate
from backend.services.tratamiento_service import TratamientoService


router = APIRouter(
    prefix="/tratamientos",
    tags=["Tratamientos"]
)


@router.get("")
def get_tratamientos(connection=Depends(get_db)):
    tratamiento_service = TratamientoService(connection)

    return tratamiento_service.get_all_tratamientos()


@router.get("/{tratamiento_id}")
def get_tratamiento(tratamiento_id: int, connection=Depends(get_db)):
    tratamiento_service = TratamientoService(connection)

    return tratamiento_service.get_tratamiento_by_id(tratamiento_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_tratamiento(
    tratamiento: TratamientoCreate,
    connection=Depends(get_db)
):
    tratamiento_service = TratamientoService(connection)

    tratamiento_data = tratamiento.model_dump()

    return tratamiento_service.create_tratamiento(tratamiento_data)


@router.put("/{tratamiento_id}")
def update_tratamiento(
    tratamiento_id: int,
    tratamiento: TratamientoUpdate,
    connection=Depends(get_db)
):
    tratamiento_service = TratamientoService(connection)

    tratamiento_data = tratamiento.model_dump(exclude_unset=True)

    return tratamiento_service.update_tratamiento(
        tratamiento_id,
        tratamiento_data
    )


@router.delete("/{tratamiento_id}")
def delete_tratamiento(tratamiento_id: int, connection=Depends(get_db)):
    tratamiento_service = TratamientoService(connection)

    return tratamiento_service.delete_tratamiento(tratamiento_id)