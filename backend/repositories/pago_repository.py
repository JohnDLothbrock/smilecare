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


class PagoRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    p.pago_id,
                    p.factura_id,
                    f.numero_factura,
                    f.total AS total_factura,
                    p.metodo_pago_id,
                    mp.nombre AS metodo_pago_nombre,
                    p.monto,
                    p.fecha_pago,
                    p.numero_referencia,
                    p.estado
                FROM pagos p
                INNER JOIN facturas f
                    ON p.factura_id = f.factura_id
                INNER JOIN metodos_pago mp
                    ON p.metodo_pago_id = mp.metodo_pago_id
                ORDER BY p.pago_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, pago_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    p.pago_id,
                    p.factura_id,
                    f.numero_factura,
                    f.total AS total_factura,
                    p.metodo_pago_id,
                    mp.nombre AS metodo_pago_nombre,
                    p.monto,
                    p.fecha_pago,
                    p.numero_referencia,
                    p.estado
                FROM pagos p
                INNER JOIN facturas f
                    ON p.factura_id = f.factura_id
                INNER JOIN metodos_pago mp
                    ON p.metodo_pago_id = mp.metodo_pago_id
                WHERE p.pago_id = :pago_id
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

    def get_by_factura_id(self, factura_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    p.pago_id,
                    p.factura_id,
                    f.numero_factura,
                    f.total AS total_factura,
                    p.metodo_pago_id,
                    mp.nombre AS metodo_pago_nombre,
                    p.monto,
                    p.fecha_pago,
                    p.numero_referencia,
                    p.estado
                FROM pagos p
                INNER JOIN facturas f
                    ON p.factura_id = f.factura_id
                INNER JOIN metodos_pago mp
                    ON p.metodo_pago_id = mp.metodo_pago_id
                WHERE p.factura_id = :factura_id
                ORDER BY p.pago_id
                """,
                {
                    "factura_id": factura_id
                }
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_total_paid_by_factura_id(
        self,
        factura_id: int,
        exclude_pago_id: Optional[int] = None
    ) -> float:
        cursor = self.connection.cursor()

        try:
            if exclude_pago_id is None:
                cursor.execute(
                    """
                    SELECT NVL(SUM(monto), 0)
                    FROM pagos
                    WHERE factura_id = :factura_id
                    """,
                    {
                        "factura_id": factura_id
                    }
                )
            else:
                cursor.execute(
                    """
                    SELECT NVL(SUM(monto), 0)
                    FROM pagos
                    WHERE factura_id = :factura_id
                    AND pago_id <> :exclude_pago_id
                    """,
                    {
                        "factura_id": factura_id,
                        "exclude_pago_id": exclude_pago_id
                    }
                )

            row = cursor.fetchone()

            return float(row[0])

        finally:
            cursor.close()

    def create(self, pago_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO pagos (
                    factura_id,
                    metodo_pago_id,
                    monto,
                    fecha_pago,
                    numero_referencia,
                    estado
                )
                VALUES (
                    :factura_id,
                    :metodo_pago_id,
                    :monto,
                    NVL(:fecha_pago, SYSDATE),
                    :numero_referencia,
                    :estado
                )
                RETURNING pago_id INTO :new_id
                """,
                {
                    "factura_id": pago_data.get("factura_id"),
                    "metodo_pago_id": pago_data.get("metodo_pago_id"),
                    "monto": pago_data.get("monto"),
                    "fecha_pago": pago_data.get("fecha_pago"),
                    "numero_referencia": pago_data.get("numero_referencia"),
                    "estado": pago_data.get("estado"),
                    "new_id": new_id
                }
            )

            pago_id = int(new_id.getvalue()[0])

            return self.get_by_id(pago_id)

        finally:
            cursor.close()

    def update(self, pago_id: int, pago_data: dict) -> Optional[dict]:
        allowed_fields = [
            "factura_id",
            "metodo_pago_id",
            "monto",
            "fecha_pago",
            "numero_referencia",
            "estado"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in pago_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(pago_id)

        pago_data["pago_id"] = pago_id

        sql = f"""
        UPDATE pagos
        SET {", ".join(set_parts)}
        WHERE pago_id = :pago_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, pago_data)

            return self.get_by_id(pago_id)

        finally:
            cursor.close()

    def delete(self, pago_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM pagos
                WHERE pago_id = :pago_id
                """,
                {
                    "pago_id": pago_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()