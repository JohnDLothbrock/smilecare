from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import InsumoCreate, InsumoUpdate
from backend.services.insumo_service import InsumoService


router = APIRouter(
    prefix="/insumos",
    tags=["Insumos"]
)


@router.get("")
def get_insumos(connection=Depends(get_db)):
    insumo_service = InsumoService(connection)

    return insumo_service.get_all_insumos()


@router.get("/{insumo_id}")
def get_insumo(insumo_id: int, connection=Depends(get_db)):
    insumo_service = InsumoService(connection)

    return insumo_service.get_insumo_by_id(insumo_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_insumo(
    insumo: InsumoCreate,
    connection=Depends(get_db)
):
    insumo_service = InsumoService(connection)

    insumo_data = insumo.model_dump()

    return insumo_service.create_insumo(insumo_data)


@router.put("/{insumo_id}")
def update_insumo(
    insumo_id: int,
    insumo: InsumoUpdate,
    connection=Depends(get_db)
):
    insumo_service = InsumoService(connection)

    insumo_data = insumo.model_dump(exclude_unset=True)

    return insumo_service.update_insumo(
        insumo_id,
        insumo_data
    )


@router.delete("/{insumo_id}")
def delete_insumo(insumo_id: int, connection=Depends(get_db)):
    insumo_service = InsumoService(connection)

    return insumo_service.delete_insumo(insumo_id)