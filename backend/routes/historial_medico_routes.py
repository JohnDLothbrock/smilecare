from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import HistorialMedicoCreate, HistorialMedicoUpdate
from backend.services.historial_medico_service import HistorialMedicoService


router = APIRouter(
    prefix="/historial-medico",
    tags=["Historial Médico"]
)


@router.get("")
def get_historiales(connection=Depends(get_db)):
    historial_service = HistorialMedicoService(connection)

    return historial_service.get_all_historiales()


@router.get("/por-paciente/{paciente_id}")
def get_historiales_by_paciente_id(
    paciente_id: int,
    connection=Depends(get_db)
):
    historial_service = HistorialMedicoService(connection)

    return historial_service.get_historiales_by_paciente_id(paciente_id)


@router.get("/{historial_id}")
def get_historial(historial_id: int, connection=Depends(get_db)):
    historial_service = HistorialMedicoService(connection)

    return historial_service.get_historial_by_id(historial_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_historial(
    historial: HistorialMedicoCreate,
    connection=Depends(get_db)
):
    historial_service = HistorialMedicoService(connection)

    historial_data = historial.model_dump()

    return historial_service.create_historial(historial_data)


@router.put("/{historial_id}")
def update_historial(
    historial_id: int,
    historial: HistorialMedicoUpdate,
    connection=Depends(get_db)
):
    historial_service = HistorialMedicoService(connection)

    historial_data = historial.model_dump(exclude_unset=True)

    return historial_service.update_historial(
        historial_id,
        historial_data
    )


@router.delete("/{historial_id}")
def delete_historial(historial_id: int, connection=Depends(get_db)):
    historial_service = HistorialMedicoService(connection)

    return historial_service.delete_historial(historial_id)