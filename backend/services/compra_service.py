from fastapi import HTTPException, status

from backend.repositories.compra_repository import CompraRepository
from backend.repositories.proveedor_repository import ProveedorRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la compra porque el proveedor o usuario indicado no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la compra porque tiene detalles relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class CompraService:

    def __init__(self, connection):
        self.connection = connection
        self.compra_repository = CompraRepository(connection)
        self.proveedor_repository = ProveedorRepository(connection)

    def validate_proveedor_exists(self, proveedor_id: int):
        proveedor = self.proveedor_repository.get_by_id(proveedor_id)

        if proveedor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El proveedor indicado no existe."
            )

    def validate_usuario_exists(self, usuario_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT usuario_id
                FROM usuarios
                WHERE usuario_id = :usuario_id
                """,
                {
                    "usuario_id": usuario_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El usuario indicado no existe."
                )

        finally:
            cursor.close()

    def get_all_compras(self):
        try:
            return self.compra_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_compra_by_id(self, compra_id: int):
        try:
            compra = self.compra_repository.get_by_id(compra_id)

            if compra is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Compra no encontrada."
                )

            return compra

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_compras_by_proveedor_id(self, proveedor_id: int):
        try:
            self.validate_proveedor_exists(proveedor_id)

            return self.compra_repository.get_by_proveedor_id(proveedor_id)

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_compra(self, compra_data: dict):
        try:
            self.validate_proveedor_exists(compra_data["proveedor_id"])
            self.validate_usuario_exists(compra_data["usuario_id"])

            if compra_data.get("total") is None:
                compra_data["total"] = 0

            compra = self.compra_repository.create(compra_data)

            self.connection.commit()

            return compra

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_compra(self, compra_id: int, compra_data: dict):
        try:
            current_compra = self.compra_repository.get_by_id(compra_id)

            if current_compra is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Compra no encontrada."
                )

            if len(compra_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "proveedor_id" in compra_data:
                self.validate_proveedor_exists(compra_data["proveedor_id"])

            if "usuario_id" in compra_data:
                self.validate_usuario_exists(compra_data["usuario_id"])

            updated_compra = self.compra_repository.update(
                compra_id,
                compra_data
            )

            self.connection.commit()

            return updated_compra

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_compra(self, compra_id: int):
        try:
            current_compra = self.compra_repository.get_by_id(compra_id)

            if current_compra is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Compra no encontrada."
                )

            self.compra_repository.delete(compra_id)

            self.connection.commit()

            return {
                "message": "Compra eliminada correctamente.",
                "compra_id": compra_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)