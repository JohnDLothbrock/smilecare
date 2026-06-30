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


class DetalleFacturaRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    df.detalle_factura_id,
                    df.factura_id,
                    f.numero_factura,
                    df.tratamiento_consulta_id,
                    t.nombre AS tratamiento_nombre,
                    df.descripcion,
                    df.cantidad,
                    df.precio_unitario,
                    df.subtotal
                FROM detalle_factura df
                INNER JOIN facturas f
                    ON df.factura_id = f.factura_id
                LEFT JOIN tratamientos_consulta tc
                    ON df.tratamiento_consulta_id = tc.tratamiento_consulta_id
                LEFT JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                ORDER BY df.detalle_factura_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, detalle_factura_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    df.detalle_factura_id,
                    df.factura_id,
                    f.numero_factura,
                    df.tratamiento_consulta_id,
                    t.nombre AS tratamiento_nombre,
                    df.descripcion,
                    df.cantidad,
                    df.precio_unitario,
                    df.subtotal
                FROM detalle_factura df
                INNER JOIN facturas f
                    ON df.factura_id = f.factura_id
                LEFT JOIN tratamientos_consulta tc
                    ON df.tratamiento_consulta_id = tc.tratamiento_consulta_id
                LEFT JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                WHERE df.detalle_factura_id = :detalle_factura_id
                """,
                {
                    "detalle_factura_id": detalle_factura_id
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
                    df.detalle_factura_id,
                    df.factura_id,
                    f.numero_factura,
                    df.tratamiento_consulta_id,
                    t.nombre AS tratamiento_nombre,
                    df.descripcion,
                    df.cantidad,
                    df.precio_unitario,
                    df.subtotal
                FROM detalle_factura df
                INNER JOIN facturas f
                    ON df.factura_id = f.factura_id
                LEFT JOIN tratamientos_consulta tc
                    ON df.tratamiento_consulta_id = tc.tratamiento_consulta_id
                LEFT JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                WHERE df.factura_id = :factura_id
                ORDER BY df.detalle_factura_id
                """,
                {
                    "factura_id": factura_id
                }
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def create(self, detalle_factura_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO detalle_factura (
                    factura_id,
                    tratamiento_consulta_id,
                    descripcion,
                    cantidad,
                    precio_unitario,
                    subtotal
                )
                VALUES (
                    :factura_id,
                    :tratamiento_consulta_id,
                    :descripcion,
                    :cantidad,
                    :precio_unitario,
                    :subtotal
                )
                RETURNING detalle_factura_id INTO :new_id
                """,
                {
                    "factura_id": detalle_factura_data.get("factura_id"),
                    "tratamiento_consulta_id": detalle_factura_data.get(
                        "tratamiento_consulta_id"
                    ),
                    "descripcion": detalle_factura_data.get("descripcion"),
                    "cantidad": detalle_factura_data.get("cantidad"),
                    "precio_unitario": detalle_factura_data.get("precio_unitario"),
                    "subtotal": detalle_factura_data.get("subtotal"),
                    "new_id": new_id
                }
            )

            detalle_factura_id = int(new_id.getvalue()[0])

            return self.get_by_id(detalle_factura_id)

        finally:
            cursor.close()

    def update(
        self,
        detalle_factura_id: int,
        detalle_factura_data: dict
    ) -> Optional[dict]:
        allowed_fields = [
            "factura_id",
            "tratamiento_consulta_id",
            "descripcion",
            "cantidad",
            "precio_unitario",
            "subtotal"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in detalle_factura_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(detalle_factura_id)

        detalle_factura_data["detalle_factura_id"] = detalle_factura_id

        sql = f"""
        UPDATE detalle_factura
        SET {", ".join(set_parts)}
        WHERE detalle_factura_id = :detalle_factura_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, detalle_factura_data)

            return self.get_by_id(detalle_factura_id)

        finally:
            cursor.close()

    def delete(self, detalle_factura_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM detalle_factura
                WHERE detalle_factura_id = :detalle_factura_id
                """,
                {
                    "detalle_factura_id": detalle_factura_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()