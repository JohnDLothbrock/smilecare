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


class InsumoRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    insumo_id,
                    codigo,
                    nombre,
                    descripcion,
                    unidad_medida,
                    estado
                FROM insumos
                ORDER BY insumo_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, insumo_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    insumo_id,
                    codigo,
                    nombre,
                    descripcion,
                    unidad_medida,
                    estado
                FROM insumos
                WHERE insumo_id = :insumo_id
                """,
                {
                    "insumo_id": insumo_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, insumo_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO insumos (
                    codigo,
                    nombre,
                    descripcion,
                    unidad_medida,
                    estado
                )
                VALUES (
                    :codigo,
                    :nombre,
                    :descripcion,
                    :unidad_medida,
                    :estado
                )
                RETURNING insumo_id INTO :new_id
                """,
                {
                    "codigo": insumo_data.get("codigo"),
                    "nombre": insumo_data.get("nombre"),
                    "descripcion": insumo_data.get("descripcion"),
                    "unidad_medida": insumo_data.get("unidad_medida"),
                    "estado": insumo_data.get("estado"),
                    "new_id": new_id
                }
            )

            insumo_id = int(new_id.getvalue()[0])

            return self.get_by_id(insumo_id)

        finally:
            cursor.close()

    def update(self, insumo_id: int, insumo_data: dict) -> Optional[dict]:
        allowed_fields = [
            "codigo",
            "nombre",
            "descripcion",
            "unidad_medida",
            "estado"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in insumo_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(insumo_id)

        insumo_data["insumo_id"] = insumo_id

        sql = f"""
        UPDATE insumos
        SET {", ".join(set_parts)}
        WHERE insumo_id = :insumo_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, insumo_data)

            return self.get_by_id(insumo_id)

        finally:
            cursor.close()

    def delete(self, insumo_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM insumos
                WHERE insumo_id = :insumo_id
                """,
                {
                    "insumo_id": insumo_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()