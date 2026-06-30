from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import ComprobanteCreate, ComprobanteUpdate
from backend.services.comprobante_service import ComprobanteService


router = APIRouter(
    prefix="/comprobantes",
    tags=["Comprobantes"]
)


@router.get("")
def get_comprobantes(connection=Depends(get_db)):
    comprobante_service = ComprobanteService(connection)

    return comprobante_service.get_all_comprobantes()


@router.get("/por-pago/{pago_id}")
def get_comprobante_by_pago_id(
    pago_id: int,
    connection=Depends(get_db)
):
    comprobante_service = ComprobanteService(connection)

    return comprobante_service.get_comprobante_by_pago_id(pago_id)


@router.get("/{comprobante_id}")
def get_comprobante(comprobante_id: int, connection=Depends(get_db)):
    comprobante_service = ComprobanteService(connection)

    return comprobante_service.get_comprobante_by_id(comprobante_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_comprobante(
    comprobante: ComprobanteCreate,
    connection=Depends(get_db)
):
    comprobante_service = ComprobanteService(connection)

    comprobante_data = comprobante.model_dump()

    return comprobante_service.create_comprobante(comprobante_data)


@router.put("/{comprobante_id}")
def update_comprobante(
    comprobante_id: int,
    comprobante: ComprobanteUpdate,
    connection=Depends(get_db)
):
    comprobante_service = ComprobanteService(connection)

    comprobante_data = comprobante.model_dump(exclude_unset=True)

    return comprobante_service.update_comprobante(
        comprobante_id,
        comprobante_data
    )


@router.delete("/{comprobante_id}")
def delete_comprobante(
    comprobante_id: int,
    connection=Depends(get_db)
):
    comprobante_service = ComprobanteService(connection)

    return comprobante_service.delete_comprobante(comprobante_id)