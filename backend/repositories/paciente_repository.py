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


class PacienteRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    paciente_id,
                    usuario_id,
                    nombre,
                    apellido,
                    telefono,
                    correo,
                    direccion,
                    fecha_nacimiento
                FROM pacientes
                ORDER BY paciente_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, paciente_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    paciente_id,
                    usuario_id,
                    nombre,
                    apellido,
                    telefono,
                    correo,
                    direccion,
                    fecha_nacimiento
                FROM pacientes
                WHERE paciente_id = :paciente_id
                """,
                {
                    "paciente_id": paciente_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, paciente_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO pacientes (
                    usuario_id,
                    nombre,
                    apellido,
                    telefono,
                    correo,
                    direccion,
                    fecha_nacimiento
                )
                VALUES (
                    :usuario_id,
                    :nombre,
                    :apellido,
                    :telefono,
                    :correo,
                    :direccion,
                    :fecha_nacimiento
                )
                RETURNING paciente_id INTO :new_id
                """,
                {
                    "usuario_id": paciente_data.get("usuario_id"),
                    "nombre": paciente_data.get("nombre"),
                    "apellido": paciente_data.get("apellido"),
                    "telefono": paciente_data.get("telefono"),
                    "correo": paciente_data.get("correo"),
                    "direccion": paciente_data.get("direccion"),
                    "fecha_nacimiento": paciente_data.get("fecha_nacimiento"),
                    "new_id": new_id
                }
            )

            paciente_id = int(new_id.getvalue()[0])

            return self.get_by_id(paciente_id)

        finally:
            cursor.close()

    def update(self, paciente_id: int, paciente_data: dict) -> Optional[dict]:
        allowed_fields = [
            "usuario_id",
            "nombre",
            "apellido",
            "telefono",
            "correo",
            "direccion",
            "fecha_nacimiento"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in paciente_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(paciente_id)

        paciente_data["paciente_id"] = paciente_id

        sql = f"""
        UPDATE pacientes
        SET {", ".join(set_parts)}
        WHERE paciente_id = :paciente_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, paciente_data)

            return self.get_by_id(paciente_id)

        finally:
            cursor.close()

    def delete(self, paciente_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM pacientes
                WHERE paciente_id = :paciente_id
                """,
                {
                    "paciente_id": paciente_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()