from fastapi import HTTPException, status

from backend.repositories.proveedor_repository import ProveedorRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el proveedor porque tiene compras relacionadas."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class ProveedorService:

    def __init__(self, connection):
        self.connection = connection
        self.proveedor_repository = ProveedorRepository(connection)

    def get_all_proveedores(self):
        try:
            return self.proveedor_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_proveedor_by_id(self, proveedor_id: int):
        try:
            proveedor = self.proveedor_repository.get_by_id(proveedor_id)

            if proveedor is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Proveedor no encontrado."
                )

            return proveedor

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_proveedor(self, proveedor_data: dict):
        try:
            proveedor = self.proveedor_repository.create(proveedor_data)

            self.connection.commit()

            return proveedor

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_proveedor(self, proveedor_id: int, proveedor_data: dict):
        try:
            current_proveedor = self.proveedor_repository.get_by_id(proveedor_id)

            if current_proveedor is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Proveedor no encontrado."
                )

            if len(proveedor_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            updated_proveedor = self.proveedor_repository.update(
                proveedor_id,
                proveedor_data
            )

            self.connection.commit()

            return updated_proveedor

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_proveedor(self, proveedor_id: int):
        try:
            current_proveedor = self.proveedor_repository.get_by_id(proveedor_id)

            if current_proveedor is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Proveedor no encontrado."
                )

            self.proveedor_repository.delete(proveedor_id)

            self.connection.commit()

            return {
                "message": "Proveedor eliminado correctamente.",
                "proveedor_id": proveedor_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)