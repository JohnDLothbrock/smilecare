from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class NuevoInsumoWorkflowCreate(BaseModel):
    codigo: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: Optional[str] = Field(
        default=None,
        max_length=300
    )
    unidad_medida: str = Field(
        min_length=1,
        max_length=30
    )
    estado: str = Field(
        default="ACTIVO",
        min_length=1,
        max_length=20
    )


class CompraItemWorkflowCreate(BaseModel):
    insumo_id: Optional[int] = None

    nuevo_insumo: Optional[
        NuevoInsumoWorkflowCreate
    ] = None

    cantidad: float = Field(gt=0)

    costo_unitario: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_product_source(self):
        has_existing_product = (
            self.insumo_id is not None
        )

        has_new_product = (
            self.nuevo_insumo is not None
        )

        if (
            not has_existing_product
            and not has_new_product
        ):
            raise ValueError(
                "Debe seleccionar un insumo existente "
                "o registrar uno nuevo."
            )

        if (
            has_existing_product
            and has_new_product
        ):
            raise ValueError(
                "No puede enviar un insumo existente "
                "y uno nuevo al mismo tiempo."
            )

        return self


class CompraWorkflowCreate(BaseModel):
    proveedor_id: int

    usuario_id: int

    fecha_compra: Optional[date] = None

    items: list[
        CompraItemWorkflowCreate
    ] = Field(min_length=1)


class InventarioProductoStockUpdate(BaseModel):
    codigo: str = Field(
        min_length=1,
        max_length=50
    )

    nombre: str = Field(
        min_length=1,
        max_length=100
    )

    descripcion: Optional[str] = Field(
        default=None,
        max_length=300
    )

    stock_minimo: Optional[float] = Field(
        default=None,
        ge=0
    )

    ubicacion: Optional[str] = Field(
        default=None,
        max_length=100
    )


class InventarioProductoEstadoUpdate(BaseModel):
    estado: str = Field(
        pattern="^(ACTIVO|INACTIVO)$"
    )