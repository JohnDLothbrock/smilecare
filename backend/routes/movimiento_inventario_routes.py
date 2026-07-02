from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import (
    MovimientoInventarioCreate,
    MovimientoInventarioUpdate
)
from backend.services.movimiento_inventario_service import (
    MovimientoInventarioService
)


router = APIRouter(
    prefix="/movimientos-inventario",
    tags=["Movimientos Inventario"]
)


@router.get("")
def get_movimientos(connection=Depends(get_db)):
    movimiento_service = MovimientoInventarioService(connection)

    return movimiento_service.get_all_movimientos()


@router.get("/por-insumo/{insumo_id}")
def get_movimientos_by_insumo_id(
    insumo_id: int,
    connection=Depends(get_db)
):
    movimiento_service = MovimientoInventarioService(connection)

    return movimiento_service.get_movimientos_by_insumo_id(insumo_id)


@router.get("/{movimiento_id}")
def get_movimiento(movimiento_id: int, connection=Depends(get_db)):
    movimiento_service = MovimientoInventarioService(connection)

    return movimiento_service.get_movimiento_by_id(movimiento_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_movimiento(
    movimiento: MovimientoInventarioCreate,
    connection=Depends(get_db)
):
    movimiento_service = MovimientoInventarioService(connection)

    movimiento_data = movimiento.model_dump()

    return movimiento_service.create_movimiento(movimiento_data)


@router.put("/{movimiento_id}")
def update_movimiento(
    movimiento_id: int,
    movimiento: MovimientoInventarioUpdate,
    connection=Depends(get_db)
):
    movimiento_service = MovimientoInventarioService(connection)

    movimiento_data = movimiento.model_dump(exclude_unset=True)

    return movimiento_service.update_movimiento(
        movimiento_id,
        movimiento_data
    )


@router.delete("/{movimiento_id}")
def delete_movimiento(
    movimiento_id: int,
    connection=Depends(get_db)
):
    movimiento_service = MovimientoInventarioService(connection)

    return movimiento_service.delete_movimiento(movimiento_id)