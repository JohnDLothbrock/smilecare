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


class MovimientoInventarioRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    m.movimiento_id,
                    m.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    m.usuario_id,
                    u.nombre_usuario,
                    m.detalle_compra_id,
                    m.consulta_id,
                    m.tipo_movimiento,
                    m.cantidad,
                    m.fecha_movimiento,
                    m.motivo
                FROM movimientos_inventario m
                INNER JOIN insumos i
                    ON m.insumo_id = i.insumo_id
                INNER JOIN usuarios u
                    ON m.usuario_id = u.usuario_id
                LEFT JOIN detalle_compra dc
                    ON m.detalle_compra_id = dc.detalle_compra_id
                LEFT JOIN consultas co
                    ON m.consulta_id = co.consulta_id
                ORDER BY m.movimiento_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, movimiento_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    m.movimiento_id,
                    m.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    m.usuario_id,
                    u.nombre_usuario,
                    m.detalle_compra_id,
                    m.consulta_id,
                    m.tipo_movimiento,
                    m.cantidad,
                    m.fecha_movimiento,
                    m.motivo
                FROM movimientos_inventario m
                INNER JOIN insumos i
                    ON m.insumo_id = i.insumo_id
                INNER JOIN usuarios u
                    ON m.usuario_id = u.usuario_id
                LEFT JOIN detalle_compra dc
                    ON m.detalle_compra_id = dc.detalle_compra_id
                LEFT JOIN consultas co
                    ON m.consulta_id = co.consulta_id
                WHERE m.movimiento_id = :movimiento_id
                """,
                {
                    "movimiento_id": movimiento_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def get_by_insumo_id(self, insumo_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    m.movimiento_id,
                    m.insumo_id,
                    i.codigo AS insumo_codigo,
                    i.nombre AS insumo_nombre,
                    m.usuario_id,
                    u.nombre_usuario,
                    m.detalle_compra_id,
                    m.consulta_id,
                    m.tipo_movimiento,
                    m.cantidad,
                    m.fecha_movimiento,
                    m.motivo
                FROM movimientos_inventario m
                INNER JOIN insumos i
                    ON m.insumo_id = i.insumo_id
                INNER JOIN usuarios u
                    ON m.usuario_id = u.usuario_id
                LEFT JOIN detalle_compra dc
                    ON m.detalle_compra_id = dc.detalle_compra_id
                LEFT JOIN consultas co
                    ON m.consulta_id = co.consulta_id
                WHERE m.insumo_id = :insumo_id
                ORDER BY m.movimiento_id
                """,
                {
                    "insumo_id": insumo_id
                }
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def create(self, movimiento_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO movimientos_inventario (
                    insumo_id,
                    usuario_id,
                    detalle_compra_id,
                    consulta_id,
                    tipo_movimiento,
                    cantidad,
                    fecha_movimiento,
                    motivo
                )
                VALUES (
                    :insumo_id,
                    :usuario_id,
                    :detalle_compra_id,
                    :consulta_id,
                    :tipo_movimiento,
                    :cantidad,
                    NVL(:fecha_movimiento, SYSDATE),
                    :motivo
                )
                RETURNING movimiento_id INTO :new_id
                """,
                {
                    "insumo_id": movimiento_data.get("insumo_id"),
                    "usuario_id": movimiento_data.get("usuario_id"),
                    "detalle_compra_id": movimiento_data.get("detalle_compra_id"),
                    "consulta_id": movimiento_data.get("consulta_id"),
                    "tipo_movimiento": movimiento_data.get("tipo_movimiento"),
                    "cantidad": movimiento_data.get("cantidad"),
                    "fecha_movimiento": movimiento_data.get("fecha_movimiento"),
                    "motivo": movimiento_data.get("motivo"),
                    "new_id": new_id
                }
            )

            movimiento_id = int(new_id.getvalue()[0])

            return self.get_by_id(movimiento_id)

        finally:
            cursor.close()

    def update(self, movimiento_id: int, movimiento_data: dict) -> Optional[dict]:
        allowed_fields = [
            "usuario_id",
            "detalle_compra_id",
            "consulta_id",
            "fecha_movimiento",
            "motivo"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in movimiento_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(movimiento_id)

        movimiento_data["movimiento_id"] = movimiento_id

        sql = f"""
        UPDATE movimientos_inventario
        SET {", ".join(set_parts)}
        WHERE movimiento_id = :movimiento_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, movimiento_data)

            return self.get_by_id(movimiento_id)

        finally:
            cursor.close()

    def delete(self, movimiento_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM movimientos_inventario
                WHERE movimiento_id = :movimiento_id
                """,
                {
                    "movimiento_id": movimiento_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()

    def update_stock_actual(self, insumo_id: int, new_stock: float):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE inventario_stock
                SET stock_actual = :new_stock
                WHERE insumo_id = :insumo_id
                """,
                {
                    "new_stock": new_stock,
                    "insumo_id": insumo_id
                }
            )

        finally:
            cursor.close()