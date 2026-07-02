import oracledb
from fastapi import HTTPException, status

from backend.core.logger import get_logger
from backend.repositories.doctor_repository import DoctorRepository
from backend.repositories.horario_doctor_repository import HorarioDoctorRepository


logger = get_logger("horarios_doctores")


def schema_to_dict(schema):
    if hasattr(schema, "model_dump"):
        return schema.model_dump(exclude_unset=True)

    return schema.dict(exclude_unset=True)


class HorarioDoctorService:

    def __init__(self, connection):
        self.repository = HorarioDoctorRepository(connection)
        self.doctor_repository = DoctorRepository(connection)

    def raise_database_error(self, error: Exception):
        logger.exception("Database error in horarios_doctores: %s", str(error))

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

    def get_by_id(self, horario_id: int):
        try:
            horario = self.repository.get_by_id(horario_id)

            if horario is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Horario de doctor no encontrado."
                )

            return horario

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
            horario_id = self.repository.create(data)

            logger.info("Horario de doctor creado con ID %s", horario_id)

            return self.repository.get_by_id(horario_id)

        except oracledb.Error as error:
            self.raise_database_error(error)

    def update(self, horario_id: int, data):
        existing = self.get_by_id(horario_id)
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
                horario_id,
                update_fields
            )

            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Horario de doctor no encontrado."
                )

            logger.info("Horario de doctor actualizado con ID %s", horario_id)

            return self.repository.get_by_id(horario_id)

        except oracledb.Error as error:
            self.raise_database_error(error)

    def delete(self, horario_id: int):
        self.get_by_id(horario_id)

        try:
            deleted = self.repository.delete(horario_id)

            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Horario de doctor no encontrado."
                )

            logger.info("Horario de doctor eliminado con ID %s", horario_id)

            return {
                "message": "Horario de doctor eliminado correctamente."
            }

        except oracledb.Error as error:
            self.raise_database_error(error)