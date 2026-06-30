from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

import oracledb


def serialize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    return value


def rows_to_dicts(cursor, rows):
    columns = [column[0].lower() for column in cursor.description]

    result = []

    for row in rows:
        row_dict = {}

        for index, column_name in enumerate(columns):
            row_dict[column_name] = serialize_value(row[index])

        result.append(row_dict)

    return result


class ComprobanteRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.comprobante_id,
                    c.pago_id,
                    p.factura_id,
                    f.numero_factura,
                    p.monto,
                    c.numero_comprobante,
                    c.tipo_comprobante,
                    c.fecha_emision,
                    c.detalle
                FROM comprobantes c
                INNER JOIN pagos p
                    ON c.pago_id = p.pago_id
                INNER JOIN facturas f
                    ON p.factura_id = f.factura_id
                ORDER BY c.comprobante_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, comprobante_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.comprobante_id,
                    c.pago_id,
                    p.factura_id,
                    f.numero_factura,
                    p.monto,
                    c.numero_comprobante,
                    c.tipo_comprobante,
                    c.fecha_emision,
                    c.detalle
                FROM comprobantes c
                INNER JOIN pagos p
                    ON c.pago_id = p.pago_id
                INNER JOIN facturas f
                    ON p.factura_id = f.factura_id
                WHERE c.comprobante_id = :comprobante_id
                """,
                {
                    "comprobante_id": comprobante_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def get_by_pago_id(self, pago_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.comprobante_id,
                    c.pago_id,
                    p.factura_id,
                    f.numero_factura,
                    p.monto,
                    c.numero_comprobante,
                    c.tipo_comprobante,
                    c.fecha_emision,
                    c.detalle
                FROM comprobantes c
                INNER JOIN pagos p
                    ON c.pago_id = p.pago_id
                INNER JOIN facturas f
                    ON p.factura_id = f.factura_id
                WHERE c.pago_id = :pago_id
                """,
                {
                    "pago_id": pago_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, comprobante_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO comprobantes (
                    pago_id,
                    numero_comprobante,
                    tipo_comprobante,
                    fecha_emision,
                    detalle
                )
                VALUES (
                    :pago_id,
                    :numero_comprobante,
                    :tipo_comprobante,
                    NVL(:fecha_emision, SYSDATE),
                    :detalle
                )
                RETURNING comprobante_id INTO :new_id
                """,
                {
                    "pago_id": comprobante_data.get("pago_id"),
                    "numero_comprobante": comprobante_data.get("numero_comprobante"),
                    "tipo_comprobante": comprobante_data.get("tipo_comprobante"),
                    "fecha_emision": comprobante_data.get("fecha_emision"),
                    "detalle": comprobante_data.get("detalle"),
                    "new_id": new_id
                }
            )

            comprobante_id = int(new_id.getvalue()[0])

            return self.get_by_id(comprobante_id)

        finally:
            cursor.close()

    def update(self, comprobante_id: int, comprobante_data: dict) -> Optional[dict]:
        allowed_fields = [
            "pago_id",
            "numero_comprobante",
            "tipo_comprobante",
            "fecha_emision",
            "detalle"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in comprobante_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(comprobante_id)

        comprobante_data["comprobante_id"] = comprobante_id

        sql = f"""
        UPDATE comprobantes
        SET {", ".join(set_parts)}
        WHERE comprobante_id = :comprobante_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, comprobante_data)

            return self.get_by_id(comprobante_id)

        finally:
            cursor.close()

    def delete(self, comprobante_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM comprobantes
                WHERE comprobante_id = :comprobante_id
                """,
                {
                    "comprobante_id": comprobante_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()