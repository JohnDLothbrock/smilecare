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


class CirugiaRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.cirugia_id,
                    c.tratamiento_consulta_id,
                    t.nombre AS tratamiento_nombre,
                    tc.consulta_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    c.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    c.fecha_cirugia,
                    c.descripcion_quirurgica,
                    c.anestesia,
                    c.observaciones,
                    c.estado
                FROM cirugias c
                INNER JOIN tratamientos_consulta tc
                    ON c.tratamiento_consulta_id = tc.tratamiento_consulta_id
                INNER JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                INNER JOIN consultas co
                    ON tc.consulta_id = co.consulta_id
                INNER JOIN citas ci
                    ON co.cita_id = ci.cita_id
                INNER JOIN pacientes p
                    ON ci.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                ORDER BY c.cirugia_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, cirugia_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.cirugia_id,
                    c.tratamiento_consulta_id,
                    t.nombre AS tratamiento_nombre,
                    tc.consulta_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    c.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    c.fecha_cirugia,
                    c.descripcion_quirurgica,
                    c.anestesia,
                    c.observaciones,
                    c.estado
                FROM cirugias c
                INNER JOIN tratamientos_consulta tc
                    ON c.tratamiento_consulta_id = tc.tratamiento_consulta_id
                INNER JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                INNER JOIN consultas co
                    ON tc.consulta_id = co.consulta_id
                INNER JOIN citas ci
                    ON co.cita_id = ci.cita_id
                INNER JOIN pacientes p
                    ON ci.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                WHERE c.cirugia_id = :cirugia_id
                """,
                {
                    "cirugia_id": cirugia_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def get_by_tratamiento_consulta_id(
        self,
        tratamiento_consulta_id: int
    ) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    c.cirugia_id,
                    c.tratamiento_consulta_id,
                    t.nombre AS tratamiento_nombre,
                    tc.consulta_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    c.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    c.fecha_cirugia,
                    c.descripcion_quirurgica,
                    c.anestesia,
                    c.observaciones,
                    c.estado
                FROM cirugias c
                INNER JOIN tratamientos_consulta tc
                    ON c.tratamiento_consulta_id = tc.tratamiento_consulta_id
                INNER JOIN tratamientos t
                    ON tc.tratamiento_id = t.tratamiento_id
                INNER JOIN consultas co
                    ON tc.consulta_id = co.consulta_id
                INNER JOIN citas ci
                    ON co.cita_id = ci.cita_id
                INNER JOIN pacientes p
                    ON ci.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON c.doctor_id = d.doctor_id
                WHERE c.tratamiento_consulta_id = :tratamiento_consulta_id
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

    def create(self, cirugia_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO cirugias (
                    tratamiento_consulta_id,
                    doctor_id,
                    fecha_cirugia,
                    descripcion_quirurgica,
                    anestesia,
                    observaciones,
                    estado
                )
                VALUES (
                    :tratamiento_consulta_id,
                    :doctor_id,
                    :fecha_cirugia,
                    :descripcion_quirurgica,
                    :anestesia,
                    :observaciones,
                    :estado
                )
                RETURNING cirugia_id INTO :new_id
                """,
                {
                    "tratamiento_consulta_id": cirugia_data.get(
                        "tratamiento_consulta_id"
                    ),
                    "doctor_id": cirugia_data.get("doctor_id"),
                    "fecha_cirugia": cirugia_data.get("fecha_cirugia"),
                    "descripcion_quirurgica": cirugia_data.get(
                        "descripcion_quirurgica"
                    ),
                    "anestesia": cirugia_data.get("anestesia"),
                    "observaciones": cirugia_data.get("observaciones"),
                    "estado": cirugia_data.get("estado"),
                    "new_id": new_id
                }
            )

            cirugia_id = int(new_id.getvalue()[0])

            return self.get_by_id(cirugia_id)

        finally:
            cursor.close()

    def update(self, cirugia_id: int, cirugia_data: dict) -> Optional[dict]:
        allowed_fields = [
            "tratamiento_consulta_id",
            "doctor_id",
            "fecha_cirugia",
            "descripcion_quirurgica",
            "anestesia",
            "observaciones",
            "estado"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in cirugia_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(cirugia_id)

        cirugia_data["cirugia_id"] = cirugia_id

        sql = f"""
        UPDATE cirugias
        SET {", ".join(set_parts)}
        WHERE cirugia_id = :cirugia_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, cirugia_data)

            return self.get_by_id(cirugia_id)

        finally:
            cursor.close()

    def delete(self, cirugia_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM cirugias
                WHERE cirugia_id = :cirugia_id
                """,
                {
                    "cirugia_id": cirugia_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()