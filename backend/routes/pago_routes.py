from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import PagoCreate, PagoUpdate
from backend.services.pago_service import PagoService


router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"]
)


@router.get("")
def get_pagos(connection=Depends(get_db)):
    pago_service = PagoService(connection)

    return pago_service.get_all_pagos()


@router.get("/por-factura/{factura_id}")
def get_pagos_by_factura_id(
    factura_id: int,
    connection=Depends(get_db)
):
    pago_service = PagoService(connection)

    return pago_service.get_pagos_by_factura_id(factura_id)


@router.get("/{pago_id}")
def get_pago(pago_id: int, connection=Depends(get_db)):
    pago_service = PagoService(connection)

    return pago_service.get_pago_by_id(pago_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_pago(
    pago: PagoCreate,
    connection=Depends(get_db)
):
    pago_service = PagoService(connection)

    pago_data = pago.model_dump()

    return pago_service.create_pago(pago_data)


@router.put("/{pago_id}")
def update_pago(
    pago_id: int,
    pago: PagoUpdate,
    connection=Depends(get_db)
):
    pago_service = PagoService(connection)

    pago_data = pago.model_dump(exclude_unset=True)

    return pago_service.update_pago(
        pago_id,
        pago_data
    )


@router.delete("/{pago_id}")
def delete_pago(pago_id: int, connection=Depends(get_db)):
    pago_service = PagoService(connection)

    return pago_service.delete_pago(pago_id)