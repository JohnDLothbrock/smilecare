from fastapi import HTTPException, status

from backend.repositories.insumo_repository import (
    InsumoRepository
)
from backend.repositories.inventario_stock_repository import (
    InventarioStockRepository
)


DISCRETE_UNITS = {
    "UNIDAD",
    "CAJA",
    "PAQUETE"
}

ALLOWED_UNITS = {
    "UNIDAD",
    "CAJA",
    "PAQUETE",
    "ML",
    "GRAMOS"
}


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo guardar la información. "
                "Verifique que el código del producto "
                "no esté siendo utilizado por otro insumo."
            )
        )

    if "ORA-02290" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo guardar la información porque "
                "uno de los valores no cumple las reglas "
                "de la base de datos."
            )
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo guardar la información porque "
                "uno de los registros relacionados no existe."
            )
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class InventarioStockService:

    def __init__(self, connection):
        self.connection = connection

        self.stock_repository = (
            InventarioStockRepository(
                connection
            )
        )

        self.insumo_repository = (
            InsumoRepository(
                connection
            )
        )

    def validate_insumo_exists(
        self,
        insumo_id: int
    ) -> dict:
        insumo = (
            self.insumo_repository.get_by_id(
                insumo_id
            )
        )

        if insumo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "El producto indicado no existe."
                )
            )

        return insumo

    def validate_stock_exists(
        self,
        stock_id: int
    ) -> dict:
        stock = (
            self.stock_repository.get_by_id(
                stock_id
            )
        )

        if stock is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Registro de stock no encontrado."
                )
            )

        return stock

    def validate_unit(
        self,
        unidad_medida: str
    ):
        normalized_unit = str(
            unidad_medida or ""
        ).upper()

        if normalized_unit not in ALLOWED_UNITS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "La unidad de medida del producto "
                    "no es válida."
                )
            )

    def validate_quantity_for_unit(
        self,
        cantidad,
        unidad_medida: str,
        field_name: str
    ):
        if cantidad is None:
            return

        quantity = float(
            cantidad
        )

        normalized_unit = str(
            unidad_medida or ""
        ).upper()

        self.validate_unit(
            normalized_unit
        )

        if quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"{field_name} no puede ser negativo."
                )
            )

        if (
            normalized_unit in DISCRETE_UNITS
            and not quantity.is_integer()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"{field_name} debe ser un número "
                    f"entero porque la unidad de medida "
                    f"es {normalized_unit}."
                )
            )

    def get_all_stock(self):
        try:
            return (
                self.stock_repository.get_all()
            )

        except Exception as error:
            raise_database_error(error)

    def get_stock_by_id(
        self,
        stock_id: int
    ):
        try:
            return self.validate_stock_exists(
                stock_id
            )

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_stock_by_insumo_id(
        self,
        insumo_id: int
    ):
        try:
            self.validate_insumo_exists(
                insumo_id
            )

            stock = (
                self.stock_repository
                .get_by_insumo_id(
                    insumo_id
                )
            )

            if stock is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        "Este producto no tiene "
                        "registro de stock."
                    )
                )

            return stock

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def update_product_and_stock(
        self,
        stock_id: int,
        update_data: dict
    ):
        try:
            current_stock = (
                self.validate_stock_exists(
                    stock_id
                )
            )

            insumo_id = current_stock[
                "insumo_id"
            ]

            current_insumo = (
                self.validate_insumo_exists(
                    insumo_id
                )
            )

            codigo = str(
                update_data["codigo"]
            ).strip()

            nombre = str(
                update_data["nombre"]
            ).strip()

            descripcion = update_data.get(
                "descripcion"
            )

            ubicacion = update_data.get(
                "ubicacion"
            )

            if not codigo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "El código del producto "
                        "es obligatorio."
                    )
                )

            if not nombre:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "El nombre del producto "
                        "es obligatorio."
                    )
                )

            if descripcion is not None:
                descripcion = str(
                    descripcion
                ).strip() or None

            if ubicacion is not None:
                ubicacion = str(
                    ubicacion
                ).strip() or None

            stock_minimo = update_data.get(
                "stock_minimo"
            )

            self.validate_quantity_for_unit(
                stock_minimo,
                current_insumo["unidad_medida"],
                "El stock mínimo"
            )

            insumo_update = {
                "codigo": codigo,
                "nombre": nombre,
                "descripcion": descripcion
            }

            stock_update = {
                "stock_minimo": stock_minimo,
                "ubicacion": ubicacion
            }

            updated_insumo = (
                self.insumo_repository.update(
                    insumo_id,
                    insumo_update
                )
            )

            updated_stock = (
                self.stock_repository.update(
                    stock_id,
                    stock_update
                )
            )

            self.connection.commit()

            return {
                "message": (
                    "Producto e información de inventario "
                    "actualizados correctamente."
                ),
                "insumo": updated_insumo,
                "stock": updated_stock
            }

        except HTTPException:
            self.connection.rollback()
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_product_status(
        self,
        stock_id: int,
        estado: str
    ):
        try:
            current_stock = (
                self.validate_stock_exists(
                    stock_id
                )
            )

            insumo_id = current_stock[
                "insumo_id"
            ]

            current_insumo = (
                self.validate_insumo_exists(
                    insumo_id
                )
            )

            normalized_status = str(
                estado
            ).upper()

            if normalized_status not in {
                "ACTIVO",
                "INACTIVO"
            }:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Estado inválido. "
                        "Use ACTIVO o INACTIVO."
                    )
                )

            if (
                current_insumo["estado"]
                == normalized_status
            ):
                return {
                    "message": (
                        "El producto ya se encuentra "
                        f"en estado {normalized_status}."
                    ),
                    "insumo": current_insumo,
                    "stock": current_stock
                }

            updated_insumo = (
                self.insumo_repository.update(
                    insumo_id,
                    {
                        "estado":
                            normalized_status
                    }
                )
            )

            self.connection.commit()

            action_message = (
                "reactivado"
                if normalized_status == "ACTIVO"
                else "desactivado"
            )

            return {
                "message": (
                    f"Producto {action_message} "
                    "correctamente."
                ),
                "insumo": updated_insumo,
                "stock":
                    self.stock_repository.get_by_id(
                        stock_id
                    )
            }

        except HTTPException:
            self.connection.rollback()
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)