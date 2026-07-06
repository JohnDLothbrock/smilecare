from fastapi import APIRouter, Depends

from backend.database import get_db
from backend.services.inventario_stock_service import (
    InventarioStockService
)
from backend.workflow_schemas import (
    InventarioProductoEstadoUpdate,
    InventarioProductoStockUpdate
)


router = APIRouter(
    prefix="/inventario-stock",
    tags=["Inventario Stock"]
)


@router.get("")
def get_all_stock(
    connection=Depends(get_db)
):
    stock_service = InventarioStockService(
        connection
    )

    return stock_service.get_all_stock()


@router.get("/por-insumo/{insumo_id}")
def get_stock_by_insumo_id(
    insumo_id: int,
    connection=Depends(get_db)
):
    stock_service = InventarioStockService(
        connection
    )

    return stock_service.get_stock_by_insumo_id(
        insumo_id
    )


@router.put("/{stock_id}/producto")
def update_product_and_stock(
    stock_id: int,
    update_data: InventarioProductoStockUpdate,
    connection=Depends(get_db)
):
    stock_service = InventarioStockService(
        connection
    )

    return (
        stock_service.update_product_and_stock(
            stock_id,
            update_data.model_dump()
        )
    )


@router.put("/{stock_id}/estado")
def update_product_status(
    stock_id: int,
    status_data: InventarioProductoEstadoUpdate,
    connection=Depends(get_db)
):
    stock_service = InventarioStockService(
        connection
    )

    return (
        stock_service.update_product_status(
            stock_id,
            status_data.estado
        )
    )


@router.get("/{stock_id}")
def get_stock(
    stock_id: int,
    connection=Depends(get_db)
):
    stock_service = InventarioStockService(
        connection
    )

    return stock_service.get_stock_by_id(
        stock_id
    )