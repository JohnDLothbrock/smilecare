from fastapi import HTTPException, status

from backend.repositories.doctor_repository import DoctorRepository
from backend.repositories.especialidad_repository import EspecialidadRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el doctor porque ya existe un valor único repetido."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el doctor porque una llave foránea no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el doctor porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class DoctorService:

    def __init__(self, connection):
        self.connection = connection
        self.doctor_repository = DoctorRepository(connection)
        self.especialidad_repository = EspecialidadRepository(connection)

    def validate_especialidad_exists(self, especialidad_id: int):
        especialidad = self.especialidad_repository.get_by_id(especialidad_id)

        if especialidad is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La especialidad indicada no existe."
            )

    def get_all_doctores(self):
        try:
            return self.doctor_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_doctor_by_id(self, doctor_id: int):
        try:
            doctor = self.doctor_repository.get_by_id(doctor_id)

            if doctor is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor no encontrado."
                )

            return doctor

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_doctor(self, doctor_data: dict):
        try:
            self.validate_especialidad_exists(doctor_data["especialidad_id"])

            doctor = self.doctor_repository.create(doctor_data)

            self.connection.commit()

            return doctor

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_doctor(self, doctor_id: int, doctor_data: dict):
        try:
            current_doctor = self.doctor_repository.get_by_id(doctor_id)

            if current_doctor is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor no encontrado."
                )

            if len(doctor_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "especialidad_id" in doctor_data:
                self.validate_especialidad_exists(doctor_data["especialidad_id"])

            updated_doctor = self.doctor_repository.update(
                doctor_id,
                doctor_data
            )

            self.connection.commit()

            return updated_doctor

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_doctor(self, doctor_id: int):
        try:
            current_doctor = self.doctor_repository.get_by_id(doctor_id)

            if current_doctor is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor no encontrado."
                )

            self.doctor_repository.delete(doctor_id)

            self.connection.commit()

            return {
                "message": "Doctor eliminado correctamente.",
                "doctor_id": doctor_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)