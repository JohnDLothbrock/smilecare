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


class DisponibilidadDoctorRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    dis.disponibilidad_id,
                    dis.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    dis.fecha,
                    dis.hora_inicio,
                    dis.hora_fin,
                    dis.estado
                FROM disponibilidad_doctores dis
                INNER JOIN doctores d
                    ON dis.doctor_id = d.doctor_id
                ORDER BY dis.fecha, dis.hora_inicio
                """
            )

            rows = cursor.fetchall()

            return [
                row_to_dict(cursor, row)
                for row in rows
            ]

        finally:
            cursor.close()

    def get_by_id(self, disponibilidad_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    dis.disponibilidad_id,
                    dis.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    dis.fecha,
                    dis.hora_inicio,
                    dis.hora_fin,
                    dis.estado
                FROM disponibilidad_doctores dis
                INNER JOIN doctores d
                    ON dis.doctor_id = d.doctor_id
                WHERE dis.disponibilidad_id = :disponibilidad_id
                """,
                {
                    "disponibilidad_id": disponibilidad_id
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
                    dis.disponibilidad_id,
                    dis.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    dis.fecha,
                    dis.hora_inicio,
                    dis.hora_fin,
                    dis.estado
                FROM disponibilidad_doctores dis
                INNER JOIN doctores d
                    ON dis.doctor_id = d.doctor_id
                WHERE dis.doctor_id = :doctor_id
                ORDER BY dis.fecha, dis.hora_inicio
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
                INSERT INTO disponibilidad_doctores (
                    doctor_id,
                    fecha,
                    hora_inicio,
                    hora_fin,
                    estado
                )
                VALUES (
                    :doctor_id,
                    :fecha,
                    :hora_inicio,
                    :hora_fin,
                    :estado
                )
                RETURNING disponibilidad_id INTO :disponibilidad_id
                """,
                {
                    "doctor_id": data.doctor_id,
                    "fecha": data.fecha,
                    "hora_inicio": data.hora_inicio,
                    "hora_fin": data.hora_fin,
                    "estado": data.estado,
                    "disponibilidad_id": new_id
                }
            )

            self.connection.commit()

            return int(new_id.getvalue()[0])

        finally:
            cursor.close()

    def update(self, disponibilidad_id: int, update_fields: dict):
        if not update_fields:
            return True

        allowed_fields = {
            "doctor_id",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "estado"
        }

        set_parts = []
        params = {
            "disponibilidad_id": disponibilidad_id
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
                UPDATE disponibilidad_doctores
                SET {", ".join(set_parts)}
                WHERE disponibilidad_id = :disponibilidad_id
            """

            cursor.execute(query, params)
            self.connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()

    def delete(self, disponibilidad_id: int):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM disponibilidad_doctores
                WHERE disponibilidad_id = :disponibilidad_id
                """,
                {
                    "disponibilidad_id": disponibilidad_id
                }
            )

            self.connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()