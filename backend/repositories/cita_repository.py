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


class CitaRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.cita_id,
                    c.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    c.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    c.fecha_hora_inicio,
                    c.duracion_minutos,
                    c.estado,
                    c.motivo
                FROM citas c
                INNER JOIN pacientes p
                    ON c.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                ORDER BY c.fecha_hora_inicio
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, cita_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.cita_id,
                    c.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    c.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    c.fecha_hora_inicio,
                    c.duracion_minutos,
                    c.estado,
                    c.motivo
                FROM citas c
                INNER JOIN pacientes p
                    ON c.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                WHERE c.cita_id = :cita_id
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

    def create(self, cita_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO citas (
                    paciente_id,
                    doctor_id,
                    fecha_hora_inicio,
                    duracion_minutos,
                    estado,
                    motivo
                )
                VALUES (
                    :paciente_id,
                    :doctor_id,
                    :fecha_hora_inicio,
                    :duracion_minutos,
                    :estado,
                    :motivo
                )
                RETURNING cita_id INTO :new_id
                """,
                {
                    "paciente_id": cita_data.get("paciente_id"),
                    "doctor_id": cita_data.get("doctor_id"),
                    "fecha_hora_inicio": cita_data.get("fecha_hora_inicio"),
                    "duracion_minutos": cita_data.get("duracion_minutos"),
                    "estado": cita_data.get("estado"),
                    "motivo": cita_data.get("motivo"),
                    "new_id": new_id
                }
            )

            cita_id = int(new_id.getvalue()[0])

            return self.get_by_id(cita_id)

        finally:
            cursor.close()

    def update(self, cita_id: int, cita_data: dict) -> Optional[dict]:
        allowed_fields = [
            "paciente_id",
            "doctor_id",
            "fecha_hora_inicio",
            "duracion_minutos",
            "estado",
            "motivo"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in cita_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(cita_id)

        cita_data["cita_id"] = cita_id

        sql = f"""
        UPDATE citas
        SET {", ".join(set_parts)}
        WHERE cita_id = :cita_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, cita_data)

            return self.get_by_id(cita_id)

        finally:
            cursor.close()

    def delete(self, cita_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM citas
                WHERE cita_id = :cita_id
                """,
                {
                    "cita_id": cita_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()