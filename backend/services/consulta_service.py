from fastapi import HTTPException, status

from backend.repositories.cita_repository import CitaRepository
from backend.repositories.consulta_repository import ConsultaRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la consulta porque esta cita ya tiene una consulta registrada."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la consulta porque la cita indicada no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la consulta porque tiene datos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class ConsultaService:

    def __init__(self, connection):
        self.connection = connection
        self.consulta_repository = ConsultaRepository(connection)
        self.cita_repository = CitaRepository(connection)

    def validate_cita_exists(self, cita_id: int):
        cita = self.cita_repository.get_by_id(cita_id)

        if cita is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La cita indicada no existe."
            )

    def validate_cita_without_consulta(self, cita_id: int):
        consulta = self.consulta_repository.get_by_cita_id(cita_id)

        if consulta is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La cita indicada ya tiene una consulta registrada."
            )

    def get_all_consultas(self):
        try:
            return self.consulta_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_consulta_by_id(self, consulta_id: int):
        try:
            consulta = self.consulta_repository.get_by_id(consulta_id)

            if consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Consulta no encontrada."
                )

            return consulta

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_consulta_by_cita_id(self, cita_id: int):
        try:
            consulta = self.consulta_repository.get_by_cita_id(cita_id)

            if consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No existe una consulta registrada para esta cita."
                )

            return consulta

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_consulta(self, consulta_data: dict):
        try:
            cita_id = consulta_data["cita_id"]

            self.validate_cita_exists(cita_id)
            self.validate_cita_without_consulta(cita_id)

            consulta = self.consulta_repository.create(consulta_data)

            self.connection.commit()

            return consulta

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_consulta(self, consulta_id: int, consulta_data: dict):
        try:
            current_consulta = self.consulta_repository.get_by_id(consulta_id)

            if current_consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Consulta no encontrada."
                )

            if len(consulta_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "cita_id" in consulta_data:
                new_cita_id = consulta_data["cita_id"]

                self.validate_cita_exists(new_cita_id)

                existing_consulta = self.consulta_repository.get_by_cita_id(new_cita_id)

                if (
                    existing_consulta is not None
                    and existing_consulta["consulta_id"] != consulta_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="La cita indicada ya tiene una consulta registrada."
                    )

            updated_consulta = self.consulta_repository.update(
                consulta_id,
                consulta_data
            )

            self.connection.commit()

            return updated_consulta

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_consulta(self, consulta_id: int):
        try:
            current_consulta = self.consulta_repository.get_by_id(consulta_id)

            if current_consulta is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Consulta no encontrada."
                )

            self.consulta_repository.delete(consulta_id)

            self.connection.commit()

            return {
                "message": "Consulta eliminada correctamente.",
                "consulta_id": consulta_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)