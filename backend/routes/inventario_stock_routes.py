from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import InventarioStockCreate, InventarioStockUpdate
from backend.services.inventario_stock_service import InventarioStockService


router = APIRouter(
    prefix="/inventario-stock",
    tags=["Inventario Stock"]
)


@router.get("")
def get_all_stock(connection=Depends(get_db)):
    stock_service = InventarioStockService(connection)

    return stock_service.get_all_stock()


@router.get("/por-insumo/{insumo_id}")
def get_stock_by_insumo_id(
    insumo_id: int,
    connection=Depends(get_db)
):
    stock_service = InventarioStockService(connection)

    return stock_service.get_stock_by_insumo_id(insumo_id)


@router.get("/{stock_id}")
def get_stock(stock_id: int, connection=Depends(get_db)):
    stock_service = InventarioStockService(connection)

    return stock_service.get_stock_by_id(stock_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_stock(
    stock: InventarioStockCreate,
    connection=Depends(get_db)
):
    stock_service = InventarioStockService(connection)

    stock_data = stock.model_dump()

    return stock_service.create_stock(stock_data)


@router.put("/{stock_id}")
def update_stock(
    stock_id: int,
    stock: InventarioStockUpdate,
    connection=Depends(get_db)
):
    stock_service = InventarioStockService(connection)

    stock_data = stock.model_dump(exclude_unset=True)

    return stock_service.update_stock(
        stock_id,
        stock_data
    )


@router.delete("/{stock_id}")
def delete_stock(stock_id: int, connection=Depends(get_db)):
    stock_service = InventarioStockService(connection)

    return stock_service.delete_stock(stock_id)