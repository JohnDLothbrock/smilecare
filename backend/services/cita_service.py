from fastapi import HTTPException, status

from backend.repositories.cita_repository import CitaRepository
from backend.repositories.doctor_repository import DoctorRepository
from backend.repositories.paciente_repository import PacienteRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la cita porque existe un valor único repetido."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la cita porque una llave foránea no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la cita porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class CitaService:

    def __init__(self, connection):
        self.connection = connection
        self.cita_repository = CitaRepository(connection)
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

    def get_all_citas(self):
        try:
            return self.cita_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_cita_by_id(self, cita_id: int):
        try:
            cita = self.cita_repository.get_by_id(cita_id)

            if cita is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cita no encontrada."
                )

            return cita

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_cita(self, cita_data: dict):
        try:
            self.validate_paciente_exists(cita_data["paciente_id"])
            self.validate_doctor_exists(cita_data["doctor_id"])

            cita = self.cita_repository.create(cita_data)

            self.connection.commit()

            return cita

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_cita(self, cita_id: int, cita_data: dict):
        try:
            current_cita = self.cita_repository.get_by_id(cita_id)

            if current_cita is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cita no encontrada."
                )

            if len(cita_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "paciente_id" in cita_data:
                self.validate_paciente_exists(cita_data["paciente_id"])

            if "doctor_id" in cita_data:
                self.validate_doctor_exists(cita_data["doctor_id"])

            updated_cita = self.cita_repository.update(
                cita_id,
                cita_data
            )

            self.connection.commit()

            return updated_cita

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_cita(self, cita_id: int):
        try:
            current_cita = self.cita_repository.get_by_id(cita_id)

            if current_cita is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cita no encontrada."
                )

            self.cita_repository.delete(cita_id)

            self.connection.commit()

            return {
                "message": "Cita eliminada correctamente.",
                "cita_id": cita_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)