from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import MetodoPagoCreate, MetodoPagoUpdate
from backend.services.metodo_pago_service import MetodoPagoService


router = APIRouter(
    prefix="/metodos-pago",
    tags=["Métodos de Pago"]
)


@router.get("")
def get_metodos_pago(connection=Depends(get_db)):
    metodo_pago_service = MetodoPagoService(connection)

    return metodo_pago_service.get_all_metodos_pago()


@router.get("/{metodo_pago_id}")
def get_metodo_pago(metodo_pago_id: int, connection=Depends(get_db)):
    metodo_pago_service = MetodoPagoService(connection)

    return metodo_pago_service.get_metodo_pago_by_id(metodo_pago_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_metodo_pago(
    metodo_pago: MetodoPagoCreate,
    connection=Depends(get_db)
):
    metodo_pago_service = MetodoPagoService(connection)

    metodo_pago_data = metodo_pago.model_dump()

    return metodo_pago_service.create_metodo_pago(metodo_pago_data)


@router.put("/{metodo_pago_id}")
def update_metodo_pago(
    metodo_pago_id: int,
    metodo_pago: MetodoPagoUpdate,
    connection=Depends(get_db)
):
    metodo_pago_service = MetodoPagoService(connection)

    metodo_pago_data = metodo_pago.model_dump(exclude_unset=True)

    return metodo_pago_service.update_metodo_pago(
        metodo_pago_id,
        metodo_pago_data
    )


@router.delete("/{metodo_pago_id}")
def delete_metodo_pago(metodo_pago_id: int, connection=Depends(get_db)):
    metodo_pago_service = MetodoPagoService(connection)

    return metodo_pago_service.delete_metodo_pago(metodo_pago_id)