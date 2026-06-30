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


class HistorialMedicoRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    hm.historial_id,
                    hm.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    hm.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    hm.alergias,
                    hm.enfermedades,
                    hm.medicamentos,
                    hm.antecedentes_quirurgicos,
                    hm.observaciones,
                    hm.fecha_registro
                FROM historial_medico hm
                INNER JOIN pacientes p
                    ON hm.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON hm.doctor_id = d.doctor_id
                ORDER BY hm.historial_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, historial_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    hm.historial_id,
                    hm.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    hm.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    hm.alergias,
                    hm.enfermedades,
                    hm.medicamentos,
                    hm.antecedentes_quirurgicos,
                    hm.observaciones,
                    hm.fecha_registro
                FROM historial_medico hm
                INNER JOIN pacientes p
                    ON hm.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON hm.doctor_id = d.doctor_id
                WHERE hm.historial_id = :historial_id
                """,
                {
                    "historial_id": historial_id
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
                    hm.historial_id,
                    hm.paciente_id,
                    p.nombre || ' ' || p.apellido AS paciente_nombre,
                    hm.doctor_id,
                    d.nombre || ' ' || d.apellido AS doctor_nombre,
                    hm.alergias,
                    hm.enfermedades,
                    hm.medicamentos,
                    hm.antecedentes_quirurgicos,
                    hm.observaciones,
                    hm.fecha_registro
                FROM historial_medico hm
                INNER JOIN pacientes p
                    ON hm.paciente_id = p.paciente_id
                INNER JOIN doctores d
                    ON hm.doctor_id = d.doctor_id
                WHERE hm.paciente_id = :paciente_id
                ORDER BY hm.fecha_registro DESC
                """,
                {
                    "paciente_id": paciente_id
                }
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def create(self, historial_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO historial_medico (
                    paciente_id,
                    doctor_id,
                    alergias,
                    enfermedades,
                    medicamentos,
                    antecedentes_quirurgicos,
                    observaciones,
                    fecha_registro
                )
                VALUES (
                    :paciente_id,
                    :doctor_id,
                    :alergias,
                    :enfermedades,
                    :medicamentos,
                    :antecedentes_quirurgicos,
                    :observaciones,
                    NVL(:fecha_registro, SYSDATE)
                )
                RETURNING historial_id INTO :new_id
                """,
                {
                    "paciente_id": historial_data.get("paciente_id"),
                    "doctor_id": historial_data.get("doctor_id"),
                    "alergias": historial_data.get("alergias"),
                    "enfermedades": historial_data.get("enfermedades"),
                    "medicamentos": historial_data.get("medicamentos"),
                    "antecedentes_quirurgicos": historial_data.get(
                        "antecedentes_quirurgicos"
                    ),
                    "observaciones": historial_data.get("observaciones"),
                    "fecha_registro": historial_data.get("fecha_registro"),
                    "new_id": new_id
                }
            )

            historial_id = int(new_id.getvalue()[0])

            return self.get_by_id(historial_id)

        finally:
            cursor.close()

    def update(self, historial_id: int, historial_data: dict) -> Optional[dict]:
        allowed_fields = [
            "paciente_id",
            "doctor_id",
            "alergias",
            "enfermedades",
            "medicamentos",
            "antecedentes_quirurgicos",
            "observaciones",
            "fecha_registro"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in historial_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(historial_id)

        historial_data["historial_id"] = historial_id

        sql = f"""
        UPDATE historial_medico
        SET {", ".join(set_parts)}
        WHERE historial_id = :historial_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, historial_data)

            return self.get_by_id(historial_id)

        finally:
            cursor.close()

    def delete(self, historial_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM historial_medico
                WHERE historial_id = :historial_id
                """,
                {
                    "historial_id": historial_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()