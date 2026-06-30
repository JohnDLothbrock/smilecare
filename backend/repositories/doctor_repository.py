from typing import Optional

import oracledb


def rows_to_dicts(cursor, rows):
    columns = [column[0].lower() for column in cursor.description]

    result = []

    for row in rows:
        row_dict = {}

        for index, column_name in enumerate(columns):
            row_dict[column_name] = row[index]

        result.append(row_dict)

    return result


class DoctorRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    d.doctor_id,
                    d.usuario_id,
                    d.especialidad_id,
                    e.nombre AS especialidad_nombre,
                    d.nombre,
                    d.apellido,
                    d.telefono,
                    d.correo
                FROM doctores d
                INNER JOIN especialidades e
                    ON d.especialidad_id = e.especialidad_id
                ORDER BY d.doctor_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, doctor_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    d.doctor_id,
                    d.usuario_id,
                    d.especialidad_id,
                    e.nombre AS especialidad_nombre,
                    d.nombre,
                    d.apellido,
                    d.telefono,
                    d.correo
                FROM doctores d
                INNER JOIN especialidades e
                    ON d.especialidad_id = e.especialidad_id
                WHERE d.doctor_id = :doctor_id
                """,
                {
                    "doctor_id": doctor_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, doctor_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO doctores (
                    usuario_id,
                    especialidad_id,
                    nombre,
                    apellido,
                    telefono,
                    correo
                )
                VALUES (
                    :usuario_id,
                    :especialidad_id,
                    :nombre,
                    :apellido,
                    :telefono,
                    :correo
                )
                RETURNING doctor_id INTO :new_id
                """,
                {
                    "usuario_id": doctor_data.get("usuario_id"),
                    "especialidad_id": doctor_data.get("especialidad_id"),
                    "nombre": doctor_data.get("nombre"),
                    "apellido": doctor_data.get("apellido"),
                    "telefono": doctor_data.get("telefono"),
                    "correo": doctor_data.get("correo"),
                    "new_id": new_id
                }
            )

            doctor_id = int(new_id.getvalue()[0])

            return self.get_by_id(doctor_id)

        finally:
            cursor.close()

    def update(self, doctor_id: int, doctor_data: dict) -> Optional[dict]:
        allowed_fields = [
            "usuario_id",
            "especialidad_id",
            "nombre",
            "apellido",
            "telefono",
            "correo"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in doctor_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(doctor_id)

        doctor_data["doctor_id"] = doctor_id

        sql = f"""
        UPDATE doctores
        SET {", ".join(set_parts)}
        WHERE doctor_id = :doctor_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, doctor_data)

            return self.get_by_id(doctor_id)

        finally:
            cursor.close()

    def delete(self, doctor_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM doctores
                WHERE doctor_id = :doctor_id
                """,
                {
                    "doctor_id": doctor_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()