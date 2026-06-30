from fastapi import HTTPException, status

from backend.repositories.cirugia_repository import CirugiaRepository
from backend.repositories.doctor_repository import DoctorRepository
from backend.repositories.tratamiento_consulta_repository import (
    TratamientoConsultaRepository
)


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la cirugía porque el tratamiento de consulta ya tiene una cirugía registrada."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la cirugía porque una llave foránea no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la cirugía porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class CirugiaService:

    def __init__(self, connection):
        self.connection = connection
        self.cirugia_repository = CirugiaRepository(connection)
        self.tratamiento_consulta_repository = TratamientoConsultaRepository(
            connection
        )
        self.doctor_repository = DoctorRepository(connection)

    def validate_tratamiento_consulta_exists(self, tratamiento_consulta_id: int):
        tratamiento_consulta = self.tratamiento_consulta_repository.get_by_id(
            tratamiento_consulta_id
        )

        if tratamiento_consulta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El tratamiento de consulta indicado no existe."
            )

    def validate_doctor_exists(self, doctor_id: int):
        doctor = self.doctor_repository.get_by_id(doctor_id)

        if doctor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El doctor indicado no existe."
            )

    def validate_tratamiento_without_cirugia(
        self,
        tratamiento_consulta_id: int
    ):
        cirugia = self.cirugia_repository.get_by_tratamiento_consulta_id(
            tratamiento_consulta_id
        )

        if cirugia is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El tratamiento de consulta indicado ya tiene una cirugía registrada."
            )

    def get_all_cirugias(self):
        try:
            return self.cirugia_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_cirugia_by_id(self, cirugia_id: int):
        try:
            cirugia = self.cirugia_repository.get_by_id(cirugia_id)

            if cirugia is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cirugía no encontrada."
                )

            return cirugia

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_cirugia_by_tratamiento_consulta_id(
        self,
        tratamiento_consulta_id: int
    ):
        try:
            self.validate_tratamiento_consulta_exists(tratamiento_consulta_id)

            cirugia = self.cirugia_repository.get_by_tratamiento_consulta_id(
                tratamiento_consulta_id
            )

            if cirugia is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No existe una cirugía para este tratamiento de consulta."
                )

            return cirugia

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_cirugia(self, cirugia_data: dict):
        try:
            tratamiento_consulta_id = cirugia_data["tratamiento_consulta_id"]

            self.validate_tratamiento_consulta_exists(tratamiento_consulta_id)
            self.validate_doctor_exists(cirugia_data["doctor_id"])
            self.validate_tratamiento_without_cirugia(tratamiento_consulta_id)

            cirugia = self.cirugia_repository.create(cirugia_data)

            self.connection.commit()

            return cirugia

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_cirugia(self, cirugia_id: int, cirugia_data: dict):
        try:
            current_cirugia = self.cirugia_repository.get_by_id(cirugia_id)

            if current_cirugia is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cirugía no encontrada."
                )

            if len(cirugia_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "tratamiento_consulta_id" in cirugia_data:
                new_tratamiento_consulta_id = cirugia_data[
                    "tratamiento_consulta_id"
                ]

                self.validate_tratamiento_consulta_exists(
                    new_tratamiento_consulta_id
                )

                existing_cirugia = (
                    self.cirugia_repository.get_by_tratamiento_consulta_id(
                        new_tratamiento_consulta_id
                    )
                )

                if (
                    existing_cirugia is not None
                    and existing_cirugia["cirugia_id"] != cirugia_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="El tratamiento de consulta indicado ya tiene una cirugía registrada."
                    )

            if "doctor_id" in cirugia_data:
                self.validate_doctor_exists(cirugia_data["doctor_id"])

            updated_cirugia = self.cirugia_repository.update(
                cirugia_id,
                cirugia_data
            )

            self.connection.commit()

            return updated_cirugia

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_cirugia(self, cirugia_id: int):
        try:
            current_cirugia = self.cirugia_repository.get_by_id(cirugia_id)

            if current_cirugia is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cirugía no encontrada."
                )

            self.cirugia_repository.delete(cirugia_id)

            self.connection.commit()

            return {
                "message": "Cirugía eliminada correctamente.",
                "cirugia_id": cirugia_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)