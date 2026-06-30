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


class MetodoPagoRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    metodo_pago_id,
                    nombre,
                    descripcion,
                    estado
                FROM metodos_pago
                ORDER BY metodo_pago_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, metodo_pago_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    metodo_pago_id,
                    nombre,
                    descripcion,
                    estado
                FROM metodos_pago
                WHERE metodo_pago_id = :metodo_pago_id
                """,
                {
                    "metodo_pago_id": metodo_pago_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, metodo_pago_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO metodos_pago (
                    nombre,
                    descripcion,
                    estado
                )
                VALUES (
                    :nombre,
                    :descripcion,
                    :estado
                )
                RETURNING metodo_pago_id INTO :new_id
                """,
                {
                    "nombre": metodo_pago_data.get("nombre"),
                    "descripcion": metodo_pago_data.get("descripcion"),
                    "estado": metodo_pago_data.get("estado"),
                    "new_id": new_id
                }
            )

            metodo_pago_id = int(new_id.getvalue()[0])

            return self.get_by_id(metodo_pago_id)

        finally:
            cursor.close()

    def update(self, metodo_pago_id: int, metodo_pago_data: dict) -> Optional[dict]:
        allowed_fields = [
            "nombre",
            "descripcion",
            "estado"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in metodo_pago_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(metodo_pago_id)

        metodo_pago_data["metodo_pago_id"] = metodo_pago_id

        sql = f"""
        UPDATE metodos_pago
        SET {", ".join(set_parts)}
        WHERE metodo_pago_id = :metodo_pago_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, metodo_pago_data)

            return self.get_by_id(metodo_pago_id)

        finally:
            cursor.close()

    def delete(self, metodo_pago_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM metodos_pago
                WHERE metodo_pago_id = :metodo_pago_id
                """,
                {
                    "metodo_pago_id": metodo_pago_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()