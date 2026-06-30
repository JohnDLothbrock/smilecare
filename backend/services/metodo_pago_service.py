from fastapi import HTTPException, status

from backend.repositories.metodo_pago_repository import MetodoPagoRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el método de pago porque ya existe un nombre repetido."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el método de pago porque tiene pagos relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class MetodoPagoService:

    def __init__(self, connection):
        self.connection = connection
        self.metodo_pago_repository = MetodoPagoRepository(connection)

    def get_all_metodos_pago(self):
        try:
            return self.metodo_pago_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_metodo_pago_by_id(self, metodo_pago_id: int):
        try:
            metodo_pago = self.metodo_pago_repository.get_by_id(metodo_pago_id)

            if metodo_pago is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Método de pago no encontrado."
                )

            return metodo_pago

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_metodo_pago(self, metodo_pago_data: dict):
        try:
            metodo_pago = self.metodo_pago_repository.create(metodo_pago_data)

            self.connection.commit()

            return metodo_pago

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_metodo_pago(self, metodo_pago_id: int, metodo_pago_data: dict):
        try:
            current_metodo_pago = self.metodo_pago_repository.get_by_id(
                metodo_pago_id
            )

            if current_metodo_pago is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Método de pago no encontrado."
                )

            if len(metodo_pago_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            updated_metodo_pago = self.metodo_pago_repository.update(
                metodo_pago_id,
                metodo_pago_data
            )

            self.connection.commit()

            return updated_metodo_pago

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_metodo_pago(self, metodo_pago_id: int):
        try:
            current_metodo_pago = self.metodo_pago_repository.get_by_id(
                metodo_pago_id
            )

            if current_metodo_pago is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Método de pago no encontrado."
                )

            self.metodo_pago_repository.delete(metodo_pago_id)

            self.connection.commit()

            return {
                "message": "Método de pago eliminado correctamente.",
                "metodo_pago_id": metodo_pago_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)