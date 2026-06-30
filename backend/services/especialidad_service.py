from fastapi import HTTPException, status

from backend.repositories.especialidad_repository import EspecialidadRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la especialidad porque ya existe un valor único repetido."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la especialidad porque tiene doctores relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class EspecialidadService:

    def __init__(self, connection):
        self.connection = connection
        self.especialidad_repository = EspecialidadRepository(connection)

    def get_all_especialidades(self):
        try:
            return self.especialidad_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_especialidad_by_id(self, especialidad_id: int):
        try:
            especialidad = self.especialidad_repository.get_by_id(especialidad_id)

            if especialidad is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Especialidad no encontrada."
                )

            return especialidad

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_especialidad(self, especialidad_data: dict):
        try:
            especialidad = self.especialidad_repository.create(especialidad_data)

            self.connection.commit()

            return especialidad

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_especialidad(self, especialidad_id: int, especialidad_data: dict):
        try:
            current_especialidad = self.especialidad_repository.get_by_id(especialidad_id)

            if current_especialidad is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Especialidad no encontrada."
                )

            if len(especialidad_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            updated_especialidad = self.especialidad_repository.update(
                especialidad_id,
                especialidad_data
            )

            self.connection.commit()

            return updated_especialidad

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_especialidad(self, especialidad_id: int):
        try:
            current_especialidad = self.especialidad_repository.get_by_id(especialidad_id)

            if current_especialidad is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Especialidad no encontrada."
                )

            self.especialidad_repository.delete(especialidad_id)

            self.connection.commit()

            return {
                "message": "Especialidad eliminada correctamente.",
                "especialidad_id": especialidad_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)