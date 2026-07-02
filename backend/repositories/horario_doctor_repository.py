from datetime import date, datetime
from typing import Any

import oracledb


def serialize_value(value: Any):
    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, date):
        return value.isoformat()

    return value


def row_to_dict(cursor, row):
    columns = [column[0].lower() for column in cursor.description]

    return {
        columns[index]: serialize_value(value)
        for index, value in enumerate(row)
    }


class HorarioDoctorRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    h.horario_id,
                    h.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    h.dia_semana,
                    h.hora_inicio,
                    h.hora_fin,
                    h.estado
                FROM horarios_doctores h
                INNER JOIN doctores d
                    ON h.doctor_id = d.doctor_id
                ORDER BY h.doctor_id, h.dia_semana, h.hora_inicio
                """
            )

            rows = cursor.fetchall()

            return [
                row_to_dict(cursor, row)
                for row in rows
            ]

        finally:
            cursor.close()

    def get_by_id(self, horario_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    h.horario_id,
                    h.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    h.dia_semana,
                    h.hora_inicio,
                    h.hora_fin,
                    h.estado
                FROM horarios_doctores h
                INNER JOIN doctores d
                    ON h.doctor_id = d.doctor_id
                WHERE h.horario_id = :horario_id
                """,
                {
                    "horario_id": horario_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return row_to_dict(cursor, row)

        finally:
            cursor.close()

    def get_by_doctor_id(self, doctor_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    h.horario_id,
                    h.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    h.dia_semana,
                    h.hora_inicio,
                    h.hora_fin,
                    h.estado
                FROM horarios_doctores h
                INNER JOIN doctores d
                    ON h.doctor_id = d.doctor_id
                WHERE h.doctor_id = :doctor_id
                ORDER BY h.dia_semana, h.hora_inicio
                """,
                {
                    "doctor_id": doctor_id
                }
            )

            rows = cursor.fetchall()

            return [
                row_to_dict(cursor, row)
                for row in rows
            ]

        finally:
            cursor.close()

    def create(self, data):
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO horarios_doctores (
                    doctor_id,
                    dia_semana,
                    hora_inicio,
                    hora_fin,
                    estado
                )
                VALUES (
                    :doctor_id,
                    :dia_semana,
                    :hora_inicio,
                    :hora_fin,
                    :estado
                )
                RETURNING horario_id INTO :horario_id
                """,
                {
                    "doctor_id": data.doctor_id,
                    "dia_semana": data.dia_semana,
                    "hora_inicio": data.hora_inicio,
                    "hora_fin": data.hora_fin,
                    "estado": data.estado,
                    "horario_id": new_id
                }
            )

            self.connection.commit()

            return int(new_id.getvalue()[0])

        finally:
            cursor.close()

    def update(self, horario_id: int, update_fields: dict):
        if not update_fields:
            return True

        allowed_fields = {
            "doctor_id",
            "dia_semana",
            "hora_inicio",
            "hora_fin",
            "estado"
        }

        set_parts = []
        params = {
            "horario_id": horario_id
        }

        for field, value in update_fields.items():
            if field in allowed_fields:
                set_parts.append(f"{field} = :{field}")
                params[field] = value

        if not set_parts:
            return True

        cursor = self.connection.cursor()

        try:
            query = f"""
                UPDATE horarios_doctores
                SET {", ".join(set_parts)}
                WHERE horario_id = :horario_id
            """

            cursor.execute(query, params)
            self.connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()

    def delete(self, horario_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM horarios_doctores
                WHERE horario_id = :horario_id
                """,
                {
                    "horario_id": horario_id
                }
            )

            self.connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()