from fastapi import HTTPException, status

from backend.repositories.detalle_factura_repository import (
    DetalleFacturaRepository
)
from backend.repositories.factura_repository import FacturaRepository
from backend.repositories.tratamiento_consulta_repository import (
    TratamientoConsultaRepository
)


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el detalle de factura porque existe un valor único repetido."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el detalle porque una llave foránea no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el detalle porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class DetalleFacturaService:

    def __init__(self, connection):
        self.connection = connection
        self.detalle_factura_repository = DetalleFacturaRepository(connection)
        self.factura_repository = FacturaRepository(connection)
        self.tratamiento_consulta_repository = TratamientoConsultaRepository(
            connection
        )

    def validate_factura_exists(self, factura_id: int):
        factura = self.factura_repository.get_by_id(factura_id)

        if factura is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La factura indicada no existe."
            )

        return factura

    def validate_tratamiento_consulta_exists(self, tratamiento_consulta_id: int):
        tratamiento_consulta = self.tratamiento_consulta_repository.get_by_id(
            tratamiento_consulta_id
        )

        if tratamiento_consulta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El tratamiento de consulta indicado no existe."
            )

        return tratamiento_consulta

    def calculate_subtotal(self, cantidad, precio_unitario):
        return round(float(cantidad) * float(precio_unitario), 2)

    def prepare_create_data(self, detalle_factura_data: dict) -> dict:
        self.validate_factura_exists(detalle_factura_data["factura_id"])

        tratamiento_consulta = None

        if detalle_factura_data.get("tratamiento_consulta_id") is not None:
            tratamiento_consulta = self.validate_tratamiento_consulta_exists(
                detalle_factura_data["tratamiento_consulta_id"]
            )

        if detalle_factura_data.get("descripcion") is None:
            if tratamiento_consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Debe indicar una descripción si no usa un tratamiento de consulta."
                )

            detalle_factura_data["descripcion"] = tratamiento_consulta[
                "tratamiento_nombre"
            ]

        if detalle_factura_data.get("precio_unitario") is None:
            if tratamiento_consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Debe indicar un precio unitario si no usa un tratamiento de consulta."
                )

            detalle_factura_data["precio_unitario"] = tratamiento_consulta[
                "precio_unitario"
            ]

        detalle_factura_data["subtotal"] = self.calculate_subtotal(
            detalle_factura_data["cantidad"],
            detalle_factura_data["precio_unitario"]
        )

        return detalle_factura_data

    def prepare_update_data(
        self,
        current_detalle: dict,
        detalle_factura_data: dict
    ) -> dict:
        if "factura_id" in detalle_factura_data:
            self.validate_factura_exists(detalle_factura_data["factura_id"])

        tratamiento_consulta = None

        if "tratamiento_consulta_id" in detalle_factura_data:
            if detalle_factura_data["tratamiento_consulta_id"] is not None:
                tratamiento_consulta = self.validate_tratamiento_consulta_exists(
                    detalle_factura_data["tratamiento_consulta_id"]
                )

        if (
            detalle_factura_data.get("descripcion") is None
            and "tratamiento_consulta_id" in detalle_factura_data
            and tratamiento_consulta is not None
        ):
            detalle_factura_data["descripcion"] = tratamiento_consulta[
                "tratamiento_nombre"
            ]

        if (
            detalle_factura_data.get("precio_unitario") is None
            and "tratamiento_consulta_id" in detalle_factura_data
            and tratamiento_consulta is not None
        ):
            detalle_factura_data["precio_unitario"] = tratamiento_consulta[
                "precio_unitario"
            ]

        cantidad = detalle_factura_data.get(
            "cantidad",
            current_detalle["cantidad"]
        )

        precio_unitario = detalle_factura_data.get(
            "precio_unitario",
            current_detalle["precio_unitario"]
        )

        if (
            "cantidad" in detalle_factura_data
            or "precio_unitario" in detalle_factura_data
            or "tratamiento_consulta_id" in detalle_factura_data
        ):
            detalle_factura_data["subtotal"] = self.calculate_subtotal(
                cantidad,
                precio_unitario
            )

        return detalle_factura_data

    def get_all_detalles_factura(self):
        try:
            return self.detalle_factura_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_detalle_factura_by_id(self, detalle_factura_id: int):
        try:
            detalle_factura = self.detalle_factura_repository.get_by_id(
                detalle_factura_id
            )

            if detalle_factura is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Detalle de factura no encontrado."
                )

            return detalle_factura

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_detalles_by_factura_id(self, factura_id: int):
        try:
            self.validate_factura_exists(factura_id)

            return self.detalle_factura_repository.get_by_factura_id(factura_id)

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_detalle_factura(self, detalle_factura_data: dict):
        try:
            detalle_factura_data = self.prepare_create_data(
                detalle_factura_data
            )

            detalle_factura = self.detalle_factura_repository.create(
                detalle_factura_data
            )

            self.factura_repository.recalculate_totals_from_details(
                detalle_factura_data["factura_id"]
            )

            self.connection.commit()

            return detalle_factura

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_detalle_factura(
        self,
        detalle_factura_id: int,
        detalle_factura_data: dict
    ):
        try:
            current_detalle = self.detalle_factura_repository.get_by_id(
                detalle_factura_id
            )

            if current_detalle is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Detalle de factura no encontrado."
                )

            if len(detalle_factura_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            old_factura_id = current_detalle["factura_id"]

            detalle_factura_data = self.prepare_update_data(
                current_detalle,
                detalle_factura_data
            )

            updated_detalle = self.detalle_factura_repository.update(
                detalle_factura_id,
                detalle_factura_data
            )

            new_factura_id = updated_detalle["factura_id"]

            self.factura_repository.recalculate_totals_from_details(
                old_factura_id
            )

            if new_factura_id != old_factura_id:
                self.factura_repository.recalculate_totals_from_details(
                    new_factura_id
                )

            self.connection.commit()

            return updated_detalle

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_detalle_factura(self, detalle_factura_id: int):
        try:
            current_detalle = self.detalle_factura_repository.get_by_id(
                detalle_factura_id
            )

            if current_detalle is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Detalle de factura no encontrado."
                )

            factura_id = current_detalle["factura_id"]

            self.detalle_factura_repository.delete(detalle_factura_id)

            self.factura_repository.recalculate_totals_from_details(factura_id)

            self.connection.commit()

            return {
                "message": "Detalle de factura eliminado correctamente.",
                "detalle_factura_id": detalle_factura_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)