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


class InventarioStockRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    s.stock_id,
                    s.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    i.unidad_medida,
                    s.stock_actual,
                    s.stock_minimo,
                    s.ubicacion
                FROM inventario_stock s
                INNER JOIN insumos i
                    ON s.insumo_id = i.insumo_id
                ORDER BY s.stock_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, stock_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    s.stock_id,
                    s.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    i.unidad_medida,
                    s.stock_actual,
                    s.stock_minimo,
                    s.ubicacion
                FROM inventario_stock s
                INNER JOIN insumos i
                    ON s.insumo_id = i.insumo_id
                WHERE s.stock_id = :stock_id
                """,
                {
                    "stock_id": stock_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def get_by_insumo_id(self, insumo_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    s.stock_id,
                    s.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    i.unidad_medida,
                    s.stock_actual,
                    s.stock_minimo,
                    s.ubicacion
                FROM inventario_stock s
                INNER JOIN insumos i
                    ON s.insumo_id = i.insumo_id
                WHERE s.insumo_id = :insumo_id
                """,
                {
                    "insumo_id": insumo_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, stock_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO inventario_stock (
                    insumo_id,
                    stock_actual,
                    stock_minimo,
                    ubicacion
                )
                VALUES (
                    :insumo_id,
                    :stock_actual,
                    :stock_minimo,
                    :ubicacion
                )
                RETURNING stock_id INTO :new_id
                """,
                {
                    "insumo_id": stock_data.get("insumo_id"),
                    "stock_actual": stock_data.get("stock_actual"),
                    "stock_minimo": stock_data.get("stock_minimo"),
                    "ubicacion": stock_data.get("ubicacion"),
                    "new_id": new_id
                }
            )

            stock_id = int(new_id.getvalue()[0])

            return self.get_by_id(stock_id)

        finally:
            cursor.close()

    def update(self, stock_id: int, stock_data: dict) -> Optional[dict]:
        allowed_fields = [
            "insumo_id",
            "stock_actual",
            "stock_minimo",
            "ubicacion"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in stock_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(stock_id)

        stock_data["stock_id"] = stock_id

        sql = f"""
        UPDATE inventario_stock
        SET {", ".join(set_parts)}
        WHERE stock_id = :stock_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, stock_data)

            return self.get_by_id(stock_id)

        finally:
            cursor.close()

    def delete(self, stock_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM inventario_stock
                WHERE stock_id = :stock_id
                """,
                {
                    "stock_id": stock_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()