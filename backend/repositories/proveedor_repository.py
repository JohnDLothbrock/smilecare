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


class ProveedorRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    proveedor_id,
                    nombre,
                    telefono,
                    correo,
                    direccion,
                    estado
                FROM proveedores
                ORDER BY proveedor_id
                """
            )

            rows = cursor.fetchall()

            return rows_to_dicts(cursor, rows)

        finally:
            cursor.close()

    def get_by_id(self, proveedor_id: int) -> Optional[dict]:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    proveedor_id,
                    nombre,
                    telefono,
                    correo,
                    direccion,
                    estado
                FROM proveedores
                WHERE proveedor_id = :proveedor_id
                """,
                {
                    "proveedor_id": proveedor_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return rows_to_dicts(cursor, [row])[0]

        finally:
            cursor.close()

    def create(self, proveedor_data: dict) -> dict:
        cursor = self.connection.cursor()

        try:
            new_id = cursor.var(oracledb.NUMBER)

            cursor.execute(
                """
                INSERT INTO proveedores (
                    nombre,
                    telefono,
                    correo,
                    direccion,
                    estado
                )
                VALUES (
                    :nombre,
                    :telefono,
                    :correo,
                    :direccion,
                    :estado
                )
                RETURNING proveedor_id INTO :new_id
                """,
                {
                    "nombre": proveedor_data.get("nombre"),
                    "telefono": proveedor_data.get("telefono"),
                    "correo": proveedor_data.get("correo"),
                    "direccion": proveedor_data.get("direccion"),
                    "estado": proveedor_data.get("estado"),
                    "new_id": new_id
                }
            )

            proveedor_id = int(new_id.getvalue()[0])

            return self.get_by_id(proveedor_id)

        finally:
            cursor.close()

    def update(self, proveedor_id: int, proveedor_data: dict) -> Optional[dict]:
        allowed_fields = [
            "nombre",
            "telefono",
            "correo",
            "direccion",
            "estado"
        ]

        set_parts = []

        for field in allowed_fields:
            if field in proveedor_data:
                set_parts.append(f"{field} = :{field}")

        if not set_parts:
            return self.get_by_id(proveedor_id)

        proveedor_data["proveedor_id"] = proveedor_id

        sql = f"""
        UPDATE proveedores
        SET {", ".join(set_parts)}
        WHERE proveedor_id = :proveedor_id
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, proveedor_data)

            return self.get_by_id(proveedor_id)

        finally:
            cursor.close()

    def delete(self, proveedor_id: int) -> bool:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM proveedores
                WHERE proveedor_id = :proveedor_id
                """,
                {
                    "proveedor_id": proveedor_id
                }
            )

            return cursor.rowcount > 0

        finally:
            cursor.close()