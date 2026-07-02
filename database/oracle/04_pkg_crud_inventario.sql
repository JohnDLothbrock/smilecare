SET SERVEROUTPUT ON;

PROMPT ============================================================
PROMPT PAQUETE CRUD INVENTARIO - SMILECARE
PROMPT ============================================================

/*
    Archivo: 04_pkg_crud_inventario.sql
    Proyecto: SmileCare
    Curso: SC-504 Lenguajes de Base de Datos

    Objetivo:
    Crear un paquete Oracle con procedimientos CRUD para inventario,
    compras y movimientos de insumos.

    Tablas incluidas:
    - PROVEEDORES
    - INSUMOS
    - INVENTARIO_STOCK
    - COMPRAS
    - DETALLE_COMPRA
    - MOVIMIENTOS_INVENTARIO
*/

CREATE OR REPLACE PACKAGE pkg_smilecare_crud_inventario AS

    /*
        ============================================================
        CRUD PROVEEDORES
        ============================================================
    */

    PROCEDURE crear_proveedor (
        p_nombre IN proveedores.nombre%TYPE,
        p_telefono IN proveedores.telefono%TYPE,
        p_correo IN proveedores.correo%TYPE,
        p_direccion IN proveedores.direccion%TYPE,
        p_estado IN proveedores.estado%TYPE,
        p_proveedor_id OUT proveedores.proveedor_id%TYPE
    );

    PROCEDURE actualizar_proveedor (
        p_proveedor_id IN proveedores.proveedor_id%TYPE,
        p_nombre IN proveedores.nombre%TYPE,
        p_telefono IN proveedores.telefono%TYPE,
        p_correo IN proveedores.correo%TYPE,
        p_direccion IN proveedores.direccion%TYPE,
        p_estado IN proveedores.estado%TYPE
    );

    PROCEDURE eliminar_proveedor (
        p_proveedor_id IN proveedores.proveedor_id%TYPE
    );

    PROCEDURE listar_proveedores (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD INSUMOS
        ============================================================
    */

    PROCEDURE crear_insumo (
        p_codigo IN insumos.codigo%TYPE,
        p_nombre IN insumos.nombre%TYPE,
        p_descripcion IN insumos.descripcion%TYPE,
        p_unidad_medida IN insumos.unidad_medida%TYPE,
        p_estado IN insumos.estado%TYPE,
        p_insumo_id OUT insumos.insumo_id%TYPE
    );

    PROCEDURE actualizar_insumo (
        p_insumo_id IN insumos.insumo_id%TYPE,
        p_codigo IN insumos.codigo%TYPE,
        p_nombre IN insumos.nombre%TYPE,
        p_descripcion IN insumos.descripcion%TYPE,
        p_unidad_medida IN insumos.unidad_medida%TYPE,
        p_estado IN insumos.estado%TYPE
    );

    PROCEDURE eliminar_insumo (
        p_insumo_id IN insumos.insumo_id%TYPE
    );

    PROCEDURE listar_insumos (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD INVENTARIO_STOCK
        ============================================================
    */

    PROCEDURE crear_stock (
        p_insumo_id IN inventario_stock.insumo_id%TYPE,
        p_stock_actual IN inventario_stock.stock_actual%TYPE,
        p_stock_minimo IN inventario_stock.stock_minimo%TYPE,
        p_ubicacion IN inventario_stock.ubicacion%TYPE,
        p_stock_id OUT inventario_stock.stock_id%TYPE
    );

    PROCEDURE actualizar_stock (
        p_stock_id IN inventario_stock.stock_id%TYPE,
        p_insumo_id IN inventario_stock.insumo_id%TYPE,
        p_stock_actual IN inventario_stock.stock_actual%TYPE,
        p_stock_minimo IN inventario_stock.stock_minimo%TYPE,
        p_ubicacion IN inventario_stock.ubicacion%TYPE
    );

    PROCEDURE eliminar_stock (
        p_stock_id IN inventario_stock.stock_id%TYPE
    );

    PROCEDURE listar_stock (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_stock_bajo_minimo (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD COMPRAS
        ============================================================
    */

    PROCEDURE crear_compra (
        p_proveedor_id IN compras.proveedor_id%TYPE,
        p_usuario_id IN compras.usuario_id%TYPE,
        p_fecha_compra IN compras.fecha_compra%TYPE,
        p_total IN compras.total%TYPE,
        p_estado IN compras.estado%TYPE,
        p_compra_id OUT compras.compra_id%TYPE
    );

    PROCEDURE actualizar_compra (
        p_compra_id IN compras.compra_id%TYPE,
        p_proveedor_id IN compras.proveedor_id%TYPE,
        p_usuario_id IN compras.usuario_id%TYPE,
        p_fecha_compra IN compras.fecha_compra%TYPE,
        p_total IN compras.total%TYPE,
        p_estado IN compras.estado%TYPE
    );

    PROCEDURE eliminar_compra (
        p_compra_id IN compras.compra_id%TYPE
    );

    PROCEDURE listar_compras (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD DETALLE_COMPRA
        ============================================================
    */

    PROCEDURE crear_detalle_compra (
        p_compra_id IN detalle_compra.compra_id%TYPE,
        p_insumo_id IN detalle_compra.insumo_id%TYPE,
        p_cantidad IN detalle_compra.cantidad%TYPE,
        p_costo_unitario IN detalle_compra.costo_unitario%TYPE,
        p_detalle_compra_id OUT detalle_compra.detalle_compra_id%TYPE
    );

    PROCEDURE actualizar_detalle_compra (
        p_detalle_compra_id IN detalle_compra.detalle_compra_id%TYPE,
        p_compra_id IN detalle_compra.compra_id%TYPE,
        p_insumo_id IN detalle_compra.insumo_id%TYPE,
        p_cantidad IN detalle_compra.cantidad%TYPE,
        p_costo_unitario IN detalle_compra.costo_unitario%TYPE
    );

    PROCEDURE eliminar_detalle_compra (
        p_detalle_compra_id IN detalle_compra.detalle_compra_id%TYPE
    );

    PROCEDURE listar_detalles_compra (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_detalles_por_compra (
        p_compra_id IN detalle_compra.compra_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD MOVIMIENTOS_INVENTARIO
        ============================================================
    */

    PROCEDURE crear_movimiento_inventario (
        p_insumo_id IN movimientos_inventario.insumo_id%TYPE,
        p_usuario_id IN movimientos_inventario.usuario_id%TYPE,
        p_detalle_compra_id IN movimientos_inventario.detalle_compra_id%TYPE,
        p_consulta_id IN movimientos_inventario.consulta_id%TYPE,
        p_tipo_movimiento IN movimientos_inventario.tipo_movimiento%TYPE,
        p_cantidad IN movimientos_inventario.cantidad%TYPE,
        p_fecha_movimiento IN movimientos_inventario.fecha_movimiento%TYPE,
        p_motivo IN movimientos_inventario.motivo%TYPE,
        p_movimiento_id OUT movimientos_inventario.movimiento_id%TYPE
    );

    PROCEDURE actualizar_movimiento_inventario (
        p_movimiento_id IN movimientos_inventario.movimiento_id%TYPE,
        p_usuario_id IN movimientos_inventario.usuario_id%TYPE,
        p_detalle_compra_id IN movimientos_inventario.detalle_compra_id%TYPE,
        p_consulta_id IN movimientos_inventario.consulta_id%TYPE,
        p_fecha_movimiento IN movimientos_inventario.fecha_movimiento%TYPE,
        p_motivo IN movimientos_inventario.motivo%TYPE
    );

    PROCEDURE eliminar_movimiento_inventario (
        p_movimiento_id IN movimientos_inventario.movimiento_id%TYPE
    );

    PROCEDURE listar_movimientos_inventario (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_movimientos_por_insumo (
        p_insumo_id IN movimientos_inventario.insumo_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

END pkg_smilecare_crud_inventario;
/

SHOW ERRORS PACKAGE pkg_smilecare_crud_inventario;


CREATE OR REPLACE PACKAGE BODY pkg_smilecare_crud_inventario AS

    /*
        Procedimiento interno:
        Recalcula el total de una compra usando los subtotales
        registrados en DETALLE_COMPRA.
    */
    PROCEDURE recalcular_total_compra (
        p_compra_id IN compras.compra_id%TYPE
    ) AS
        v_total compras.total%TYPE;
    BEGIN
        SELECT NVL(SUM(subtotal), 0)
        INTO v_total
        FROM detalle_compra
        WHERE compra_id = p_compra_id;

        UPDATE compras
        SET total = v_total
        WHERE compra_id = p_compra_id;
    END recalcular_total_compra;


    /*
        Procedimiento interno:
        Crea un registro de stock en cero si el insumo todavía
        no existe en INVENTARIO_STOCK.
    */
    PROCEDURE asegurar_stock (
        p_insumo_id IN inventario_stock.insumo_id%TYPE
    ) AS
        v_cantidad NUMBER;
    BEGIN
        SELECT COUNT(*)
        INTO v_cantidad
        FROM inventario_stock
        WHERE insumo_id = p_insumo_id;

        IF v_cantidad = 0 THEN
            INSERT INTO inventario_stock (
                insumo_id,
                stock_actual,
                stock_minimo,
                ubicacion
            )
            VALUES (
                p_insumo_id,
                0,
                0,
                'Sin ubicación'
            );
        END IF;
    END asegurar_stock;


    /*
        Procedimiento interno:
        Aplica el efecto del movimiento de inventario sobre el stock.
        ENTRADA aumenta el stock.
        SALIDA disminuye el stock.
        AJUSTE cambia el stock al valor indicado.
    */
    PROCEDURE aplicar_movimiento_stock (
        p_insumo_id IN inventario_stock.insumo_id%TYPE,
        p_tipo_movimiento IN movimientos_inventario.tipo_movimiento%TYPE,
        p_cantidad IN movimientos_inventario.cantidad%TYPE
    ) AS
        v_stock_actual inventario_stock.stock_actual%TYPE;
    BEGIN
        asegurar_stock(p_insumo_id);

        SELECT stock_actual
        INTO v_stock_actual
        FROM inventario_stock
        WHERE insumo_id = p_insumo_id
        FOR UPDATE;

        IF p_tipo_movimiento = 'ENTRADA' THEN
            UPDATE inventario_stock
            SET stock_actual = stock_actual + p_cantidad
            WHERE insumo_id = p_insumo_id;

        ELSIF p_tipo_movimiento = 'SALIDA' THEN
            IF v_stock_actual < p_cantidad THEN
                RAISE_APPLICATION_ERROR(
                    -23001,
                    'No hay suficiente stock para realizar la salida.'
                );
            END IF;

            UPDATE inventario_stock
            SET stock_actual = stock_actual - p_cantidad
            WHERE insumo_id = p_insumo_id;

        ELSIF p_tipo_movimiento = 'AJUSTE' THEN
            UPDATE inventario_stock
            SET stock_actual = p_cantidad
            WHERE insumo_id = p_insumo_id;

        ELSE
            RAISE_APPLICATION_ERROR(
                -23002,
                'Tipo de movimiento inválido. Use ENTRADA, SALIDA o AJUSTE.'
            );
        END IF;
    END aplicar_movimiento_stock;


    /*
        Procedimiento interno:
        Revierte un movimiento cuando se elimina.
        Los ajustes no se revierten porque no sabemos el stock anterior.
    */
    PROCEDURE revertir_movimiento_stock (
        p_insumo_id IN inventario_stock.insumo_id%TYPE,
        p_tipo_movimiento IN movimientos_inventario.tipo_movimiento%TYPE,
        p_cantidad IN movimientos_inventario.cantidad%TYPE
    ) AS
        v_stock_actual inventario_stock.stock_actual%TYPE;
    BEGIN
        asegurar_stock(p_insumo_id);

        SELECT stock_actual
        INTO v_stock_actual
        FROM inventario_stock
        WHERE insumo_id = p_insumo_id
        FOR UPDATE;

        IF p_tipo_movimiento = 'ENTRADA' THEN
            IF v_stock_actual < p_cantidad THEN
                RAISE_APPLICATION_ERROR(
                    -23003,
                    'No se puede revertir la entrada porque el stock quedaría negativo.'
                );
            END IF;

            UPDATE inventario_stock
            SET stock_actual = stock_actual - p_cantidad
            WHERE insumo_id = p_insumo_id;

        ELSIF p_tipo_movimiento = 'SALIDA' THEN
            UPDATE inventario_stock
            SET stock_actual = stock_actual + p_cantidad
            WHERE insumo_id = p_insumo_id;

        ELSIF p_tipo_movimiento = 'AJUSTE' THEN
            RAISE_APPLICATION_ERROR(
                -23004,
                'No se puede eliminar un ajuste porque no se conoce el stock anterior.'
            );

        ELSE
            RAISE_APPLICATION_ERROR(
                -23005,
                'Tipo de movimiento inválido.'
            );
        END IF;
    END revertir_movimiento_stock;


    /*
        ============================================================
        CRUD PROVEEDORES
        ============================================================
    */

    PROCEDURE crear_proveedor (
        p_nombre IN proveedores.nombre%TYPE,
        p_telefono IN proveedores.telefono%TYPE,
        p_correo IN proveedores.correo%TYPE,
        p_direccion IN proveedores.direccion%TYPE,
        p_estado IN proveedores.estado%TYPE,
        p_proveedor_id OUT proveedores.proveedor_id%TYPE
    ) AS
    BEGIN
        INSERT INTO proveedores (
            nombre,
            telefono,
            correo,
            direccion,
            estado
        )
        VALUES (
            p_nombre,
            p_telefono,
            p_correo,
            p_direccion,
            p_estado
        )
        RETURNING proveedor_id INTO p_proveedor_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23999,
                'Error inesperado al crear proveedor: ' || SQLERRM
            );
    END crear_proveedor;


    PROCEDURE actualizar_proveedor (
        p_proveedor_id IN proveedores.proveedor_id%TYPE,
        p_nombre IN proveedores.nombre%TYPE,
        p_telefono IN proveedores.telefono%TYPE,
        p_correo IN proveedores.correo%TYPE,
        p_direccion IN proveedores.direccion%TYPE,
        p_estado IN proveedores.estado%TYPE
    ) AS
    BEGIN
        UPDATE proveedores
        SET
            nombre = p_nombre,
            telefono = p_telefono,
            correo = p_correo,
            direccion = p_direccion,
            estado = p_estado
        WHERE proveedor_id = p_proveedor_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22001,
                'No se encontró el proveedor indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23998,
                'Error inesperado al actualizar proveedor: ' || SQLERRM
            );
    END actualizar_proveedor;


    PROCEDURE eliminar_proveedor (
        p_proveedor_id IN proveedores.proveedor_id%TYPE
    ) AS
    BEGIN
        DELETE FROM proveedores
        WHERE proveedor_id = p_proveedor_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22002,
                'No se encontró el proveedor indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23997,
                'Error inesperado al eliminar proveedor: ' || SQLERRM
            );
    END eliminar_proveedor;


    PROCEDURE listar_proveedores (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                proveedor_id,
                nombre,
                telefono,
                correo,
                direccion,
                estado
            FROM proveedores
            ORDER BY proveedor_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23996,
                'Error inesperado al listar proveedores: ' || SQLERRM
            );
    END listar_proveedores;


    /*
        ============================================================
        CRUD INSUMOS
        ============================================================
    */

    PROCEDURE crear_insumo (
        p_codigo IN insumos.codigo%TYPE,
        p_nombre IN insumos.nombre%TYPE,
        p_descripcion IN insumos.descripcion%TYPE,
        p_unidad_medida IN insumos.unidad_medida%TYPE,
        p_estado IN insumos.estado%TYPE,
        p_insumo_id OUT insumos.insumo_id%TYPE
    ) AS
    BEGIN
        INSERT INTO insumos (
            codigo,
            nombre,
            descripcion,
            unidad_medida,
            estado
        )
        VALUES (
            p_codigo,
            p_nombre,
            p_descripcion,
            p_unidad_medida,
            p_estado
        )
        RETURNING insumo_id INTO p_insumo_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -22101,
                'No se pudo crear el insumo porque el código ya existe.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23995,
                'Error inesperado al crear insumo: ' || SQLERRM
            );
    END crear_insumo;


    PROCEDURE actualizar_insumo (
        p_insumo_id IN insumos.insumo_id%TYPE,
        p_codigo IN insumos.codigo%TYPE,
        p_nombre IN insumos.nombre%TYPE,
        p_descripcion IN insumos.descripcion%TYPE,
        p_unidad_medida IN insumos.unidad_medida%TYPE,
        p_estado IN insumos.estado%TYPE
    ) AS
    BEGIN
        UPDATE insumos
        SET
            codigo = p_codigo,
            nombre = p_nombre,
            descripcion = p_descripcion,
            unidad_medida = p_unidad_medida,
            estado = p_estado
        WHERE insumo_id = p_insumo_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22102,
                'No se encontró el insumo indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23994,
                'Error inesperado al actualizar insumo: ' || SQLERRM
            );
    END actualizar_insumo;


    PROCEDURE eliminar_insumo (
        p_insumo_id IN insumos.insumo_id%TYPE
    ) AS
    BEGIN
        DELETE FROM insumos
        WHERE insumo_id = p_insumo_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22103,
                'No se encontró el insumo indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23993,
                'Error inesperado al eliminar insumo: ' || SQLERRM
            );
    END eliminar_insumo;


    PROCEDURE listar_insumos (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                insumo_id,
                codigo,
                nombre,
                descripcion,
                unidad_medida,
                estado
            FROM insumos
            ORDER BY insumo_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23992,
                'Error inesperado al listar insumos: ' || SQLERRM
            );
    END listar_insumos;


    /*
        ============================================================
        CRUD INVENTARIO_STOCK
        ============================================================
    */

    PROCEDURE crear_stock (
        p_insumo_id IN inventario_stock.insumo_id%TYPE,
        p_stock_actual IN inventario_stock.stock_actual%TYPE,
        p_stock_minimo IN inventario_stock.stock_minimo%TYPE,
        p_ubicacion IN inventario_stock.ubicacion%TYPE,
        p_stock_id OUT inventario_stock.stock_id%TYPE
    ) AS
    BEGIN
        INSERT INTO inventario_stock (
            insumo_id,
            stock_actual,
            stock_minimo,
            ubicacion
        )
        VALUES (
            p_insumo_id,
            p_stock_actual,
            p_stock_minimo,
            p_ubicacion
        )
        RETURNING stock_id INTO p_stock_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -22201,
                'No se pudo crear el stock porque el insumo ya tiene registro de inventario.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23991,
                'Error inesperado al crear stock: ' || SQLERRM
            );
    END crear_stock;


    PROCEDURE actualizar_stock (
        p_stock_id IN inventario_stock.stock_id%TYPE,
        p_insumo_id IN inventario_stock.insumo_id%TYPE,
        p_stock_actual IN inventario_stock.stock_actual%TYPE,
        p_stock_minimo IN inventario_stock.stock_minimo%TYPE,
        p_ubicacion IN inventario_stock.ubicacion%TYPE
    ) AS
    BEGIN
        UPDATE inventario_stock
        SET
            insumo_id = p_insumo_id,
            stock_actual = p_stock_actual,
            stock_minimo = p_stock_minimo,
            ubicacion = p_ubicacion
        WHERE stock_id = p_stock_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22202,
                'No se encontró el registro de stock indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23990,
                'Error inesperado al actualizar stock: ' || SQLERRM
            );
    END actualizar_stock;


    PROCEDURE eliminar_stock (
        p_stock_id IN inventario_stock.stock_id%TYPE
    ) AS
    BEGIN
        DELETE FROM inventario_stock
        WHERE stock_id = p_stock_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22203,
                'No se encontró el registro de stock indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23989,
                'Error inesperado al eliminar stock: ' || SQLERRM
            );
    END eliminar_stock;


    PROCEDURE listar_stock (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                s.stock_id,
                s.insumo_id,
                i.codigo,
                i.nombre AS insumo_nombre,
                s.stock_actual,
                s.stock_minimo,
                s.ubicacion
            FROM inventario_stock s
            INNER JOIN insumos i
                ON s.insumo_id = i.insumo_id
            ORDER BY s.stock_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23988,
                'Error inesperado al listar stock: ' || SQLERRM
            );
    END listar_stock;


    PROCEDURE listar_stock_bajo_minimo (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                s.stock_id,
                s.insumo_id,
                i.codigo,
                i.nombre AS insumo_nombre,
                s.stock_actual,
                s.stock_minimo,
                s.ubicacion
            FROM inventario_stock s
            INNER JOIN insumos i
                ON s.insumo_id = i.insumo_id
            WHERE s.stock_minimo IS NOT NULL
              AND s.stock_actual <= s.stock_minimo
            ORDER BY s.stock_actual ASC;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23987,
                'Error inesperado al listar stock bajo mínimo: ' || SQLERRM
            );
    END listar_stock_bajo_minimo;


    /*
        ============================================================
        CRUD COMPRAS
        ============================================================
    */

    PROCEDURE crear_compra (
        p_proveedor_id IN compras.proveedor_id%TYPE,
        p_usuario_id IN compras.usuario_id%TYPE,
        p_fecha_compra IN compras.fecha_compra%TYPE,
        p_total IN compras.total%TYPE,
        p_estado IN compras.estado%TYPE,
        p_compra_id OUT compras.compra_id%TYPE
    ) AS
    BEGIN
        INSERT INTO compras (
            proveedor_id,
            usuario_id,
            fecha_compra,
            total,
            estado
        )
        VALUES (
            p_proveedor_id,
            p_usuario_id,
            NVL(p_fecha_compra, SYSDATE),
            NVL(p_total, 0),
            p_estado
        )
        RETURNING compra_id INTO p_compra_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23986,
                'Error inesperado al crear compra: ' || SQLERRM
            );
    END crear_compra;


    PROCEDURE actualizar_compra (
        p_compra_id IN compras.compra_id%TYPE,
        p_proveedor_id IN compras.proveedor_id%TYPE,
        p_usuario_id IN compras.usuario_id%TYPE,
        p_fecha_compra IN compras.fecha_compra%TYPE,
        p_total IN compras.total%TYPE,
        p_estado IN compras.estado%TYPE
    ) AS
    BEGIN
        UPDATE compras
        SET
            proveedor_id = p_proveedor_id,
            usuario_id = p_usuario_id,
            fecha_compra = p_fecha_compra,
            total = NVL(p_total, 0),
            estado = p_estado
        WHERE compra_id = p_compra_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22302,
                'No se encontró la compra indicada para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23985,
                'Error inesperado al actualizar compra: ' || SQLERRM
            );
    END actualizar_compra;


    PROCEDURE eliminar_compra (
        p_compra_id IN compras.compra_id%TYPE
    ) AS
    BEGIN
        DELETE FROM compras
        WHERE compra_id = p_compra_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22303,
                'No se encontró la compra indicada para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23984,
                'Error inesperado al eliminar compra: ' || SQLERRM
            );
    END eliminar_compra;


    PROCEDURE listar_compras (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                c.compra_id,
                c.proveedor_id,
                p.nombre AS proveedor_nombre,
                c.usuario_id,
                c.fecha_compra,
                c.total,
                c.estado
            FROM compras c
            INNER JOIN proveedores p
                ON c.proveedor_id = p.proveedor_id
            ORDER BY c.compra_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23983,
                'Error inesperado al listar compras: ' || SQLERRM
            );
    END listar_compras;


    /*
        ============================================================
        CRUD DETALLE_COMPRA
        ============================================================
    */

    PROCEDURE crear_detalle_compra (
        p_compra_id IN detalle_compra.compra_id%TYPE,
        p_insumo_id IN detalle_compra.insumo_id%TYPE,
        p_cantidad IN detalle_compra.cantidad%TYPE,
        p_costo_unitario IN detalle_compra.costo_unitario%TYPE,
        p_detalle_compra_id OUT detalle_compra.detalle_compra_id%TYPE
    ) AS
        v_subtotal detalle_compra.subtotal%TYPE;
    BEGIN
        v_subtotal := NVL(p_cantidad, 0) * NVL(p_costo_unitario, 0);

        INSERT INTO detalle_compra (
            compra_id,
            insumo_id,
            cantidad,
            costo_unitario,
            subtotal
        )
        VALUES (
            p_compra_id,
            p_insumo_id,
            p_cantidad,
            p_costo_unitario,
            v_subtotal
        )
        RETURNING detalle_compra_id INTO p_detalle_compra_id;

        recalcular_total_compra(p_compra_id);

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23982,
                'Error inesperado al crear detalle de compra: ' || SQLERRM
            );
    END crear_detalle_compra;


    PROCEDURE actualizar_detalle_compra (
        p_detalle_compra_id IN detalle_compra.detalle_compra_id%TYPE,
        p_compra_id IN detalle_compra.compra_id%TYPE,
        p_insumo_id IN detalle_compra.insumo_id%TYPE,
        p_cantidad IN detalle_compra.cantidad%TYPE,
        p_costo_unitario IN detalle_compra.costo_unitario%TYPE
    ) AS
        v_subtotal detalle_compra.subtotal%TYPE;
        v_compra_anterior detalle_compra.compra_id%TYPE;
    BEGIN
        SELECT compra_id
        INTO v_compra_anterior
        FROM detalle_compra
        WHERE detalle_compra_id = p_detalle_compra_id;

        v_subtotal := NVL(p_cantidad, 0) * NVL(p_costo_unitario, 0);

        UPDATE detalle_compra
        SET
            compra_id = p_compra_id,
            insumo_id = p_insumo_id,
            cantidad = p_cantidad,
            costo_unitario = p_costo_unitario,
            subtotal = v_subtotal
        WHERE detalle_compra_id = p_detalle_compra_id;

        recalcular_total_compra(v_compra_anterior);

        IF v_compra_anterior <> p_compra_id THEN
            recalcular_total_compra(p_compra_id);
        END IF;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(
                -22401,
                'No se encontró el detalle de compra indicado para actualizar.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23981,
                'Error inesperado al actualizar detalle de compra: ' || SQLERRM
            );
    END actualizar_detalle_compra;


    PROCEDURE eliminar_detalle_compra (
        p_detalle_compra_id IN detalle_compra.detalle_compra_id%TYPE
    ) AS
        v_compra_id detalle_compra.compra_id%TYPE;
    BEGIN
        SELECT compra_id
        INTO v_compra_id
        FROM detalle_compra
        WHERE detalle_compra_id = p_detalle_compra_id;

        DELETE FROM detalle_compra
        WHERE detalle_compra_id = p_detalle_compra_id;

        recalcular_total_compra(v_compra_id);

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(
                -22402,
                'No se encontró el detalle de compra indicado para eliminar.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23980,
                'Error inesperado al eliminar detalle de compra: ' || SQLERRM
            );
    END eliminar_detalle_compra;


    PROCEDURE listar_detalles_compra (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                dc.detalle_compra_id,
                dc.compra_id,
                dc.insumo_id,
                i.codigo,
                i.nombre AS insumo_nombre,
                dc.cantidad,
                dc.costo_unitario,
                dc.subtotal
            FROM detalle_compra dc
            INNER JOIN insumos i
                ON dc.insumo_id = i.insumo_id
            ORDER BY dc.detalle_compra_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23979,
                'Error inesperado al listar detalles de compra: ' || SQLERRM
            );
    END listar_detalles_compra;


    PROCEDURE listar_detalles_por_compra (
        p_compra_id IN detalle_compra.compra_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                dc.detalle_compra_id,
                dc.compra_id,
                dc.insumo_id,
                i.codigo,
                i.nombre AS insumo_nombre,
                dc.cantidad,
                dc.costo_unitario,
                dc.subtotal
            FROM detalle_compra dc
            INNER JOIN insumos i
                ON dc.insumo_id = i.insumo_id
            WHERE dc.compra_id = p_compra_id
            ORDER BY dc.detalle_compra_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23978,
                'Error inesperado al listar detalles por compra: ' || SQLERRM
            );
    END listar_detalles_por_compra;


    /*
        ============================================================
        CRUD MOVIMIENTOS_INVENTARIO
        ============================================================
    */

    PROCEDURE crear_movimiento_inventario (
        p_insumo_id IN movimientos_inventario.insumo_id%TYPE,
        p_usuario_id IN movimientos_inventario.usuario_id%TYPE,
        p_detalle_compra_id IN movimientos_inventario.detalle_compra_id%TYPE,
        p_consulta_id IN movimientos_inventario.consulta_id%TYPE,
        p_tipo_movimiento IN movimientos_inventario.tipo_movimiento%TYPE,
        p_cantidad IN movimientos_inventario.cantidad%TYPE,
        p_fecha_movimiento IN movimientos_inventario.fecha_movimiento%TYPE,
        p_motivo IN movimientos_inventario.motivo%TYPE,
        p_movimiento_id OUT movimientos_inventario.movimiento_id%TYPE
    ) AS
    BEGIN
        aplicar_movimiento_stock(
            p_insumo_id,
            p_tipo_movimiento,
            p_cantidad
        );

        INSERT INTO movimientos_inventario (
            insumo_id,
            usuario_id,
            detalle_compra_id,
            consulta_id,
            tipo_movimiento,
            cantidad,
            fecha_movimiento,
            motivo
        )
        VALUES (
            p_insumo_id,
            p_usuario_id,
            p_detalle_compra_id,
            p_consulta_id,
            p_tipo_movimiento,
            p_cantidad,
            NVL(p_fecha_movimiento, SYSDATE),
            p_motivo
        )
        RETURNING movimiento_id INTO p_movimiento_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23977,
                'Error inesperado al crear movimiento de inventario: ' || SQLERRM
            );
    END crear_movimiento_inventario;


    /*
        Importante:
        Este UPDATE no permite cambiar insumo_id, tipo_movimiento ni cantidad.
        Eso se hace para no dañar el historial ni corromper el cálculo de stock.
        Solamente actualiza datos administrativos del movimiento.
    */
    PROCEDURE actualizar_movimiento_inventario (
        p_movimiento_id IN movimientos_inventario.movimiento_id%TYPE,
        p_usuario_id IN movimientos_inventario.usuario_id%TYPE,
        p_detalle_compra_id IN movimientos_inventario.detalle_compra_id%TYPE,
        p_consulta_id IN movimientos_inventario.consulta_id%TYPE,
        p_fecha_movimiento IN movimientos_inventario.fecha_movimiento%TYPE,
        p_motivo IN movimientos_inventario.motivo%TYPE
    ) AS
    BEGIN
        UPDATE movimientos_inventario
        SET
            usuario_id = p_usuario_id,
            detalle_compra_id = p_detalle_compra_id,
            consulta_id = p_consulta_id,
            fecha_movimiento = p_fecha_movimiento,
            motivo = p_motivo
        WHERE movimiento_id = p_movimiento_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -22501,
                'No se encontró el movimiento de inventario indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23976,
                'Error inesperado al actualizar movimiento de inventario: ' || SQLERRM
            );
    END actualizar_movimiento_inventario;


    PROCEDURE eliminar_movimiento_inventario (
        p_movimiento_id IN movimientos_inventario.movimiento_id%TYPE
    ) AS
        v_insumo_id movimientos_inventario.insumo_id%TYPE;
        v_tipo_movimiento movimientos_inventario.tipo_movimiento%TYPE;
        v_cantidad movimientos_inventario.cantidad%TYPE;
    BEGIN
        SELECT
            insumo_id,
            tipo_movimiento,
            cantidad
        INTO
            v_insumo_id,
            v_tipo_movimiento,
            v_cantidad
        FROM movimientos_inventario
        WHERE movimiento_id = p_movimiento_id;

        revertir_movimiento_stock(
            v_insumo_id,
            v_tipo_movimiento,
            v_cantidad
        );

        DELETE FROM movimientos_inventario
        WHERE movimiento_id = p_movimiento_id;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(
                -22502,
                'No se encontró el movimiento de inventario indicado para eliminar.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23975,
                'Error inesperado al eliminar movimiento de inventario: ' || SQLERRM
            );
    END eliminar_movimiento_inventario;


    PROCEDURE listar_movimientos_inventario (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                mi.movimiento_id,
                mi.insumo_id,
                i.codigo,
                i.nombre AS insumo_nombre,
                mi.usuario_id,
                mi.detalle_compra_id,
                mi.consulta_id,
                mi.tipo_movimiento,
                mi.cantidad,
                mi.fecha_movimiento,
                mi.motivo
            FROM movimientos_inventario mi
            INNER JOIN insumos i
                ON mi.insumo_id = i.insumo_id
            ORDER BY mi.movimiento_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23974,
                'Error inesperado al listar movimientos de inventario: ' || SQLERRM
            );
    END listar_movimientos_inventario;


    PROCEDURE listar_movimientos_por_insumo (
        p_insumo_id IN movimientos_inventario.insumo_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                mi.movimiento_id,
                mi.insumo_id,
                i.codigo,
                i.nombre AS insumo_nombre,
                mi.usuario_id,
                mi.detalle_compra_id,
                mi.consulta_id,
                mi.tipo_movimiento,
                mi.cantidad,
                mi.fecha_movimiento,
                mi.motivo
            FROM movimientos_inventario mi
            INNER JOIN insumos i
                ON mi.insumo_id = i.insumo_id
            WHERE mi.insumo_id = p_insumo_id
            ORDER BY mi.fecha_movimiento DESC;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -23973,
                'Error inesperado al listar movimientos por insumo: ' || SQLERRM
            );
    END listar_movimientos_por_insumo;

END pkg_smilecare_crud_inventario;
/

SHOW ERRORS PACKAGE BODY pkg_smilecare_crud_inventario;


PROMPT ============================================================
PROMPT VERIFICANDO ESTADO DEL PAQUETE
PROMPT ============================================================

SELECT
    object_name,
    object_type,
    status
FROM user_objects
WHERE object_name = 'PKG_SMILECARE_CRUD_INVENTARIO'
ORDER BY object_type;