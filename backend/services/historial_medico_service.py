from fastapi import HTTPException, status

from backend.repositories.doctor_repository import DoctorRepository
from backend.repositories.historial_medico_repository import (
    HistorialMedicoRepository
)
from backend.repositories.paciente_repository import PacienteRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el historial porque el paciente o doctor indicado no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el historial porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class HistorialMedicoService:

    def __init__(self, connection):
        self.connection = connection
        self.historial_medico_repository = HistorialMedicoRepository(connection)
        self.paciente_repository = PacienteRepository(connection)
        self.doctor_repository = DoctorRepository(connection)

    def validate_paciente_exists(self, paciente_id: int):
        paciente = self.paciente_repository.get_by_id(paciente_id)

        if paciente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El paciente indicado no existe."
            )

    def validate_doctor_exists(self, doctor_id: int):
        doctor = self.doctor_repository.get_by_id(doctor_id)

        if doctor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El doctor indicado no existe."
            )

    def get_all_historiales(self):
        try:
            return self.historial_medico_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_historial_by_id(self, historial_id: int):
        try:
            historial = self.historial_medico_repository.get_by_id(historial_id)

            if historial is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historial médico no encontrado."
                )

            return historial

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_historiales_by_paciente_id(self, paciente_id: int):
        try:
            self.validate_paciente_exists(paciente_id)

            return self.historial_medico_repository.get_by_paciente_id(
                paciente_id
            )

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_historial(self, historial_data: dict):
        try:
            self.validate_paciente_exists(historial_data["paciente_id"])
            self.validate_doctor_exists(historial_data["doctor_id"])

            historial = self.historial_medico_repository.create(historial_data)

            self.connection.commit()

            return historial

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_historial(self, historial_id: int, historial_data: dict):
        try:
            current_historial = self.historial_medico_repository.get_by_id(
                historial_id
            )

            if current_historial is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historial médico no encontrado."
                )

            if len(historial_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "paciente_id" in historial_data:
                self.validate_paciente_exists(historial_data["paciente_id"])

            if "doctor_id" in historial_data:
                self.validate_doctor_exists(historial_data["doctor_id"])

            updated_historial = self.historial_medico_repository.update(
                historial_id,
                historial_data
            )

            self.connection.commit()

            return updated_historial

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_historial(self, historial_id: int):
        try:
            current_historial = self.historial_medico_repository.get_by_id(
                historial_id
            )

            if current_historial is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historial médico no encontrado."
                )

            self.historial_medico_repository.delete(historial_id)

            self.connection.commit()

            return {
                "message": "Historial médico eliminado correctamente.",
                "historial_id": historial_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)