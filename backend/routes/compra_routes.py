from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import CompraCreate, CompraUpdate
from backend.services.compra_service import CompraService
from backend.workflow_schemas import CompraWorkflowCreate


router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)


@router.get("")
def get_compras(
    connection=Depends(get_db)
):
    compra_service = CompraService(connection)

    return compra_service.get_all_compras()


@router.get("/por-proveedor/{proveedor_id}")
def get_compras_by_proveedor_id(
    proveedor_id: int,
    connection=Depends(get_db)
):
    compra_service = CompraService(connection)

    return compra_service.get_compras_by_proveedor_id(
        proveedor_id
    )


@router.post(
    "/completa",
    status_code=status.HTTP_201_CREATED
)
def create_compra_completa(
    compra: CompraWorkflowCreate,
    connection=Depends(get_db)
):
    compra_service = CompraService(connection)

    compra_data = compra.model_dump()

    return compra_service.create_compra_completa(
        compra_data
    )


@router.get("/{compra_id}")
def get_compra(
    compra_id: int,
    connection=Depends(get_db)
):
    compra_service = CompraService(connection)

    return compra_service.get_compra_by_id(
        compra_id
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_compra(
    compra: CompraCreate,
    connection=Depends(get_db)
):
    compra_service = CompraService(connection)

    compra_data = compra.model_dump()

    return compra_service.create_compra(
        compra_data
    )


@router.put("/{compra_id}")
def update_compra(
    compra_id: int,
    compra: CompraUpdate,
    connection=Depends(get_db)
):
    compra_service = CompraService(connection)

    compra_data = compra.model_dump(
        exclude_unset=True
    )

    return compra_service.update_compra(
        compra_id,
        compra_data
    )


@router.delete("/{compra_id}")
def delete_compra(
    compra_id: int,
    connection=Depends(get_db)
):
    compra_service = CompraService(connection)

    return compra_service.delete_compra(
        compra_id
    )