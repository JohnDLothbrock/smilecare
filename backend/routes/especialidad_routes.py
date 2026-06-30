from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import EspecialidadCreate, EspecialidadUpdate
from backend.services.especialidad_service import EspecialidadService


router = APIRouter(
    prefix="/especialidades",
    tags=["Especialidades"]
)


@router.get("")
def get_especialidades(connection=Depends(get_db)):
    especialidad_service = EspecialidadService(connection)

    return especialidad_service.get_all_especialidades()


@router.get("/{especialidad_id}")
def get_especialidad(especialidad_id: int, connection=Depends(get_db)):
    especialidad_service = EspecialidadService(connection)

    return especialidad_service.get_especialidad_by_id(especialidad_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_especialidad(
    especialidad: EspecialidadCreate,
    connection=Depends(get_db)
):
    especialidad_service = EspecialidadService(connection)

    especialidad_data = especialidad.model_dump()

    return especialidad_service.create_especialidad(especialidad_data)


@router.put("/{especialidad_id}")
def update_especialidad(
    especialidad_id: int,
    especialidad: EspecialidadUpdate,
    connection=Depends(get_db)
):
    especialidad_service = EspecialidadService(connection)

    especialidad_data = especialidad.model_dump(exclude_unset=True)

    return especialidad_service.update_especialidad(
        especialidad_id,
        especialidad_data
    )


@router.delete("/{especialidad_id}")
def delete_especialidad(especialidad_id: int, connection=Depends(get_db)):
    especialidad_service = EspecialidadService(connection)

    return especialidad_service.delete_especialidad(especialidad_id)