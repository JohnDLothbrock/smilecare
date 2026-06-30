from fastapi import HTTPException, status

from backend.repositories.comprobante_repository import ComprobanteRepository
from backend.repositories.pago_repository import PagoRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el comprobante porque el pago o el número de comprobante ya están registrados."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el comprobante porque el pago indicado no existe."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class ComprobanteService:

    def __init__(self, connection):
        self.connection = connection
        self.comprobante_repository = ComprobanteRepository(connection)
        self.pago_repository = PagoRepository(connection)

    def validate_pago_exists(self, pago_id: int):
        pago = self.pago_repository.get_by_id(pago_id)

        if pago is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El pago indicado no existe."
            )

        return pago

    def validate_pago_without_comprobante(self, pago_id: int):
        comprobante = self.comprobante_repository.get_by_pago_id(pago_id)

        if comprobante is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El pago indicado ya tiene un comprobante registrado."
            )

    def get_all_comprobantes(self):
        try:
            return self.comprobante_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_comprobante_by_id(self, comprobante_id: int):
        try:
            comprobante = self.comprobante_repository.get_by_id(comprobante_id)

            if comprobante is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comprobante no encontrado."
                )

            return comprobante

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_comprobante_by_pago_id(self, pago_id: int):
        try:
            self.validate_pago_exists(pago_id)

            comprobante = self.comprobante_repository.get_by_pago_id(pago_id)

            if comprobante is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No existe un comprobante para este pago."
                )

            return comprobante

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_comprobante(self, comprobante_data: dict):
        try:
            pago_id = comprobante_data["pago_id"]

            self.validate_pago_exists(pago_id)
            self.validate_pago_without_comprobante(pago_id)

            comprobante = self.comprobante_repository.create(comprobante_data)

            self.connection.commit()

            return comprobante

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_comprobante(self, comprobante_id: int, comprobante_data: dict):
        try:
            current_comprobante = self.comprobante_repository.get_by_id(
                comprobante_id
            )

            if current_comprobante is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comprobante no encontrado."
                )

            if len(comprobante_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            if "pago_id" in comprobante_data:
                new_pago_id = comprobante_data["pago_id"]

                self.validate_pago_exists(new_pago_id)

                existing_comprobante = (
                    self.comprobante_repository.get_by_pago_id(new_pago_id)
                )

                if (
                    existing_comprobante is not None
                    and existing_comprobante["comprobante_id"] != comprobante_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="El pago indicado ya tiene un comprobante registrado."
                    )

            updated_comprobante = self.comprobante_repository.update(
                comprobante_id,
                comprobante_data
            )

            self.connection.commit()

            return updated_comprobante

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_comprobante(self, comprobante_id: int):
        try:
            current_comprobante = self.comprobante_repository.get_by_id(
                comprobante_id
            )

            if current_comprobante is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comprobante no encontrado."
                )

            self.comprobante_repository.delete(comprobante_id)

            self.connection.commit()

            return {
                "message": "Comprobante eliminado correctamente.",
                "comprobante_id": comprobante_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)