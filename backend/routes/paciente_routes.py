from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import PacienteCreate, PacienteUpdate
from backend.services.paciente_service import PacienteService


router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)


@router.get("")
def get_pacientes(connection=Depends(get_db)):
    paciente_service = PacienteService(connection)

    return paciente_service.get_all_pacientes()


@router.get("/{paciente_id}")
def get_paciente(paciente_id: int, connection=Depends(get_db)):
    paciente_service = PacienteService(connection)

    return paciente_service.get_paciente_by_id(paciente_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_paciente(
    paciente: PacienteCreate,
    connection=Depends(get_db)
):
    paciente_service = PacienteService(connection)

    paciente_data = paciente.model_dump()

    return paciente_service.create_paciente(paciente_data)


@router.put("/{paciente_id}")
def update_paciente(
    paciente_id: int,
    paciente: PacienteUpdate,
    connection=Depends(get_db)
):
    paciente_service = PacienteService(connection)

    paciente_data = paciente.model_dump(exclude_unset=True)

    return paciente_service.update_paciente(
        paciente_id,
        paciente_data
    )


@router.delete("/{paciente_id}")
def delete_paciente(paciente_id: int, connection=Depends(get_db)):
    paciente_service = PacienteService(connection)

    return paciente_service.delete_paciente(paciente_id)