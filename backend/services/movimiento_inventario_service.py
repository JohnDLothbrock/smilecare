from fastapi import HTTPException, status

from backend.repositories.consulta_repository import ConsultaRepository
from backend.repositories.detalle_compra_repository import DetalleCompraRepository
from backend.repositories.insumo_repository import InsumoRepository
from backend.repositories.inventario_stock_repository import (
    InventarioStockRepository
)
from backend.repositories.movimiento_inventario_repository import (
    MovimientoInventarioRepository
)


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-02290" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el movimiento porque el tipo o la cantidad no cumplen las reglas."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el movimiento porque una llave foránea no existe."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class MovimientoInventarioService:

    def __init__(self, connection):
        self.connection = connection
        self.movimiento_repository = MovimientoInventarioRepository(connection)
        self.insumo_repository = InsumoRepository(connection)
        self.stock_repository = InventarioStockRepository(connection)
        self.detalle_compra_repository = DetalleCompraRepository(connection)
        self.consulta_repository = ConsultaRepository(connection)

    def validate_usuario_exists(self, usuario_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT usuario_id
                FROM usuarios
                WHERE usuario_id = :usuario_id
                """,
                {
                    "usuario_id": usuario_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El usuario indicado no existe."
                )

        finally:
            cursor.close()

    def validate_insumo_exists(self, insumo_id: int):
        insumo = self.insumo_repository.get_by_id(insumo_id)

        if insumo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El insumo indicado no existe."
            )

    def validate_stock_exists(self, insumo_id: int) -> dict:
        stock = self.stock_repository.get_by_insumo_id(insumo_id)

        if stock is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El insumo indicado no tiene registro en inventario stock."
            )

        return stock

    def validate_detalle_compra_exists(self, detalle_compra_id: int):
        detalle_compra = self.detalle_compra_repository.get_by_id(
            detalle_compra_id
        )

        if detalle_compra is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El detalle de compra indicado no existe."
            )

    def validate_consulta_exists(self, consulta_id: int):
        consulta = self.consulta_repository.get_by_id(consulta_id)

        if consulta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La consulta indicada no existe."
            )

    def validate_optional_references(self, movimiento_data: dict):
        if movimiento_data.get("detalle_compra_id") is not None:
            self.validate_detalle_compra_exists(
                movimiento_data["detalle_compra_id"]
            )

        if movimiento_data.get("consulta_id") is not None:
            self.validate_consulta_exists(
                movimiento_data["consulta_id"]
            )

    def calculate_new_stock(self, stock_actual: float, tipo_movimiento: str, cantidad: float):
        stock_actual = float(stock_actual)
        cantidad = float(cantidad)

        if tipo_movimiento == "ENTRADA":
            return round(stock_actual + cantidad, 2)

        if tipo_movimiento == "SALIDA":
            new_stock = round(stock_actual - cantidad, 2)

            if new_stock < 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="No hay suficiente stock para registrar la salida."
                )

            return new_stock

        if tipo_movimiento == "AJUSTE":
            return round(cantidad, 2)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de movimiento inválido. Use ENTRADA, SALIDA o AJUSTE."
        )

    def calculate_reverse_stock(
        self,
        stock_actual: float,
        tipo_movimiento: str,
        cantidad: float
    ):
        stock_actual = float(stock_actual)
        cantidad = float(cantidad)

        if tipo_movimiento == "ENTRADA":
            new_stock = round(stock_actual - cantidad, 2)

            if new_stock < 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="No se puede eliminar esta entrada porque dejaría el stock en negativo."
                )

            return new_stock

        if tipo_movimiento == "SALIDA":
            return round(stock_actual + cantidad, 2)

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un movimiento de tipo AJUSTE porque no se conoce el stock anterior."
        )

    def apply_stock_change(self, movimiento_data: dict):
        stock = self.validate_stock_exists(movimiento_data["insumo_id"])

        new_stock = self.calculate_new_stock(
            stock["stock_actual"],
            movimiento_data["tipo_movimiento"],
            movimiento_data["cantidad"]
        )

        self.movimiento_repository.update_stock_actual(
            movimiento_data["insumo_id"],
            new_stock
        )

    def reverse_stock_change(self, movimiento_data: dict):
        stock = self.validate_stock_exists(movimiento_data["insumo_id"])

        new_stock = self.calculate_reverse_stock(
            stock["stock_actual"],
            movimiento_data["tipo_movimiento"],
            movimiento_data["cantidad"]
        )

        self.movimiento_repository.update_stock_actual(
            movimiento_data["insumo_id"],
            new_stock
        )

    def get_all_movimientos(self):
        try:
            return self.movimiento_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_movimiento_by_id(self, movimiento_id: int):
        try:
            movimiento = self.movimiento_repository.get_by_id(movimiento_id)

            if movimiento is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Movimiento de inventario no encontrado."
                )

            return movimiento

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_movimientos_by_insumo_id(self, insumo_id: int):
        try:
            self.validate_insumo_exists(insumo_id)

            return self.movimiento_repository.get_by_insumo_id(insumo_id)

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_movimiento(self, movimiento_data: dict):
        try:
            self.validate_insumo_exists(movimiento_data["insumo_id"])
            self.validate_usuario_exists(movimiento_data["usuario_id"])
            self.validate_optional_references(movimiento_data)

            self.apply_stock_change(movimiento_data)

            movimiento = self.movimiento_repository.create(movimiento_data)

            self.connection.commit()

            return movimiento

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_movimiento(self, movimiento_id: int, movimiento_data: dict):
        try:
            current_movimiento = self.movimiento_repository.get_by_id(
                movimiento_id
            )

            if current_movimiento is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Movimiento de inventario no encontrado."
                )

            if len(movimiento_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "usuario_id" in movimiento_data:
                self.validate_usuario_exists(movimiento_data["usuario_id"])

            self.validate_optional_references(movimiento_data)

            updated_movimiento = self.movimiento_repository.update(
                movimiento_id,
                movimiento_data
            )

            self.connection.commit()

            return updated_movimiento

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_movimiento(self, movimiento_id: int):
        try:
            current_movimiento = self.movimiento_repository.get_by_id(
                movimiento_id
            )

            if current_movimiento is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Movimiento de inventario no encontrado."
                )

            self.reverse_stock_change(current_movimiento)

            self.movimiento_repository.delete(movimiento_id)

            self.connection.commit()

            return {
                "message": "Movimiento de inventario eliminado correctamente.",
                "movimiento_id": movimiento_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)