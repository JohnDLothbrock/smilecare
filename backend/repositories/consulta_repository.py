from datetime import date, datetime
from typing import Any, Optional

import oracledb


def serialize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, date):
        return value.isoformat()

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


class ConsultaRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    co.consulta_id,
                    co.cita_id,
                    c.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    c.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    c.fecha_hora_inicio,
                    co.diagnostico,
                    co.observaciones,
                    co.fecha_atencion
                FROM consultas co
                INNER JOIN citas c
                    ON co.cita_id = c.cita_id
                INNER JOIN pacientes p
                    ON c.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                ORDER BY co.consulta_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, consulta_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    co.consulta_id,
                    co.cita_id,
                    c.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    c.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    c.fecha_hora_inicio,
                    co.diagnostico,
                    co.observaciones,
                    co.fecha_atencion
                FROM consultas co
                INNER JOIN citas c
                    ON co.cita_id = c.cita_id
                INNER JOIN pacientes p
                    ON c.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                WHERE co.consulta_id = :consulta_id
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

    def get_by_cita_id(self, cita_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    co.consulta_id,
                    co.cita_id,
                    c.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    c.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    c.fecha_hora_inicio,
                    co.diagnostico,
                    co.observaciones,
                    co.fecha_atencion
                FROM consultas co
                INNER JOIN citas c
                    ON co.cita_id = c.cita_id
                INNER JOIN pacientes p
                    ON c.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                WHERE co.cita_id = :cita_id
                """,
                {
                    "cita_id": cita_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, consulta_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO consultas (
                    cita_id,
                    diagnostico,
                    observaciones,
                    fecha_atencion
                )
                VALUES (
                    :cita_id,
                    :diagnostico,
                    :observaciones,
                    :fecha_atencion
                )
                RETURNING consulta_id INTO :new_id
                """,
                {
                    "cita_id": consulta_data.get("cita_id"),
                    "diagnostico": consulta_data.get("diagnostico"),
                    "observaciones": consulta_data.get("observaciones"),
                    "fecha_atencion": consulta_data.get("fecha_atencion"),
                    "new_id": new_id
                }
            )

            consulta_id = int(new_id.getvalue()[0])

            return self.get_by_id(consulta_id)

        finally:
            cursor.close()

    def update(self, consulta_id: int, consulta_data: dict) -> Optional[dict]:
        allowed_fields = [
            "cita_id",
            "diagnostico",
            "observaciones",
            "fecha_atencion"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in consulta_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(consulta_id)

        consulta_data["consulta_id"] = consulta_id

        sql = f"""
        UPDATE consultas
        SET {", ".join(set_parts)}
        WHERE consulta_id = :consulta_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, consulta_data)

            return self.get_by_id(consulta_id)

        finally:
            cursor.close()

    def delete(self, consulta_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM consultas
                WHERE consulta_id = :consulta_id
                """,
                {
                    "consulta_id": consulta_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()