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


class EspecialidadRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    especialidad_id,
                    nombre,
                    descripcion
                FROM especialidades
                ORDER BY especialidad_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, especialidad_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    especialidad_id,
                    nombre,
                    descripcion
                FROM especialidades
                WHERE especialidad_id = :especialidad_id
                """,
                {
                    "especialidad_id": especialidad_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, especialidad_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO especialidades (
                    nombre,
                    descripcion
                )
                VALUES (
                    :nombre,
                    :descripcion
                )
                RETURNING especialidad_id INTO :new_id
                """,
                {
                    "nombre": especialidad_data.get("nombre"),
                    "descripcion": especialidad_data.get("descripcion"),
                    "new_id": new_id
                }
            )

            especialidad_id = int(new_id.getvalue()[0])

            return self.get_by_id(especialidad_id)

        finally:
            cursor.close()

    def update(self, especialidad_id: int, especialidad_data: dict) -> Optional[dict]:
        allowed_fields = [
            "nombre",
            "descripcion"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in especialidad_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(especialidad_id)

        especialidad_data["especialidad_id"] = especialidad_id

        sql = f"""
        UPDATE especialidades
        SET {", ".join(set_parts)}
        WHERE especialidad_id = :especialidad_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, especialidad_data)

            return self.get_by_id(especialidad_id)

        finally:
            cursor.close()

    def delete(self, especialidad_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM especialidades
                WHERE especialidad_id = :especialidad_id
                """,
                {
                    "especialidad_id": especialidad_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()