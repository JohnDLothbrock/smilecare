from decimal import Decimal
from typing import Any, Optional

import oracledb


def serialize_value(value: Any) -> Any:
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


class DetalleCompraRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    dc.detalle_compra_id,
                    dc.compra_id,
                    dc.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    dc.cantidad,
                    dc.costo_unitario,
                    dc.subtotal
                FROM detalle_compra dc
                INNER JOIN insumos i
                    ON dc.insumo_id = i.insumo_id
                ORDER BY dc.detalle_compra_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, detalle_compra_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    dc.detalle_compra_id,
                    dc.compra_id,
                    dc.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    dc.cantidad,
                    dc.costo_unitario,
                    dc.subtotal
                FROM detalle_compra dc
                INNER JOIN insumos i
                    ON dc.insumo_id = i.insumo_id
                WHERE dc.detalle_compra_id = :detalle_compra_id
                """,
                {
                    "detalle_compra_id": detalle_compra_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def get_by_compra_id(self, compra_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    dc.detalle_compra_id,
                    dc.compra_id,
                    dc.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    dc.cantidad,
                    dc.costo_unitario,
                    dc.subtotal
                FROM detalle_compra dc
                INNER JOIN insumos i
                    ON dc.insumo_id = i.insumo_id
                WHERE dc.compra_id = :compra_id
                ORDER BY dc.detalle_compra_id
                """,
                {
                    "compra_id": compra_id
                }
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def create(self, detalle_compra_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO detalle_compra (
                    compra_id,
                    insumo_id,
                    cantidad,
                    costo_unitario,
                    subtotal
                )
                VALUES (
                    :compra_id,
                    :insumo_id,
                    :cantidad,
                    :costo_unitario,
                    :subtotal
                )
                RETURNING detalle_compra_id INTO :new_id
                """,
                {
                    "compra_id": detalle_compra_data.get("compra_id"),
                    "insumo_id": detalle_compra_data.get("insumo_id"),
                    "cantidad": detalle_compra_data.get("cantidad"),
                    "costo_unitario": detalle_compra_data.get("costo_unitario"),
                    "subtotal": detalle_compra_data.get("subtotal"),
                    "new_id": new_id
                }
            )

            detalle_compra_id = int(new_id.getvalue()[0])

            return self.get_by_id(detalle_compra_id)

        finally:
            cursor.close()

    def update(
        self,
        detalle_compra_id: int,
        detalle_compra_data: dict
    ) -> Optional[dict]:
        allowed_fields = [
            "compra_id",
            "insumo_id",
            "cantidad",
            "costo_unitario",
            "subtotal"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in detalle_compra_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(detalle_compra_id)

        detalle_compra_data["detalle_compra_id"] = detalle_compra_id

        sql = f"""
        UPDATE detalle_compra
        SET {", ".join(set_parts)}
        WHERE detalle_compra_id = :detalle_compra_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, detalle_compra_data)

            return self.get_by_id(detalle_compra_id)

        finally:
            cursor.close()

    def delete(self, detalle_compra_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM detalle_compra
                WHERE detalle_compra_id = :detalle_compra_id
                """,
                {
                    "detalle_compra_id": detalle_compra_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()