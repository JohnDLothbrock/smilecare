from fastapi import HTTPException, status

from backend.repositories.consulta_repository import ConsultaRepository
from backend.repositories.factura_repository import FacturaRepository
from backend.repositories.paciente_repository import PacienteRepository
from backend.repositories.tratamiento_consulta_repository import (
    TratamientoConsultaRepository
)


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la factura porque el número de factura o la consulta ya están registrados."
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo guardar la factura porque una llave foránea no existe."
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar físicamente la factura porque tiene detalles, pagos o comprobantes relacionados. Use anulación lógica."
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class FacturaService:

    def __init__(self, connection):
        self.connection = connection
        self.factura_repository = FacturaRepository(connection)
        self.paciente_repository = PacienteRepository(connection)
        self.consulta_repository = ConsultaRepository(connection)
        self.tratamiento_consulta_repository = TratamientoConsultaRepository(
            connection
        )

    def validate_paciente_exists(self, paciente_id: int):
        paciente = self.paciente_repository.get_by_id(paciente_id)

        if paciente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El paciente indicado no existe."
            )

    def validate_consulta_exists(self, consulta_id: int):
        consulta = self.consulta_repository.get_by_id(consulta_id)

        if consulta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La consulta indicada no existe."
            )

        return consulta

    def validate_consulta_patient(self, consulta: dict, paciente_id: int):
        if consulta["paciente_id"] != paciente_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La consulta indicada no pertenece al paciente indicado."
            )

    def calculate_subtotal_from_consulta(self, consulta_id: int) -> float:
        tratamientos = self.tratamiento_consulta_repository.get_by_consulta_id(
            consulta_id
        )

        subtotal = 0

        for tratamiento in tratamientos:
            subtotal += float(tratamiento["subtotal"])

        return round(subtotal, 2)

    def prepare_create_data(self, factura_data: dict) -> dict:
        self.validate_paciente_exists(factura_data["paciente_id"])

        consulta_id = factura_data.get("consulta_id")

        if consulta_id is not None:
            consulta = self.validate_consulta_exists(consulta_id)

            self.validate_consulta_patient(
                consulta,
                factura_data["paciente_id"]
            )

        if factura_data.get("subtotal") is None:
            if consulta_id is not None:
                factura_data["subtotal"] = self.calculate_subtotal_from_consulta(
                    consulta_id
                )
            else:
                factura_data["subtotal"] = 0

        if factura_data.get("impuesto") is None:
            factura_data["impuesto"] = 0

        factura_data["total"] = round(
            float(factura_data["subtotal"]) + float(factura_data["impuesto"]),
            2
        )

        return factura_data

    def prepare_update_data(self, current_factura: dict, factura_data: dict) -> dict:
        paciente_id = factura_data.get(
            "paciente_id",
            current_factura["paciente_id"]
        )

        consulta_id = factura_data.get(
            "consulta_id",
            current_factura["consulta_id"]
        )

        if "paciente_id" in factura_data:
            self.validate_paciente_exists(factura_data["paciente_id"])

        if "consulta_id" in factura_data and factura_data["consulta_id"] is not None:
            consulta = self.validate_consulta_exists(factura_data["consulta_id"])

            self.validate_consulta_patient(
                consulta,
                paciente_id
            )

        if "consulta_id" in factura_data and "subtotal" not in factura_data:
            if consulta_id is not None:
                factura_data["subtotal"] = self.calculate_subtotal_from_consulta(
                    consulta_id
                )

        subtotal = factura_data.get(
            "subtotal",
            current_factura["subtotal"]
        )

        impuesto = factura_data.get(
            "impuesto",
            current_factura["impuesto"]
        )

        if "subtotal" in factura_data or "impuesto" in factura_data:
            factura_data["total"] = round(
                float(subtotal) + float(impuesto or 0),
                2
            )

        return factura_data

    def get_all_facturas(self):
        try:
            return self.factura_repository.get_all()

        except Exception as error:
            raise_database_error(error)

    def get_factura_by_id(self, factura_id: int):
        try:
            factura = self.factura_repository.get_by_id(factura_id)

            if factura is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Factura no encontrada."
                )

            return factura

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_facturas_by_paciente_id(self, paciente_id: int):
        try:
            self.validate_paciente_exists(paciente_id)

            return self.factura_repository.get_by_paciente_id(paciente_id)

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_factura_by_consulta_id(self, consulta_id: int):
        try:
            self.validate_consulta_exists(consulta_id)

            factura = self.factura_repository.get_by_consulta_id(consulta_id)

            if factura is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No existe una factura para esta consulta."
                )

            return factura

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_factura(self, factura_data: dict):
        try:
            factura_data = self.prepare_create_data(factura_data)

            factura = self.factura_repository.create(factura_data)

            self.connection.commit()

            return factura

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def update_factura(self, factura_id: int, factura_data: dict):
        try:
            current_factura = self.factura_repository.get_by_id(factura_id)

            if current_factura is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Factura no encontrada."
                )

            if len(factura_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se enviaron datos para actualizar."
                )

            factura_data = self.prepare_update_data(
                current_factura,
                factura_data
            )

            updated_factura = self.factura_repository.update(
                factura_id,
                factura_data
            )

            self.connection.commit()

            return updated_factura

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def delete_factura(self, factura_id: int):
        try:
            current_factura = self.factura_repository.get_by_id(factura_id)

            if current_factura is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Factura no encontrada."
                )

            if current_factura["estado"] == "ANULADA":
                return {
                    "message": "La factura ya se encuentra anulada.",
                    "factura_id": factura_id,
                    "estado": "ANULADA"
                }

            updated_factura = self.factura_repository.soft_delete(factura_id)

            self.connection.commit()

            return {
                "message": "Factura anulada correctamente. Los detalles, pagos y comprobantes se conservaron.",
                "factura": updated_factura
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)

    def restore_factura(self, factura_id: int):
        try:
            current_factura = self.factura_repository.get_by_id(factura_id)

            if current_factura is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Factura no encontrada."
                )

            if current_factura["estado"] != "ANULADA":
                return {
                    "message": "La factura no está anulada, no es necesario restaurarla.",
                    "factura": current_factura
                }

            applied_payments = self.factura_repository.count_applied_payments(
                factura_id
            )

            new_status = "PAGADA" if applied_payments > 0 else "PENDIENTE"

            restored_factura = self.factura_repository.restore(
                factura_id,
                new_status
            )

            self.connection.commit()

            return {
                "message": f"Factura restaurada correctamente con estado {new_status}.",
                "factura": restored_factura
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()
            raise_database_error(error)