from fastapi import HTTPException, status

from backend.repositories.compra_repository import CompraRepository
from backend.repositories.detalle_compra_repository import DetalleCompraRepository
from backend.repositories.insumo_repository import InsumoRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el detalle porque la compra o insumo indicado no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el detalle porque tiene movimientos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class DetalleCompraService:

    def __init__(self, connection):
        self.connection = connection
        self.detalle_compra_repository = DetalleCompraRepository(connection)
        self.compra_repository = CompraRepository(connection)
        self.insumo_repository = InsumoRepository(connection)

    def validate_compra_exists(self, compra_id: int):
        compra = self.compra_repository.get_by_id(compra_id)

        if compra is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La compra indicada no existe."
            )

    def validate_insumo_exists(self, insumo_id: int):
        insumo = self.insumo_repository.get_by_id(insumo_id)

        if insumo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El insumo indicado no existe."
            )

    def calculate_subtotal(self, cantidad, costo_unitario):
        return round(float(cantidad) * float(costo_unitario), 2)

    def prepare_create_data(self, detalle_compra_data: dict) -> dict:
        self.validate_compra_exists(detalle_compra_data["compra_id"])
        self.validate_insumo_exists(detalle_compra_data["insumo_id"])

        detalle_compra_data["subtotal"] = self.calculate_subtotal(
            detalle_compra_data["cantidad"],
            detalle_compra_data["costo_unitario"]
        )

        return detalle_compra_data

    def prepare_update_data(
        self,
        current_detalle: dict,
        detalle_compra_data: dict
    ) -> dict:
        if "compra_id" in detalle_compra_data:
            self.validate_compra_exists(detalle_compra_data["compra_id"])

        if "insumo_id" in detalle_compra_data:
            self.validate_insumo_exists(detalle_compra_data["insumo_id"])

        cantidad = detalle_compra_data.get(
            "cantidad",
            current_detalle["cantidad"]
        )

        costo_unitario = detalle_compra_data.get(
            "costo_unitario",
            current_detalle["costo_unitario"]
        )

        if (
            "cantidad" in detalle_compra_data
            or "costo_unitario" in detalle_compra_data
        ):
            detalle_compra_data["subtotal"] = self.calculate_subtotal(
                cantidad,
                costo_unitario
            )

        return detalle_compra_data

    def get_all_detalles_compra(self):
        try:
            return self.detalle_compra_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_detalle_compra_by_id(self, detalle_compra_id: int):
        try:
            detalle = self.detalle_compra_repository.get_by_id(
                detalle_compra_id
            )

            if detalle is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Detalle de compra no encontrado."
                )

            return detalle

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_detalles_by_compra_id(self, compra_id: int):
        try:
            self.validate_compra_exists(compra_id)

            return self.detalle_compra_repository.get_by_compra_id(compra_id)

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_detalle_compra(self, detalle_compra_data: dict):
        try:
            detalle_compra_data = self.prepare_create_data(
                detalle_compra_data
            )

            detalle = self.detalle_compra_repository.create(
                detalle_compra_data
            )

            self.compra_repository.recalculate_total_from_details(
                detalle_compra_data["compra_id"]
            )

            self.connection.commit()

            return detalle

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_detalle_compra(
        self,
        detalle_compra_id: int,
        detalle_compra_data: dict
    ):
        try:
            current_detalle = self.detalle_compra_repository.get_by_id(
                detalle_compra_id
            )

            if current_detalle is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Detalle de compra no encontrado."
                )

            if len(detalle_compra_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            old_compra_id = current_detalle["compra_id"]

            detalle_compra_data = self.prepare_update_data(
                current_detalle,
                detalle_compra_data
            )

            updated_detalle = self.detalle_compra_repository.update(
                detalle_compra_id,
                detalle_compra_data
            )

            new_compra_id = updated_detalle["compra_id"]

            self.compra_repository.recalculate_total_from_details(
                old_compra_id
            )

            if new_compra_id != old_compra_id:
                self.compra_repository.recalculate_total_from_details(
                    new_compra_id
                )

            self.connection.commit()

            return updated_detalle

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_detalle_compra(self, detalle_compra_id: int):
        try:
            current_detalle = self.detalle_compra_repository.get_by_id(
                detalle_compra_id
            )

            if current_detalle is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Detalle de compra no encontrado."
                )

            compra_id = current_detalle["compra_id"]

            self.detalle_compra_repository.delete(detalle_compra_id)

            self.compra_repository.recalculate_total_from_details(compra_id)

            self.connection.commit()

            return {
                "message": "Detalle de compra eliminado correctamente.",
                "detalle_compra_id": detalle_compra_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)