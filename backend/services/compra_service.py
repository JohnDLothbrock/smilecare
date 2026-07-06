from fastapi import HTTPException, status

from backend.repositories.compra_repository import CompraRepository
from backend.repositories.detalle_compra_repository import (
    DetalleCompraRepository
)
from backend.repositories.insumo_repository import InsumoRepository
from backend.repositories.movimiento_inventario_repository import (
    MovimientoInventarioRepository
)
from backend.repositories.proveedor_repository import ProveedorRepository


DISCRETE_UNITS = {
    "UNIDAD",
    "CAJA",
    "PAQUETE"
}

ALLOWED_UNITS = {
    "UNIDAD",
    "CAJA",
    "PAQUETE",
    "ML",
    "GRAMOS"
}


def raise_database_error(error: Exception):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo completar la compra porque uno de los "
                "registros ya existe."
            )
        )

    if "ORA-02290" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo completar la compra porque uno de los "
                "valores no cumple las reglas de la base de datos."
            )
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo guardar la compra porque una llave "
                "foránea no existe."
            )
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se puede eliminar la compra porque tiene "
                "datos relacionados."
            )
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error de base de datos: {error_message}"
    )


class CompraService:

    def __init__(self, connection):
        self.connection = connection

        self.compra_repository = CompraRepository(
            connection
        )

        self.proveedor_repository = ProveedorRepository(
            connection
        )

        self.insumo_repository = InsumoRepository(
            connection
        )

        self.detalle_compra_repository = (
            DetalleCompraRepository(
                connection
            )
        )

        self.movimiento_repository = (
            MovimientoInventarioRepository(
                connection
            )
        )

    def validate_proveedor_exists(
        self,
        proveedor_id: int
    ):
        proveedor = (
            self.proveedor_repository.get_by_id(
                proveedor_id
            )
        )

        if proveedor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El proveedor indicado no existe."
            )

    def validate_usuario_exists(
        self,
        usuario_id: int
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT usuario_id
                FROM usuarios
                WHERE usuario_id = :usuario_id
                """,
                {
                    "usuario_id": usuario_id
                }
            )

            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El usuario indicado no existe."
                )

        finally:
            cursor.close()

    def get_insumo_by_codigo(
        self,
        codigo: str
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    insumo_id,
                    codigo,
                    nombre
                FROM insumos
                WHERE UPPER(codigo) = UPPER(:codigo)
                """,
                {
                    "codigo": codigo
                }
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "insumo_id": row[0],
                "codigo": row[1],
                "nombre": row[2]
            }

        finally:
            cursor.close()

    def validate_unit(
        self,
        unidad_medida: str
    ):
        normalized_unit = str(
            unidad_medida or ""
        ).upper()

        if normalized_unit not in ALLOWED_UNITS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Unidad de medida inválida. "
                    "Use UNIDAD, CAJA, PAQUETE, ML o GRAMOS."
                )
            )

    def validate_quantity_for_unit(
        self,
        cantidad: float,
        unidad_medida: str,
        product_name: str
    ):
        quantity = float(cantidad)

        normalized_unit = str(
            unidad_medida or ""
        ).upper()

        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"La cantidad de {product_name} "
                    "debe ser mayor a cero."
                )
            )

        if (
            normalized_unit in DISCRETE_UNITS
            and not quantity.is_integer()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"La cantidad de {product_name} debe ser "
                    f"un número entero porque su unidad de medida "
                    f"es {normalized_unit}."
                )
            )

    def validate_workflow_items(
        self,
        items: list
    ):
        if len(items) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "La compra debe contener al menos "
                    "un producto."
                )
            )

        existing_insumo_ids = set()

        new_insumo_codes = set()

        for item in items:
            insumo_id = item.get(
                "insumo_id"
            )

            nuevo_insumo = item.get(
                "nuevo_insumo"
            )

            cantidad = float(
                item["cantidad"]
            )

            if insumo_id is not None:
                if insumo_id in existing_insumo_ids:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            "No puede agregar el mismo insumo "
                            "más de una vez en la misma compra."
                        )
                    )

                existing_insumo_ids.add(
                    insumo_id
                )

                insumo = (
                    self.insumo_repository.get_by_id(
                        insumo_id
                    )
                )

                if insumo is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=(
                            f"El insumo con ID {insumo_id} "
                            "no existe."
                        )
                    )

                self.validate_quantity_for_unit(
                    cantidad,
                    insumo["unidad_medida"],
                    insumo["nombre"]
                )

                continue

            if nuevo_insumo is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Debe seleccionar un insumo existente "
                        "o registrar uno nuevo."
                    )
                )

            codigo = nuevo_insumo[
                "codigo"
            ].strip()

            nombre = nuevo_insumo[
                "nombre"
            ].strip()

            unidad_medida = str(
                nuevo_insumo[
                    "unidad_medida"
                ]
            ).upper()

            self.validate_unit(
                unidad_medida
            )

            self.validate_quantity_for_unit(
                cantidad,
                unidad_medida,
                nombre
            )

            normalized_code = (
                codigo.upper()
            )

            if (
                normalized_code
                in new_insumo_codes
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"El código {codigo} fue agregado "
                        "más de una vez en la compra."
                    )
                )

            new_insumo_codes.add(
                normalized_code
            )

            existing_insumo = (
                self.get_insumo_by_codigo(
                    codigo
                )
            )

            if existing_insumo is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"El código {codigo} ya pertenece "
                        f"al insumo "
                        f"{existing_insumo['nombre']}. "
                        "Seleccione el producto existente."
                    )
                )

    def calculate_subtotal(
        self,
        cantidad: float,
        costo_unitario: float
    ) -> float:
        return round(
            float(cantidad)
            * float(costo_unitario),
            2
        )

    def ensure_stock_record_exists(
        self,
        insumo_id: int
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                SELECT stock_id
                FROM inventario_stock
                WHERE insumo_id = :insumo_id
                FOR UPDATE
                """,
                {
                    "insumo_id": insumo_id
                }
            )

            row = cursor.fetchone()

            if row is not None:
                return

            cursor.execute(
                """
                INSERT INTO inventario_stock (
                    insumo_id,
                    stock_actual,
                    stock_minimo,
                    ubicacion
                )
                VALUES (
                    :insumo_id,
                    0,
                    0,
                    NULL
                )
                """,
                {
                    "insumo_id": insumo_id
                }
            )

        finally:
            cursor.close()

    def increase_stock(
        self,
        insumo_id: int,
        cantidad: float
    ):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE inventario_stock
                SET stock_actual =
                    stock_actual + :cantidad
                WHERE insumo_id = :insumo_id
                """,
                {
                    "cantidad": cantidad,
                    "insumo_id": insumo_id
                }
            )

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=(
                        status.HTTP_500_INTERNAL_SERVER_ERROR
                    ),
                    detail=(
                        "No se pudo actualizar el stock "
                        "del insumo."
                    )
                )

        finally:
            cursor.close()

    def get_all_compras(self):
        try:
            return (
                self.compra_repository.get_all()
            )

        except Exception as error:
            raise_database_error(error)

    def get_compra_by_id(
        self,
        compra_id: int
    ):
        try:
            compra = (
                self.compra_repository.get_by_id(
                    compra_id
                )
            )

            if compra is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Compra no encontrada."
                )

            return compra

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def get_compras_by_proveedor_id(
        self,
        proveedor_id: int
    ):
        try:
            self.validate_proveedor_exists(
                proveedor_id
            )

            return (
                self.compra_repository
                .get_by_proveedor_id(
                    proveedor_id
                )
            )

        except HTTPException:
            raise

        except Exception as error:
            raise_database_error(error)

    def create_compra(
        self,
        compra_data: dict
    ):
        try:
            self.validate_proveedor_exists(
                compra_data["proveedor_id"]
            )

            self.validate_usuario_exists(
                compra_data["usuario_id"]
            )

            if compra_data.get("total") is None:
                compra_data["total"] = 0

            compra = (
                self.compra_repository.create(
                    compra_data
                )
            )

            self.connection.commit()

            return compra

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()

            raise_database_error(error)

    def create_compra_completa(
        self,
        compra_data: dict
    ):
        try:
            proveedor_id = compra_data[
                "proveedor_id"
            ]

            usuario_id = compra_data[
                "usuario_id"
            ]

            fecha_compra = compra_data.get(
                "fecha_compra"
            )

            items = compra_data.get(
                "items",
                []
            )

            self.validate_proveedor_exists(
                proveedor_id
            )

            self.validate_usuario_exists(
                usuario_id
            )

            self.validate_workflow_items(
                items
            )

            compra_header = {
                "proveedor_id": proveedor_id,
                "usuario_id": usuario_id,
                "fecha_compra": fecha_compra,
                "total": 0,
                "estado": "RECIBIDA"
            }

            compra = (
                self.compra_repository.create(
                    compra_header
                )
            )

            compra_id = compra[
                "compra_id"
            ]

            insumos_creados = []

            detalles_creados = []

            movimientos_creados = []

            for item in items:
                insumo_id = item.get(
                    "insumo_id"
                )

                nuevo_insumo = item.get(
                    "nuevo_insumo"
                )

                if insumo_id is None:
                    nuevo_insumo[
                        "codigo"
                    ] = nuevo_insumo[
                        "codigo"
                    ].strip()

                    nuevo_insumo[
                        "nombre"
                    ] = nuevo_insumo[
                        "nombre"
                    ].strip()

                    nuevo_insumo[
                        "unidad_medida"
                    ] = str(
                        nuevo_insumo[
                            "unidad_medida"
                        ]
                    ).upper()

                    nuevo_insumo[
                        "estado"
                    ] = "ACTIVO"

                    insumo = (
                        self.insumo_repository.create(
                            nuevo_insumo
                        )
                    )

                    insumo_id = insumo[
                        "insumo_id"
                    ]

                    insumos_creados.append(
                        insumo
                    )

                cantidad = float(
                    item["cantidad"]
                )

                costo_unitario = float(
                    item["costo_unitario"]
                )

                subtotal = (
                    self.calculate_subtotal(
                        cantidad,
                        costo_unitario
                    )
                )

                detalle_data = {
                    "compra_id": compra_id,
                    "insumo_id": insumo_id,
                    "cantidad": cantidad,
                    "costo_unitario": costo_unitario,
                    "subtotal": subtotal
                }

                detalle = (
                    self.detalle_compra_repository
                    .create(
                        detalle_data
                    )
                )

                detalles_creados.append(
                    detalle
                )

                self.ensure_stock_record_exists(
                    insumo_id
                )

                self.increase_stock(
                    insumo_id,
                    cantidad
                )

                movimiento_data = {
                    "insumo_id": insumo_id,
                    "usuario_id": usuario_id,
                    "detalle_compra_id": (
                        detalle[
                            "detalle_compra_id"
                        ]
                    ),
                    "consulta_id": None,
                    "tipo_movimiento": "ENTRADA",
                    "cantidad": cantidad,
                    "fecha_movimiento": fecha_compra,
                    "motivo": (
                        f"Entrada automática por "
                        f"compra #{compra_id}"
                    )
                }

                movimiento = (
                    self.movimiento_repository
                    .create(
                        movimiento_data
                    )
                )

                movimientos_creados.append(
                    movimiento
                )

            compra_actualizada = (
                self.compra_repository
                .recalculate_total_from_details(
                    compra_id
                )
            )

            self.connection.commit()

            return {
                "message": (
                    "Compra recibida correctamente. "
                    "Los productos fueron agregados "
                    "al inventario."
                ),
                "compra": compra_actualizada,
                "insumos_creados": (
                    insumos_creados
                ),
                "detalles": detalles_creados,
                "movimientos": (
                    movimientos_creados
                )
            }

        except HTTPException:
            self.connection.rollback()

            raise

        except Exception as error:
            self.connection.rollback()

            raise_database_error(error)

    def update_compra(
        self,
        compra_id: int,
        compra_data: dict
    ):
        try:
            current_compra = (
                self.compra_repository.get_by_id(
                    compra_id
                )
            )

            if current_compra is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Compra no encontrada."
                )

            if len(compra_data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "No se enviaron datos "
                        "para actualizar."
                    )
                )

            if "proveedor_id" in compra_data:
                self.validate_proveedor_exists(
                    compra_data[
                        "proveedor_id"
                    ]
                )

            if "usuario_id" in compra_data:
                self.validate_usuario_exists(
                    compra_data[
                        "usuario_id"
                    ]
                )

            updated_compra = (
                self.compra_repository.update(
                    compra_id,
                    compra_data
                )
            )

            self.connection.commit()

            return updated_compra

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()

            raise_database_error(error)

    def delete_compra(
        self,
        compra_id: int
    ):
        try:
            current_compra = (
                self.compra_repository.get_by_id(
                    compra_id
                )
            )

            if current_compra is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Compra no encontrada."
                )

            self.compra_repository.delete(
                compra_id
            )

            self.connection.commit()

            return {
                "message": (
                    "Compra eliminada correctamente."
                ),
                "compra_id": compra_id
            }

        except HTTPException:
            raise

        except Exception as error:
            self.connection.rollback()

            raise_database_error(error)