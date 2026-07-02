from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import DetalleCompraCreate, DetalleCompraUpdate
from backend.services.detalle_compra_service import DetalleCompraService


router = APIRouter(
    prefix="/detalle-compra",
    tags=["Detalle Compra"]
)


@router.get("")
def get_detalles_compra(connection=Depends(get_db)):
    detalle_compra_service = DetalleCompraService(connection)

    return detalle_compra_service.get_all_detalles_compra()


@router.get("/por-compra/{compra_id}")
def get_detalles_by_compra_id(
    compra_id: int,
    connection=Depends(get_db)
):
    detalle_compra_service = DetalleCompraService(connection)

    return detalle_compra_service.get_detalles_by_compra_id(compra_id)


@router.get("/{detalle_compra_id}")
def get_detalle_compra(
    detalle_compra_id: int,
    connection=Depends(get_db)
):
    detalle_compra_service = DetalleCompraService(connection)

    return detalle_compra_service.get_detalle_compra_by_id(
        detalle_compra_id
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_detalle_compra(
    detalle_compra: DetalleCompraCreate,
    connection=Depends(get_db)
):
    detalle_compra_service = DetalleCompraService(connection)

    detalle_compra_data = detalle_compra.model_dump()

    return detalle_compra_service.create_detalle_compra(detalle_compra_data)


@router.put("/{detalle_compra_id}")
def update_detalle_compra(
    detalle_compra_id: int,
    detalle_compra: DetalleCompraUpdate,
    connection=Depends(get_db)
):
    detalle_compra_service = DetalleCompraService(connection)

    detalle_compra_data = detalle_compra.model_dump(exclude_unset=True)

    return detalle_compra_service.update_detalle_compra(
        detalle_compra_id,
        detalle_compra_data
    )


@router.delete("/{detalle_compra_id}")
def delete_detalle_compra(
    detalle_compra_id: int,
    connection=Depends(get_db)
):
    detalle_compra_service = DetalleCompraService(connection)

    return detalle_compra_service.delete_detalle_compra(detalle_compra_id)