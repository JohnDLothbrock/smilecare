from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import DetalleFacturaCreate, DetalleFacturaUpdate
from backend.services.detalle_factura_service import DetalleFacturaService


router = APIRouter(
    prefix="/detalle-factura",
    tags=["Detalle Factura"]
)


@router.get("")
def get_detalles_factura(connection=Depends(get_db)):
    detalle_factura_service = DetalleFacturaService(connection)

    return detalle_factura_service.get_all_detalles_factura()


@router.get("/por-factura/{factura_id}")
def get_detalles_by_factura_id(
    factura_id: int,
    connection=Depends(get_db)
):
    detalle_factura_service = DetalleFacturaService(connection)

    return detalle_factura_service.get_detalles_by_factura_id(factura_id)


@router.get("/{detalle_factura_id}")
def get_detalle_factura(
    detalle_factura_id: int,
    connection=Depends(get_db)
):
    detalle_factura_service = DetalleFacturaService(connection)

    return detalle_factura_service.get_detalle_factura_by_id(
        detalle_factura_id
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_detalle_factura(
    detalle_factura: DetalleFacturaCreate,
    connection=Depends(get_db)
):
    detalle_factura_service = DetalleFacturaService(connection)

    detalle_factura_data = detalle_factura.model_dump()

    return detalle_factura_service.create_detalle_factura(detalle_factura_data)


@router.put("/{detalle_factura_id}")
def update_detalle_factura(
    detalle_factura_id: int,
    detalle_factura: DetalleFacturaUpdate,
    connection=Depends(get_db)
):
    detalle_factura_service = DetalleFacturaService(connection)

    detalle_factura_data = detalle_factura.model_dump(exclude_unset=True)

    return detalle_factura_service.update_detalle_factura(
        detalle_factura_id,
        detalle_factura_data
    )


@router.delete("/{detalle_factura_id}")
def delete_detalle_factura(
    detalle_factura_id: int,
    connection=Depends(get_db)
):
    detalle_factura_service = DetalleFacturaService(connection)

    return detalle_factura_service.delete_detalle_factura(detalle_factura_id)