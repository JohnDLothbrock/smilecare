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


class TratamientoRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    tratamiento_id,
                    nombre,
                    descripcion,
                    costo_base,
                    estado
                FROM tratamientos
                ORDER BY tratamiento_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, tratamiento_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    tratamiento_id,
                    nombre,
                    descripcion,
                    costo_base,
                    estado
                FROM tratamientos
                WHERE tratamiento_id = :tratamiento_id
                """,
                {
                    "tratamiento_id": tratamiento_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, tratamiento_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO tratamientos (
                    nombre,
                    descripcion,
                    costo_base,
                    estado
                )
                VALUES (
                    :nombre,
                    :descripcion,
                    :costo_base,
                    :estado
                )
                RETURNING tratamiento_id INTO :new_id
                """,
                {
                    "nombre": tratamiento_data.get("nombre"),
                    "descripcion": tratamiento_data.get("descripcion"),
                    "costo_base": tratamiento_data.get("costo_base"),
                    "estado": tratamiento_data.get("estado"),
                    "new_id": new_id
                }
            )

            tratamiento_id = int(new_id.getvalue()[0])

            return self.get_by_id(tratamiento_id)

        finally:
            cursor.close()

    def update(self, tratamiento_id: int, tratamiento_data: dict) -> Optional[dict]:
        allowed_fields = [
            "nombre",
            "descripcion",
            "costo_base",
            "estado"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in tratamiento_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(tratamiento_id)

        tratamiento_data["tratamiento_id"] = tratamiento_id

        sql = f"""
        UPDATE tratamientos
        SET {", ".join(set_parts)}
        WHERE tratamiento_id = :tratamiento_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, tratamiento_data)

            return self.get_by_id(tratamiento_id)

        finally:
            cursor.close()

    def delete(self, tratamiento_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM tratamientos
                WHERE tratamiento_id = :tratamiento_id
                """,
                {
                    "tratamiento_id": tratamiento_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()