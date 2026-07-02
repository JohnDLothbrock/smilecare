import oracledb
from fastapi import HTTPException, status

from backend.core.logger import get_logger
from backend.repositories.disponibilidad_doctor_repository import (
    DisponibilidadDoctorRepository
)
from backend.repositories.doctor_repository import DoctorRepository


logger = get_logger("disponibilidad_doctores")


def schema_to_dict(schema):
    if hasattr(schema, "model_dump"):
        return schema.model_dump(exclude_unset=True)

    return schema.dict(exclude_unset=True)


class DisponibilidadDoctorService:

    def __init__(self, connection):
        self.repository = DisponibilidadDoctorRepository(connection)
        self.doctor_repository = DoctorRepository(connection)

    def raise_database_error(self, error: Exception):
        logger.exception(
            "Database error in disponibilidad_doctores: %s",
            str(error)
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos: {str(error)}"
        )

    def validate_doctor_exists(self, doctor_id: int):
        doctor = self.doctor_repository.get_by_id(doctor_id)

        if doctor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El doctor indicado no existe."
            )

    def validate_hours(self, hora_inicio: str, hora_fin: str):
        if hora_inicio >= hora_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora de inicio debe ser menor que la hora de fin."
            )

    def get_all(self):
        try:
            return self.repository.get_all()

        except oracledb.Error as error:
            self.raise_database_error(error)

    def get_by_id(self, disponibilidad_id: int):
        try:
            disponibilidad = self.repository.get_by_id(disponibilidad_id)

            if disponibilidad is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Disponibilidad de doctor no encontrada."
                )

            return disponibilidad

        except oracledb.Error as error:
            self.raise_database_error(error)

    def get_by_doctor_id(self, doctor_id: int):
        self.validate_doctor_exists(doctor_id)

        try:
            return self.repository.get_by_doctor_id(doctor_id)

        except oracledb.Error as error:
            self.raise_database_error(error)

    def create(self, data):
        self.validate_doctor_exists(data.doctor_id)
        self.validate_hours(data.hora_inicio, data.hora_fin)

        try:
            disponibilidad_id = self.repository.create(data)

            logger.info(
                "Disponibilidad de doctor creada con ID %s",
                disponibilidad_id
            )

            return self.repository.get_by_id(disponibilidad_id)

        except oracledb.Error as error:
            self.raise_database_error(error)

    def update(self, disponibilidad_id: int, data):
        existing = self.get_by_id(disponibilidad_id)
        update_fields = schema_to_dict(data)

        merged = {
            **existing,
            **update_fields
        }

        if "doctor_id" in update_fields:
            self.validate_doctor_exists(update_fields["doctor_id"])

        self.validate_hours(
            merged["hora_inicio"],
            merged["hora_fin"]
        )

        try:
            updated = self.repository.update(
                disponibilidad_id,
                update_fields
            )

            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Disponibilidad de doctor no encontrada."
                )

            logger.info(
                "Disponibilidad de doctor actualizada con ID %s",
                disponibilidad_id
            )

            return self.repository.get_by_id(disponibilidad_id)

        except oracledb.Error as error:
            self.raise_database_error(error)

    def delete(self, disponibilidad_id: int):
        self.get_by_id(disponibilidad_id)

        try:
            deleted = self.repository.delete(disponibilidad_id)

            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Disponibilidad de doctor no encontrada."
                )

            logger.info(
                "Disponibilidad de doctor eliminada con ID %s",
                disponibilidad_id
            )

            return {
                "message": "Disponibilidad de doctor eliminada correctamente."
            }

        except oracledb.Error as error:
            self.raise_database_error(error)