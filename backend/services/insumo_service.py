from fastapi import HTTPException, status

from backend.repositories.insumo_repository import InsumoRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el insumo porque el código ya existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el insumo porque tiene stock, compras o movimientos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class InsumoService:

    def __init__(self, connection):
        self.connection = connection
        self.insumo_repository = InsumoRepository(connection)

    def get_all_insumos(self):
        try:
            return self.insumo_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_insumo_by_id(self, insumo_id: int):
        try:
            insumo = self.insumo_repository.get_by_id(insumo_id)

            if insumo is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Insumo no encontrado."
                )

            return insumo

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_insumo(self, insumo_data: dict):
        try:
            insumo = self.insumo_repository.create(insumo_data)

            self.connection.commit()

            return insumo

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_insumo(self, insumo_id: int, insumo_data: dict):
        try:
            current_insumo = self.insumo_repository.get_by_id(insumo_id)

            if current_insumo is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Insumo no encontrado."
                )

            if len(insumo_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            updated_insumo = self.insumo_repository.update(
                insumo_id,
                insumo_data
            )

            self.connection.commit()

            return updated_insumo

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_insumo(self, insumo_id: int):
        try:
            current_insumo = self.insumo_repository.get_by_id(insumo_id)

            if current_insumo is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Insumo no encontrado."
                )

            self.insumo_repository.delete(insumo_id)

            self.connection.commit()

            return {
                "message": "Insumo eliminado correctamente.",
                "insumo_id": insumo_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)