from fastapi import HTTPException, status

from backend.repositories.tratamiento_repository import TratamientoRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el tratamiento porque ya existe un valor único repetido."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el tratamiento porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class TratamientoService:

    def __init__(self, connection):
        self.connection = connection
        self.tratamiento_repository = TratamientoRepository(connection)

    def get_all_tratamientos(self):
        try:
            return self.tratamiento_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_tratamiento_by_id(self, tratamiento_id: int):
        try:
            tratamiento = self.tratamiento_repository.get_by_id(tratamiento_id)

            if tratamiento is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tratamiento no encontrado."
                )

            return tratamiento

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_tratamiento(self, tratamiento_data: dict):
        try:
            tratamiento = self.tratamiento_repository.create(tratamiento_data)

            self.connection.commit()

            return tratamiento

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_tratamiento(self, tratamiento_id: int, tratamiento_data: dict):
        try:
            current_tratamiento = self.tratamiento_repository.get_by_id(tratamiento_id)

            if current_tratamiento is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tratamiento no encontrado."
                )

            if len(tratamiento_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            updated_tratamiento = self.tratamiento_repository.update(
                tratamiento_id,
                tratamiento_data
            )

            self.connection.commit()

            return updated_tratamiento

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_tratamiento(self, tratamiento_id: int):
        try:
            current_tratamiento = self.tratamiento_repository.get_by_id(tratamiento_id)

            if current_tratamiento is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tratamiento no encontrado."
                )

            self.tratamiento_repository.delete(tratamiento_id)

            self.connection.commit()

            return {
                "message": "Tratamiento eliminado correctamente.",
                "tratamiento_id": tratamiento_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)