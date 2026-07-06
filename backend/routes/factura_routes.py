from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import FacturaCreate, FacturaUpdate
from backend.services.factura_service import FacturaService


router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)


@router.get("")
def get_facturas(connection=Depends(get_db)):
    factura_service = FacturaService(connection)

    return factura_service.get_all_facturas()


@router.get("/por-paciente/{paciente_id}")
def get_facturas_by_paciente_id(
    paciente_id: int,
    connection=Depends(get_db)
):
    factura_service = FacturaService(connection)

    return factura_service.get_facturas_by_paciente_id(paciente_id)


@router.get("/por-consulta/{consulta_id}")
def get_factura_by_consulta_id(
    consulta_id: int,
    connection=Depends(get_db)
):
    factura_service = FacturaService(connection)

    return factura_service.get_factura_by_consulta_id(consulta_id)


@router.get("/{factura_id}")
def get_factura(factura_id: int, connection=Depends(get_db)):
    factura_service = FacturaService(connection)

    return factura_service.get_factura_by_id(factura_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_factura(
    factura: FacturaCreate,
    connection=Depends(get_db)
):
    factura_service = FacturaService(connection)

    factura_data = factura.model_dump()

    return factura_service.create_factura(factura_data)


@router.put("/{factura_id}")
def update_factura(
    factura_id: int,
    factura: FacturaUpdate,
    connection=Depends(get_db)
):
    factura_service = FacturaService(connection)

    factura_data = factura.model_dump(exclude_unset=True)

    return factura_service.update_factura(
        factura_id,
        factura_data
    )


@router.put("/{factura_id}/restaurar")
def restore_factura(factura_id: int, connection=Depends(get_db)):
    factura_service = FacturaService(connection)

    return factura_service.restore_factura(factura_id)


@router.delete("/{factura_id}")
def delete_factura(factura_id: int, connection=Depends(get_db)):
    factura_service = FacturaService(connection)

    return factura_service.delete_factura(factura_id)