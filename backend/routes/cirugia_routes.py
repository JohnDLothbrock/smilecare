from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import CirugiaCreate, CirugiaUpdate
from backend.services.cirugia_service import CirugiaService


router = APIRouter(
    prefix="/cirugias",
    tags=["Cirugías"]
)


@router.get("")
def get_cirugias(connection=Depends(get_db)):
    cirugia_service = CirugiaService(connection)

    return cirugia_service.get_all_cirugias()


@router.get("/por-tratamiento-consulta/{tratamiento_consulta_id}")
def get_cirugia_by_tratamiento_consulta_id(
    tratamiento_consulta_id: int,
    connection=Depends(get_db)
):
    cirugia_service = CirugiaService(connection)

    return cirugia_service.get_cirugia_by_tratamiento_consulta_id(
        tratamiento_consulta_id
    )


@router.get("/{cirugia_id}")
def get_cirugia(cirugia_id: int, connection=Depends(get_db)):
    cirugia_service = CirugiaService(connection)

    return cirugia_service.get_cirugia_by_id(cirugia_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_cirugia(
    cirugia: CirugiaCreate,
    connection=Depends(get_db)
):
    cirugia_service = CirugiaService(connection)

    cirugia_data = cirugia.model_dump()

    return cirugia_service.create_cirugia(cirugia_data)


@router.put("/{cirugia_id}")
def update_cirugia(
    cirugia_id: int,
    cirugia: CirugiaUpdate,
    connection=Depends(get_db)
):
    cirugia_service = CirugiaService(connection)

    cirugia_data = cirugia.model_dump(exclude_unset=True)

    return cirugia_service.update_cirugia(
        cirugia_id,
        cirugia_data
    )


@router.delete("/{cirugia_id}")
def delete_cirugia(cirugia_id: int, connection=Depends(get_db)):
    cirugia_service = CirugiaService(connection)

    return cirugia_service.delete_cirugia(cirugia_id)