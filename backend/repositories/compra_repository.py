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


class CompraRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.compra_id,
                    c.proveedor_id,
                    p.nombre AS proveedor_nombre,
                    c.usuario_id,
                    u.nombre_usuario,
                    c.fecha_compra,
                    c.total,
                    c.estado
                FROM compras c
                INNER JOIN proveedores p
                    ON c.proveedor_id = p.proveedor_id
                INNER JOIN usuarios u
                    ON c.usuario_id = u.usuario_id
                ORDER BY c.compra_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, compra_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.compra_id,
                    c.proveedor_id,
                    p.nombre AS proveedor_nombre,
                    c.usuario_id,
                    u.nombre_usuario,
                    c.fecha_compra,
                    c.total,
                    c.estado
                FROM compras c
                INNER JOIN proveedores p
                    ON c.proveedor_id = p.proveedor_id
                INNER JOIN usuarios u
                    ON c.usuario_id = u.usuario_id
                WHERE c.compra_id = :compra_id
                """,
                {
                    "compra_id": compra_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def get_by_proveedor_id(self, proveedor_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.compra_id,
                    c.proveedor_id,
                    p.nombre AS proveedor_nombre,
                    c.usuario_id,
                    u.nombre_usuario,
                    c.fecha_compra,
                    c.total,
                    c.estado
                FROM compras c
                INNER JOIN proveedores p
                    ON c.proveedor_id = p.proveedor_id
                INNER JOIN usuarios u
                    ON c.usuario_id = u.usuario_id
                WHERE c.proveedor_id = :proveedor_id
                ORDER BY c.compra_id
                """,
                {
                    "proveedor_id": proveedor_id
                }
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def create(self, compra_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO compras (
                    proveedor_id,
                    usuario_id,
                    fecha_compra,
                    total,
                    estado
                )
                VALUES (
                    :proveedor_id,
                    :usuario_id,
                    NVL(:fecha_compra, SYSDATE),
                    :total,
                    :estado
                )
                RETURNING compra_id INTO :new_id
                """,
                {
                    "proveedor_id": compra_data.get("proveedor_id"),
                    "usuario_id": compra_data.get("usuario_id"),
                    "fecha_compra": compra_data.get("fecha_compra"),
                    "total": compra_data.get("total"),
                    "estado": compra_data.get("estado"),
                    "new_id": new_id
                }
            )

            compra_id = int(new_id.getvalue()[0])

            return self.get_by_id(compra_id)

        finally:
            cursor.close()

    def update(self, compra_id: int, compra_data: dict) -> Optional[dict]:
        allowed_fields = [
            "proveedor_id",
            "usuario_id",
            "fecha_compra",
            "total",
            "estado"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in compra_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(compra_id)

        compra_data["compra_id"] = compra_id

        sql = f"""
        UPDATE compras
        SET {", ".join(set_parts)}
        WHERE compra_id = :compra_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, compra_data)

            return self.get_by_id(compra_id)

        finally:
            cursor.close()

    def delete(self, compra_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM compras
                WHERE compra_id = :compra_id
                """,
                {
                    "compra_id": compra_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()

    def calculate_detalle_total(self, compra_id: int) -> float:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT NVL(SUM(subtotal), 0)
                FROM detalle_compra
                WHERE compra_id = :compra_id
                """,
                {
                    "compra_id": compra_id
                }
            )

            row = cursor.fetchone()

            return float(row[0])

        finally:
            cursor.close()

    def recalculate_total_from_details(self, compra_id: int) -> Optional[dict]:
        compra = self.get_by_id(compra_id)

        if compra is None:
            return None

        total = self.calculate_detalle_total(compra_id)

        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE compras
                SET total = :total
                WHERE compra_id = :compra_id
                """,
                {
                    "total": total,
                    "compra_id": compra_id
                }
            )

            return self.get_by_id(compra_id)

        finally:
            cursor.close()