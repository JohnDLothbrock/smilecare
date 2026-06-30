from fastapi import HTTPException, status

from backend.repositories.insumo_repository import InsumoRepository
from backend.repositories.inventario_stock_repository import (
    InventarioStockRepository
)


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el stock porque este insumo ya tiene un registro de inventario."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el stock porque el insumo indicado no existe."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class InventarioStockService:

    def __init__(self, connection):
        self.connection = connection
        self.stock_repository = InventarioStockRepository(connection)
        self.insumo_repository = InsumoRepository(connection)

    def validate_insumo_exists(self, insumo_id: int):
        insumo = self.insumo_repository.get_by_id(insumo_id)

        if insumo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El insumo indicado no existe."
            )

    def validate_insumo_without_stock(self, insumo_id: int):
        stock = self.stock_repository.get_by_insumo_id(insumo_id)

        if stock is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El insumo indicado ya tiene un registro de stock."
            )

    def get_all_stock(self):
        try:
            return self.stock_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_stock_by_id(self, stock_id: int):
        try:
            stock = self.stock_repository.get_by_id(stock_id)

            if stock is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de stock no encontrado."
                )

            return stock

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_stock_by_insumo_id(self, insumo_id: int):
        try:
            self.validate_insumo_exists(insumo_id)

            stock = self.stock_repository.get_by_insumo_id(insumo_id)

            if stock is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Este insumo no tiene registro de stock."
                )

            return stock

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_stock(self, stock_data: dict):
        try:
            insumo_id = stock_data["insumo_id"]

            self.validate_insumo_exists(insumo_id)
            self.validate_insumo_without_stock(insumo_id)

            stock = self.stock_repository.create(stock_data)

            self.connection.commit()

            return stock

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_stock(self, stock_id: int, stock_data: dict):
        try:
            current_stock = self.stock_repository.get_by_id(stock_id)

            if current_stock is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de stock no encontrado."
                )

            if len(stock_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "insumo_id" in stock_data:
                new_insumo_id = stock_data["insumo_id"]

                self.validate_insumo_exists(new_insumo_id)

                existing_stock = self.stock_repository.get_by_insumo_id(
                    new_insumo_id
                )

                if (
                    existing_stock is not None
                    and existing_stock["stock_id"] != stock_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="El insumo indicado ya tiene un registro de stock."
                    )

            updated_stock = self.stock_repository.update(stock_id, stock_data)

            self.connection.commit()

            return updated_stock

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_stock(self, stock_id: int):
        try:
            current_stock = self.stock_repository.get_by_id(stock_id)

            if current_stock is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de stock no encontrado."
                )

            self.stock_repository.delete(stock_id)

            self.connection.commit()

            return {
                "message": "Registro de stock eliminado correctamente.",
                "stock_id": stock_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)