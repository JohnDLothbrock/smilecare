from fastapi import HTTPException, status

from backend.repositories.paciente_repository import PacienteRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el paciente porque existe un valor único repetido."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el paciente porque una llave foránea no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el paciente porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class PacienteService:

    def __init__(self, connection):
        self.connection = connection
        self.paciente_repository = PacienteRepository(connection)

    def get_all_pacientes(self):
        try:
            return self.paciente_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_paciente_by_id(self, paciente_id: int):
        try:
            paciente = self.paciente_repository.get_by_id(paciente_id)

            if paciente is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paciente no encontrado."
                )

            return paciente

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_paciente(self, paciente_data: dict):
        try:
            paciente = self.paciente_repository.create(paciente_data)

            self.connection.commit()

            return paciente

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_paciente(self, paciente_id: int, paciente_data: dict):
        try:
            current_paciente = self.paciente_repository.get_by_id(paciente_id)

            if current_paciente is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paciente no encontrado."
                )

            if len(paciente_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            updated_paciente = self.paciente_repository.update(
                paciente_id,
                paciente_data
            )

            self.connection.commit()

            return updated_paciente

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_paciente(self, paciente_id: int):
        try:
            current_paciente = self.paciente_repository.get_by_id(paciente_id)

            if current_paciente is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paciente no encontrado."
                )

            self.paciente_repository.delete(paciente_id)

            self.connection.commit()

            return {
                "message": "Paciente eliminado correctamente.",
                "paciente_id": paciente_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)