from fastapi import HTTPException, status

from backend.repositories.factura_repository import FacturaRepository
from backend.repositories.metodo_pago_repository import MetodoPagoRepository
from backend.repositories.pago_repository import PagoRepository


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el pago porque existe un valor único repetido."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar el pago porque una llave foránea no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el pago porque tiene comprobantes relacionados."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class PagoService:

    def __init__(self, connection):
        self.connection = connection
        self.pago_repository = PagoRepository(connection)
        self.factura_repository = FacturaRepository(connection)
        self.metodo_pago_repository = MetodoPagoRepository(connection)

    def validate_factura_exists(self, factura_id: int):
        factura = self.factura_repository.get_by_id(factura_id)

        if factura is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La factura indicada no existe."
            )

        return factura

    def validate_metodo_pago_exists(self, metodo_pago_id: int):
        metodo_pago = self.metodo_pago_repository.get_by_id(metodo_pago_id)

        if metodo_pago is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El método de pago indicado no existe."
            )

        return metodo_pago

    def validate_payment_amount(
        self,
        factura_id: int,
        monto: float,
        exclude_pago_id=None
    ):
        factura = self.validate_factura_exists(factura_id)

        total_factura = float(factura["total"])
        total_pagado = self.pago_repository.get_total_paid_by_factura_id(
            factura_id,
            exclude_pago_id
        )

        nuevo_total_pagado = round(total_pagado + float(monto), 2)

        if nuevo_total_pagado > total_factura:
            saldo_disponible = round(total_factura - total_pagado, 2)

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "El monto del pago supera el saldo pendiente. "
                    f"Saldo disponible: {saldo_disponible}"
                )
            )

    def prepare_create_data(self, pago_data: dict) -> dict:
        self.validate_factura_exists(pago_data["factura_id"])
        self.validate_metodo_pago_exists(pago_data["metodo_pago_id"])

        self.validate_payment_amount(
            pago_data["factura_id"],
            pago_data["monto"]
        )

        return pago_data

    def prepare_update_data(self, current_pago: dict, pago_data: dict) -> dict:
        factura_id = pago_data.get(
            "factura_id",
            current_pago["factura_id"]
        )

        metodo_pago_id = pago_data.get(
            "metodo_pago_id",
            current_pago["metodo_pago_id"]
        )

        monto = pago_data.get(
            "monto",
            current_pago["monto"]
        )

        if "factura_id" in pago_data:
            self.validate_factura_exists(factura_id)

        if "metodo_pago_id" in pago_data:
            self.validate_metodo_pago_exists(metodo_pago_id)

        if "factura_id" in pago_data or "monto" in pago_data:
            self.validate_payment_amount(
                factura_id,
                monto,
                current_pago["pago_id"]
            )

        return pago_data

    def get_all_pagos(self):
        try:
            return self.pago_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_pago_by_id(self, pago_id: int):
        try:
            pago = self.pago_repository.get_by_id(pago_id)

            if pago is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pago no encontrado."
                )

            return pago

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_pagos_by_factura_id(self, factura_id: int):
        try:
            self.validate_factura_exists(factura_id)

            return self.pago_repository.get_by_factura_id(factura_id)

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_pago(self, pago_data: dict):
        try:
            pago_data = self.prepare_create_data(pago_data)

            pago = self.pago_repository.create(pago_data)

            self.connection.commit()

            return pago

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_pago(self, pago_id: int, pago_data: dict):
        try:
            current_pago = self.pago_repository.get_by_id(pago_id)

            if current_pago is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pago no encontrado."
                )

            if len(pago_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            pago_data = self.prepare_update_data(
                current_pago,
                pago_data
            )

            updated_pago = self.pago_repository.update(
                pago_id,
                pago_data
            )

            self.connection.commit()

            return updated_pago

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_pago(self, pago_id: int):
        try:
            current_pago = self.pago_repository.get_by_id(pago_id)

            if current_pago is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pago no encontrado."
                )

            self.pago_repository.delete(pago_id)

            self.connection.commit()

            return {
                "message": "Pago eliminado correctamente.",
                "pago_id": pago_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)