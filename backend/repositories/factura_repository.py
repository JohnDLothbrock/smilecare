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


class FacturaRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    f.factura_id,
                    f.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    f.consulta_id,
                    f.numero_factura,
                    f.fecha_emision,
                    f.subtotal,
                    f.impuesto,
                    f.total,
                    f.estado
                FROM facturas f
                INNER JOIN pacientes p
                    ON f.paciente_id = p.paciente_id
                ORDER BY f.factura_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, factura_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    f.factura_id,
                    f.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    f.consulta_id,
                    f.numero_factura,
                    f.fecha_emision,
                    f.subtotal,
                    f.impuesto,
                    f.total,
                    f.estado
                FROM facturas f
                INNER JOIN pacientes p
                    ON f.paciente_id = p.paciente_id
                WHERE f.factura_id = :factura_id
                """,
                {
                    "factura_id": factura_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def get_by_paciente_id(self, paciente_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    f.factura_id,
                    f.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    f.consulta_id,
                    f.numero_factura,
                    f.fecha_emision,
                    f.subtotal,
                    f.impuesto,
                    f.total,
                    f.estado
                FROM facturas f
                INNER JOIN pacientes p
                    ON f.paciente_id = p.paciente_id
                WHERE f.paciente_id = :paciente_id
                ORDER BY f.factura_id
                """,
                {
                    "paciente_id": paciente_id
                }
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_consulta_id(self, consulta_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    f.factura_id,
                    f.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    f.consulta_id,
                    f.numero_factura,
                    f.fecha_emision,
                    f.subtotal,
                    f.impuesto,
                    f.total,
                    f.estado
                FROM facturas f
                INNER JOIN pacientes p
                    ON f.paciente_id = p.paciente_id
                WHERE f.consulta_id = :consulta_id
                """,
                {
                    "consulta_id": consulta_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, factura_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO facturas (
                    paciente_id,
                    consulta_id,
                    numero_factura,
                    fecha_emision,
                    subtotal,
                    impuesto,
                    total,
                    estado
                )
                VALUES (
                    :paciente_id,
                    :consulta_id,
                    :numero_factura,
                    NVL(:fecha_emision, SYSDATE),
                    :subtotal,
                    :impuesto,
                    :total,
                    :estado
                )
                RETURNING factura_id INTO :new_id
                """,
                {
                    "paciente_id": factura_data.get("paciente_id"),
                    "consulta_id": factura_data.get("consulta_id"),
                    "numero_factura": factura_data.get("numero_factura"),
                    "fecha_emision": factura_data.get("fecha_emision"),
                    "subtotal": factura_data.get("subtotal"),
                    "impuesto": factura_data.get("impuesto"),
                    "total": factura_data.get("total"),
                    "estado": factura_data.get("estado"),
                    "new_id": new_id
                }
            )

            factura_id = int(new_id.getvalue()[0])

            return self.get_by_id(factura_id)

        finally:
            cursor.close()

    def update(self, factura_id: int, factura_data: dict) -> Optional[dict]:
        allowed_fields = [
            "paciente_id",
            "consulta_id",
            "numero_factura",
            "fecha_emision",
            "subtotal",
            "impuesto",
            "total",
            "estado"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in factura_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(factura_id)

        factura_data["factura_id"] = factura_id

        sql = f"""
        UPDATE facturas
        SET {", ".join(set_parts)}
        WHERE factura_id = :factura_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, factura_data)

            return self.get_by_id(factura_id)

        finally:
            cursor.close()

    def delete(self, factura_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM facturas
                WHERE factura_id = :factura_id
                """,
                {
                    "factura_id": factura_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()

    def calculate_detalle_subtotal(self, factura_id: int) -> float:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT NVL(SUM(subtotal), 0)
                FROM detalle_factura
                WHERE factura_id = :factura_id
                """,
                {
                    "factura_id": factura_id
                }
            )

            row = cursor.fetchone()

            return float(row[0])

        finally:
            cursor.close()

    def recalculate_totals_from_details(self, factura_id: int) -> Optional[dict]:
        factura = self.get_by_id(factura_id)

        if factura is None:
            return None

        subtotal = self.calculate_detalle_subtotal(factura_id)
        impuesto = factura.get("impuesto") or 0
        total = round(float(subtotal) + float(impuesto), 2)

        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE facturas
                SET
                    subtotal = :subtotal,
                    total = :total
                WHERE factura_id = :factura_id
                """,
                {
                    "subtotal": subtotal,
                    "total": total,
                    "factura_id": factura_id
                }
            )

            return self.get_by_id(factura_id)

        finally:
            cursor.close()