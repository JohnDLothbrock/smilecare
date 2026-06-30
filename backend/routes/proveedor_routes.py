from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import ProveedorCreate, ProveedorUpdate
from backend.services.proveedor_service import ProveedorService


router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"]
)


@router.get("")
def get_proveedores(connection=Depends(get_db)):
    proveedor_service = ProveedorService(connection)

    return proveedor_service.get_all_proveedores()


@router.get("/{proveedor_id}")
def get_proveedor(proveedor_id: int, connection=Depends(get_db)):
    proveedor_service = ProveedorService(connection)

    return proveedor_service.get_proveedor_by_id(proveedor_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_proveedor(
    proveedor: ProveedorCreate,
    connection=Depends(get_db)
):
    proveedor_service = ProveedorService(connection)

    proveedor_data = proveedor.model_dump()

    return proveedor_service.create_proveedor(proveedor_data)


@router.put("/{proveedor_id}")
def update_proveedor(
    proveedor_id: int,
    proveedor: ProveedorUpdate,
    connection=Depends(get_db)
):
    proveedor_service = ProveedorService(connection)

    proveedor_data = proveedor.model_dump(exclude_unset=True)

    return proveedor_service.update_proveedor(
        proveedor_id,
        proveedor_data
    )


@router.delete("/{proveedor_id}")
def delete_proveedor(proveedor_id: int, connection=Depends(get_db)):
    proveedor_service = ProveedorService(connection)

    return proveedor_service.delete_proveedor(proveedor_id)