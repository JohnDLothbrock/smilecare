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


class TratamientoConsultaRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    tc.tratamiento_consulta_id,
                    tc.consulta_id,
                    co.cita_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    tc.tratamiento_id,
                    t.nombre AS tratamiento_nombre,
                    tc.cantidad,
                    tc.precio_unitario,
                    tc.subtotal
                FROM tratamientos_consulta tc
                INNER JOIN consultas co
                    ON tc.consulta_id = co.consulta_id
                INNER JOIN citas c
                    ON co.cita_id = c.cita_id
                INNER JOIN pacientes p
                    ON c.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                INNER JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                ORDER BY tc.tratamiento_consulta_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, tratamiento_consulta_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    tc.tratamiento_consulta_id,
                    tc.consulta_id,
                    co.cita_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    tc.tratamiento_id,
                    t.nombre AS tratamiento_nombre,
                    tc.cantidad,
                    tc.precio_unitario,
                    tc.subtotal
                FROM tratamientos_consulta tc
                INNER JOIN consultas co
                    ON tc.consulta_id = co.consulta_id
                INNER JOIN citas c
                    ON co.cita_id = c.cita_id
                INNER JOIN pacientes p
                    ON c.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                INNER JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                WHERE tc.tratamiento_consulta_id = :tratamiento_consulta_id
                """,
                {
                    "tratamiento_consulta_id": tratamiento_consulta_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def get_by_consulta_id(self, consulta_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    tc.tratamiento_consulta_id,
                    tc.consulta_id,
                    co.cita_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    tc.tratamiento_id,
                    t.nombre AS tratamiento_nombre,
                    tc.cantidad,
                    tc.precio_unitario,
                    tc.subtotal
                FROM tratamientos_consulta tc
                INNER JOIN consultas co
                    ON tc.consulta_id = co.consulta_id
                INNER JOIN citas c
                    ON co.cita_id = c.cita_id
                INNER JOIN pacientes p
                    ON c.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                INNER JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                WHERE tc.consulta_id = :consulta_id
                ORDER BY tc.tratamiento_consulta_id
                """,
                {
                    "consulta_id": consulta_id
                }
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def create(self, tratamiento_consulta_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO tratamientos_consulta (
                    consulta_id,
                    tratamiento_id,
                    cantidad,
                    precio_unitario,
                    subtotal
                )
                VALUES (
                    :consulta_id,
                    :tratamiento_id,
                    :cantidad,
                    :precio_unitario,
                    :subtotal
                )
                RETURNING tratamiento_consulta_id INTO :new_id
                """,
                {
                    "consulta_id": tratamiento_consulta_data.get("consulta_id"),
                    "tratamiento_id": tratamiento_consulta_data.get("tratamiento_id"),
                    "cantidad": tratamiento_consulta_data.get("cantidad"),
                    "precio_unitario": tratamiento_consulta_data.get("precio_unitario"),
                    "subtotal": tratamiento_consulta_data.get("subtotal"),
                    "new_id": new_id
                }
            )

            tratamiento_consulta_id = int(new_id.getvalue()[0])

            return self.get_by_id(tratamiento_consulta_id)

        finally:
            cursor.close()

    def update(
        self,
        tratamiento_consulta_id: int,
        tratamiento_consulta_data: dict
    ) -> Optional[dict]:
        allowed_fields = [
            "consulta_id",
            "tratamiento_id",
            "cantidad",
            "precio_unitario",
            "subtotal"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in tratamiento_consulta_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(tratamiento_consulta_id)

        tratamiento_consulta_data["tratamiento_consulta_id"] = tratamiento_consulta_id

        sql = f"""
        UPDATE tratamientos_consulta
        SET {", ".join(set_parts)}
        WHERE tratamiento_consulta_id = :tratamiento_consulta_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, tratamiento_consulta_data)

            return self.get_by_id(tratamiento_consulta_id)

        finally:
            cursor.close()

    def delete(self, tratamiento_consulta_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM tratamientos_consulta
                WHERE tratamiento_consulta_id = :tratamiento_consulta_id
                """,
                {
                    "tratamiento_consulta_id": tratamiento_consulta_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()