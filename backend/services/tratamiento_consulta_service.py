from fastapi import HTTPException, status

from backend.repositories.consulta_repository import ConsultaRepository
from backend.repositories.tratamiento_consulta_repository import (
    TratamientoConsultaRepository
)
from backend.repositories.tratamiento_repository import TratamientoRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el tratamiento de consulta porque existe un valor único repetido."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el tratamiento de consulta porque una llave foránea no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el tratamiento de consulta porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class TratamientoConsultaService:

    def __init__(self, connection):
        self.connection = connection
        self.tratamiento_consulta_repository = TratamientoConsultaRepository(connection)
        self.consulta_repository = ConsultaRepository(connection)
        self.tratamiento_repository = TratamientoRepository(connection)

    def validate_consulta_exists(self, consulta_id: int):
        consulta = self.consulta_repository.get_by_id(consulta_id)

        if consulta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La consulta indicada no existe."
            )

    def validate_tratamiento_exists(self, tratamiento_id: int):
        tratamiento = self.tratamiento_repository.get_by_id(tratamiento_id)

        if tratamiento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El tratamiento indicado no existe."
            )

        return tratamiento

    def calculate_subtotal(self, cantidad, precio_unitario):
        return round(float(cantidad) * float(precio_unitario), 2)

    def prepare_create_data(self, tratamiento_consulta_data: dict) -> dict:
        self.validate_consulta_exists(tratamiento_consulta_data["consulta_id"])

        tratamiento = self.validate_tratamiento_exists(
            tratamiento_consulta_data["tratamiento_id"]
        )

        if tratamiento_consulta_data.get("precio_unitario") is None:
            tratamiento_consulta_data["precio_unitario"] = tratamiento["costo_base"]

        tratamiento_consulta_data["subtotal"] = self.calculate_subtotal(
            tratamiento_consulta_data["cantidad"],
            tratamiento_consulta_data["precio_unitario"]
        )

        return tratamiento_consulta_data

    def prepare_update_data(
        self,
        current_data: dict,
        tratamiento_consulta_data: dict
    ) -> dict:
        if "consulta_id" in tratamiento_consulta_data:
            self.validate_consulta_exists(tratamiento_consulta_data["consulta_id"])

        if "tratamiento_id" in tratamiento_consulta_data:
            tratamiento = self.validate_tratamiento_exists(
                tratamiento_consulta_data["tratamiento_id"]
            )

            if "precio_unitario" not in tratamiento_consulta_data:
                tratamiento_consulta_data["precio_unitario"] = tratamiento["costo_base"]

        cantidad = tratamiento_consulta_data.get(
            "cantidad",
            current_data["cantidad"]
        )

        precio_unitario = tratamiento_consulta_data.get(
            "precio_unitario",
            current_data["precio_unitario"]
        )

        if (
            "cantidad" in tratamiento_consulta_data
            or "precio_unitario" in tratamiento_consulta_data
            or "tratamiento_id" in tratamiento_consulta_data
        ):
            tratamiento_consulta_data["subtotal"] = self.calculate_subtotal(
                cantidad,
                precio_unitario
            )

        return tratamiento_consulta_data

    def get_all_tratamientos_consulta(self):
        try:
            return self.tratamiento_consulta_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_tratamiento_consulta_by_id(self, tratamiento_consulta_id: int):
        try:
            tratamiento_consulta = self.tratamiento_consulta_repository.get_by_id(
                tratamiento_consulta_id
            )

            if tratamiento_consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tratamiento de consulta no encontrado."
                )

            return tratamiento_consulta

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_tratamientos_by_consulta_id(self, consulta_id: int):
        try:
            self.validate_consulta_exists(consulta_id)

            return self.tratamiento_consulta_repository.get_by_consulta_id(
                consulta_id
            )

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_tratamiento_consulta(self, tratamiento_consulta_data: dict):
        try:
            tratamiento_consulta_data = self.prepare_create_data(
                tratamiento_consulta_data
            )

            tratamiento_consulta = self.tratamiento_consulta_repository.create(
                tratamiento_consulta_data
            )

            self.connection.commit()

            return tratamiento_consulta

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_tratamiento_consulta(
        self,
        tratamiento_consulta_id: int,
        tratamiento_consulta_data: dict
    ):
        try:
            current_tratamiento_consulta = (
                self.tratamiento_consulta_repository.get_by_id(
                    tratamiento_consulta_id
                )
            )

            if current_tratamiento_consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tratamiento de consulta no encontrado."
                )

            if len(tratamiento_consulta_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            tratamiento_consulta_data = self.prepare_update_data(
                current_tratamiento_consulta,
                tratamiento_consulta_data
            )

            updated_tratamiento_consulta = (
                self.tratamiento_consulta_repository.update(
                    tratamiento_consulta_id,
                    tratamiento_consulta_data
                )
            )

            self.connection.commit()

            return updated_tratamiento_consulta

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_tratamiento_consulta(self, tratamiento_consulta_id: int):
        try:
            current_tratamiento_consulta = (
                self.tratamiento_consulta_repository.get_by_id(
                    tratamiento_consulta_id
                )
            )

            if current_tratamiento_consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tratamiento de consulta no encontrado."
                )

            self.tratamiento_consulta_repository.delete(tratamiento_consulta_id)

            self.connection.commit()

            return {
                "message": "Tratamiento de consulta eliminado correctamente.",
                "tratamiento_consulta_id": tratamiento_consulta_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)