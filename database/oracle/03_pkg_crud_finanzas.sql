SET SERVEROUTPUT ON;

PROMPT ============================================================
PROMPT PAQUETE CRUD FINANZAS - SMILECARE
PROMPT ============================================================

/*
    Archivo: 03_pkg_crud_finanzas.sql
    Proyecto: SmileCare
    Curso: SC-504 Lenguajes de Base de Datos

    Objetivo:
    Crear un paquete Oracle con procedimientos CRUD para el área financiera
    del sistema.

    Tablas incluidas:
    - FACTURAS
    - DETALLE_FACTURA
    - METODOS_PAGO
    - PAGOS
    - COMPROBANTES
*/

CREATE OR REPLACE PACKAGE pkg_smilecare_crud_finanzas AS

    /*
        ============================================================
        CRUD FACTURAS
        ============================================================
    */

    PROCEDURE crear_factura (
        p_paciente_id IN facturas.paciente_id%TYPE,
        p_consulta_id IN facturas.consulta_id%TYPE,
        p_numero_factura IN facturas.numero_factura%TYPE,
        p_fecha_emision IN facturas.fecha_emision%TYPE,
        p_subtotal IN facturas.subtotal%TYPE,
        p_impuesto IN facturas.impuesto%TYPE,
        p_estado IN facturas.estado%TYPE,
        p_factura_id OUT facturas.factura_id%TYPE
    );

    PROCEDURE actualizar_factura (
        p_factura_id IN facturas.factura_id%TYPE,
        p_paciente_id IN facturas.paciente_id%TYPE,
        p_consulta_id IN facturas.consulta_id%TYPE,
        p_numero_factura IN facturas.numero_factura%TYPE,
        p_fecha_emision IN facturas.fecha_emision%TYPE,
        p_subtotal IN facturas.subtotal%TYPE,
        p_impuesto IN facturas.impuesto%TYPE,
        p_estado IN facturas.estado%TYPE
    );

    PROCEDURE eliminar_factura (
        p_factura_id IN facturas.factura_id%TYPE
    );

    PROCEDURE listar_facturas (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD DETALLE_FACTURA
        ============================================================
    */

    PROCEDURE crear_detalle_factura (
        p_factura_id IN detalle_factura.factura_id%TYPE,
        p_tratamiento_consulta_id IN detalle_factura.tratamiento_consulta_id%TYPE,
        p_descripcion IN detalle_factura.descripcion%TYPE,
        p_cantidad IN detalle_factura.cantidad%TYPE,
        p_precio_unitario IN detalle_factura.precio_unitario%TYPE,
        p_detalle_factura_id OUT detalle_factura.detalle_factura_id%TYPE
    );

    PROCEDURE actualizar_detalle_factura (
        p_detalle_factura_id IN detalle_factura.detalle_factura_id%TYPE,
        p_factura_id IN detalle_factura.factura_id%TYPE,
        p_tratamiento_consulta_id IN detalle_factura.tratamiento_consulta_id%TYPE,
        p_descripcion IN detalle_factura.descripcion%TYPE,
        p_cantidad IN detalle_factura.cantidad%TYPE,
        p_precio_unitario IN detalle_factura.precio_unitario%TYPE
    );

    PROCEDURE eliminar_detalle_factura (
        p_detalle_factura_id IN detalle_factura.detalle_factura_id%TYPE
    );

    PROCEDURE listar_detalles_factura (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_detalles_por_factura (
        p_factura_id IN detalle_factura.factura_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD METODOS_PAGO
        ============================================================
    */

    PROCEDURE crear_metodo_pago (
        p_nombre IN metodos_pago.nombre%TYPE,
        p_descripcion IN metodos_pago.descripcion%TYPE,
        p_estado IN metodos_pago.estado%TYPE,
        p_metodo_pago_id OUT metodos_pago.metodo_pago_id%TYPE
    );

    PROCEDURE actualizar_metodo_pago (
        p_metodo_pago_id IN metodos_pago.metodo_pago_id%TYPE,
        p_nombre IN metodos_pago.nombre%TYPE,
        p_descripcion IN metodos_pago.descripcion%TYPE,
        p_estado IN metodos_pago.estado%TYPE
    );

    PROCEDURE eliminar_metodo_pago (
        p_metodo_pago_id IN metodos_pago.metodo_pago_id%TYPE
    );

    PROCEDURE listar_metodos_pago (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD PAGOS
        ============================================================
    */

    PROCEDURE crear_pago (
        p_factura_id IN pagos.factura_id%TYPE,
        p_metodo_pago_id IN pagos.metodo_pago_id%TYPE,
        p_monto IN pagos.monto%TYPE,
        p_fecha_pago IN pagos.fecha_pago%TYPE,
        p_numero_referencia IN pagos.numero_referencia%TYPE,
        p_estado IN pagos.estado%TYPE,
        p_pago_id OUT pagos.pago_id%TYPE
    );

    PROCEDURE actualizar_pago (
        p_pago_id IN pagos.pago_id%TYPE,
        p_factura_id IN pagos.factura_id%TYPE,
        p_metodo_pago_id IN pagos.metodo_pago_id%TYPE,
        p_monto IN pagos.monto%TYPE,
        p_fecha_pago IN pagos.fecha_pago%TYPE,
        p_numero_referencia IN pagos.numero_referencia%TYPE,
        p_estado IN pagos.estado%TYPE
    );

    PROCEDURE eliminar_pago (
        p_pago_id IN pagos.pago_id%TYPE
    );

    PROCEDURE listar_pagos (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_pagos_por_factura (
        p_factura_id IN pagos.factura_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD COMPROBANTES
        ============================================================
    */

    PROCEDURE crear_comprobante (
        p_pago_id IN comprobantes.pago_id%TYPE,
        p_numero_comprobante IN comprobantes.numero_comprobante%TYPE,
        p_tipo_comprobante IN comprobantes.tipo_comprobante%TYPE,
        p_fecha_emision IN comprobantes.fecha_emision%TYPE,
        p_detalle IN comprobantes.detalle%TYPE,
        p_comprobante_id OUT comprobantes.comprobante_id%TYPE
    );

    PROCEDURE actualizar_comprobante (
        p_comprobante_id IN comprobantes.comprobante_id%TYPE,
        p_pago_id IN comprobantes.pago_id%TYPE,
        p_numero_comprobante IN comprobantes.numero_comprobante%TYPE,
        p_tipo_comprobante IN comprobantes.tipo_comprobante%TYPE,
        p_fecha_emision IN comprobantes.fecha_emision%TYPE,
        p_detalle IN comprobantes.detalle%TYPE
    );

    PROCEDURE eliminar_comprobante (
        p_comprobante_id IN comprobantes.comprobante_id%TYPE
    );

    PROCEDURE listar_comprobantes (
        p_resultado OUT SYS_REFCURSOR
    );

END pkg_smilecare_crud_finanzas;
/

SHOW ERRORS PACKAGE pkg_smilecare_crud_finanzas;


CREATE OR REPLACE PACKAGE BODY pkg_smilecare_crud_finanzas AS

    /*
        Procedimiento interno:
        Recalcula subtotal y total de una factura usando sus detalles.
    */
    PROCEDURE recalcular_total_factura (
        p_factura_id IN facturas.factura_id%TYPE
    ) AS
        v_subtotal facturas.subtotal%TYPE;
        v_impuesto facturas.impuesto%TYPE;
    BEGIN
        SELECT NVL(SUM(subtotal), 0)
        INTO v_subtotal
        FROM detalle_factura
        WHERE factura_id = p_factura_id;

        SELECT NVL(impuesto, 0)
        INTO v_impuesto
        FROM facturas
        WHERE factura_id = p_factura_id;

        UPDATE facturas
        SET
            subtotal = v_subtotal,
            total = v_subtotal + v_impuesto
        WHERE factura_id = p_factura_id;
    END recalcular_total_factura;


    /*
        ============================================================
        CRUD FACTURAS
        ============================================================
    */

    PROCEDURE crear_factura (
        p_paciente_id IN facturas.paciente_id%TYPE,
        p_consulta_id IN facturas.consulta_id%TYPE,
        p_numero_factura IN facturas.numero_factura%TYPE,
        p_fecha_emision IN facturas.fecha_emision%TYPE,
        p_subtotal IN facturas.subtotal%TYPE,
        p_impuesto IN facturas.impuesto%TYPE,
        p_estado IN facturas.estado%TYPE,
        p_factura_id OUT facturas.factura_id%TYPE
    ) AS
        v_total facturas.total%TYPE;
    BEGIN
        v_total := NVL(p_subtotal, 0) + NVL(p_impuesto, 0);

        INSERT INTO facturas (
            paciente_id,
            consulta_id,
            numero_factura,
            fecha_emision,
            subtotal,
            impuesto,
            total,
            estado
        )
        VALUES (
            p_paciente_id,
            p_consulta_id,
            p_numero_factura,
            NVL(p_fecha_emision, SYSDATE),
            NVL(p_subtotal, 0),
            NVL(p_impuesto, 0),
            v_total,
            p_estado
        )
        RETURNING factura_id INTO p_factura_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -21001,
                'No se pudo crear la factura porque el número de factura o la consulta ya existen.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21999,
                'Error inesperado al crear factura: ' || SQLERRM
            );
    END crear_factura;


    PROCEDURE actualizar_factura (
        p_factura_id IN facturas.factura_id%TYPE,
        p_paciente_id IN facturas.paciente_id%TYPE,
        p_consulta_id IN facturas.consulta_id%TYPE,
        p_numero_factura IN facturas.numero_factura%TYPE,
        p_fecha_emision IN facturas.fecha_emision%TYPE,
        p_subtotal IN facturas.subtotal%TYPE,
        p_impuesto IN facturas.impuesto%TYPE,
        p_estado IN facturas.estado%TYPE
    ) AS
        v_total facturas.total%TYPE;
    BEGIN
        v_total := NVL(p_subtotal, 0) + NVL(p_impuesto, 0);

        UPDATE facturas
        SET
            paciente_id = p_paciente_id,
            consulta_id = p_consulta_id,
            numero_factura = p_numero_factura,
            fecha_emision = p_fecha_emision,
            subtotal = NVL(p_subtotal, 0),
            impuesto = NVL(p_impuesto, 0),
            total = v_total,
            estado = p_estado
        WHERE factura_id = p_factura_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21002,
                'No se encontró la factura indicada para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21998,
                'Error inesperado al actualizar factura: ' || SQLERRM
            );
    END actualizar_factura;


    PROCEDURE eliminar_factura (
        p_factura_id IN facturas.factura_id%TYPE
    ) AS
    BEGIN
        DELETE FROM facturas
        WHERE factura_id = p_factura_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21003,
                'No se encontró la factura indicada para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21997,
                'Error inesperado al eliminar factura: ' || SQLERRM
            );
    END eliminar_factura;


    PROCEDURE listar_facturas (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                f.factura_id,
                f.paciente_id,
                p.nombre || ' ' || p.apellido AS paciente_nombre,
                f.consulta_id,
                f.numero_factura,
                f.fecha_emision,
                f.subtotal,
                f.impuesto,
                f.total,
                f.estado
            FROM facturas f
            INNER JOIN pacientes p
                ON f.paciente_id = p.paciente_id
            ORDER BY f.factura_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21996,
                'Error inesperado al listar facturas: ' || SQLERRM
            );
    END listar_facturas;


    /*
        ============================================================
        CRUD DETALLE_FACTURA
        ============================================================
    */

    PROCEDURE crear_detalle_factura (
        p_factura_id IN detalle_factura.factura_id%TYPE,
        p_tratamiento_consulta_id IN detalle_factura.tratamiento_consulta_id%TYPE,
        p_descripcion IN detalle_factura.descripcion%TYPE,
        p_cantidad IN detalle_factura.cantidad%TYPE,
        p_precio_unitario IN detalle_factura.precio_unitario%TYPE,
        p_detalle_factura_id OUT detalle_factura.detalle_factura_id%TYPE
    ) AS
        v_subtotal detalle_factura.subtotal%TYPE;
    BEGIN
        v_subtotal := NVL(p_cantidad, 0) * NVL(p_precio_unitario, 0);

        INSERT INTO detalle_factura (
            factura_id,
            tratamiento_consulta_id,
            descripcion,
            cantidad,
            precio_unitario,
            subtotal
        )
        VALUES (
            p_factura_id,
            p_tratamiento_consulta_id,
            p_descripcion,
            p_cantidad,
            p_precio_unitario,
            v_subtotal
        )
        RETURNING detalle_factura_id INTO p_detalle_factura_id;

        recalcular_total_factura(p_factura_id);

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21995,
                'Error inesperado al crear detalle de factura: ' || SQLERRM
            );
    END crear_detalle_factura;


    PROCEDURE actualizar_detalle_factura (
        p_detalle_factura_id IN detalle_factura.detalle_factura_id%TYPE,
        p_factura_id IN detalle_factura.factura_id%TYPE,
        p_tratamiento_consulta_id IN detalle_factura.tratamiento_consulta_id%TYPE,
        p_descripcion IN detalle_factura.descripcion%TYPE,
        p_cantidad IN detalle_factura.cantidad%TYPE,
        p_precio_unitario IN detalle_factura.precio_unitario%TYPE
    ) AS
        v_subtotal detalle_factura.subtotal%TYPE;
        v_factura_anterior detalle_factura.factura_id%TYPE;
    BEGIN
        SELECT factura_id
        INTO v_factura_anterior
        FROM detalle_factura
        WHERE detalle_factura_id = p_detalle_factura_id;

        v_subtotal := NVL(p_cantidad, 0) * NVL(p_precio_unitario, 0);

        UPDATE detalle_factura
        SET
            factura_id = p_factura_id,
            tratamiento_consulta_id = p_tratamiento_consulta_id,
            descripcion = p_descripcion,
            cantidad = p_cantidad,
            precio_unitario = p_precio_unitario,
            subtotal = v_subtotal
        WHERE detalle_factura_id = p_detalle_factura_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21102,
                'No se encontró el detalle de factura indicado para actualizar.'
            );
        END IF;

        recalcular_total_factura(v_factura_anterior);

        IF v_factura_anterior <> p_factura_id THEN
            recalcular_total_factura(p_factura_id);
        END IF;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(
                -21103,
                'No se encontró el detalle de factura indicado.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21994,
                'Error inesperado al actualizar detalle de factura: ' || SQLERRM
            );
    END actualizar_detalle_factura;


    PROCEDURE eliminar_detalle_factura (
        p_detalle_factura_id IN detalle_factura.detalle_factura_id%TYPE
    ) AS
        v_factura_id detalle_factura.factura_id%TYPE;
    BEGIN
        SELECT factura_id
        INTO v_factura_id
        FROM detalle_factura
        WHERE detalle_factura_id = p_detalle_factura_id;

        DELETE FROM detalle_factura
        WHERE detalle_factura_id = p_detalle_factura_id;

        recalcular_total_factura(v_factura_id);

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(
                -21104,
                'No se encontró el detalle de factura indicado para eliminar.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21993,
                'Error inesperado al eliminar detalle de factura: ' || SQLERRM
            );
    END eliminar_detalle_factura;


    PROCEDURE listar_detalles_factura (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                df.detalle_factura_id,
                df.factura_id,
                f.numero_factura,
                df.tratamiento_consulta_id,
                df.descripcion,
                df.cantidad,
                df.precio_unitario,
                df.subtotal
            FROM detalle_factura df
            INNER JOIN facturas f
                ON df.factura_id = f.factura_id
            ORDER BY df.detalle_factura_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21992,
                'Error inesperado al listar detalles de factura: ' || SQLERRM
            );
    END listar_detalles_factura;


    PROCEDURE listar_detalles_por_factura (
        p_factura_id IN detalle_factura.factura_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                detalle_factura_id,
                factura_id,
                tratamiento_consulta_id,
                descripcion,
                cantidad,
                precio_unitario,
                subtotal
            FROM detalle_factura
            WHERE factura_id = p_factura_id
            ORDER BY detalle_factura_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21991,
                'Error inesperado al listar detalles por factura: ' || SQLERRM
            );
    END listar_detalles_por_factura;


    /*
        ============================================================
        CRUD METODOS_PAGO
        ============================================================
    */

    PROCEDURE crear_metodo_pago (
        p_nombre IN metodos_pago.nombre%TYPE,
        p_descripcion IN metodos_pago.descripcion%TYPE,
        p_estado IN metodos_pago.estado%TYPE,
        p_metodo_pago_id OUT metodos_pago.metodo_pago_id%TYPE
    ) AS
    BEGIN
        INSERT INTO metodos_pago (
            nombre,
            descripcion,
            estado
        )
        VALUES (
            p_nombre,
            p_descripcion,
            p_estado
        )
        RETURNING metodo_pago_id INTO p_metodo_pago_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -21201,
                'No se pudo crear el método de pago porque ya existe.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21990,
                'Error inesperado al crear método de pago: ' || SQLERRM
            );
    END crear_metodo_pago;


    PROCEDURE actualizar_metodo_pago (
        p_metodo_pago_id IN metodos_pago.metodo_pago_id%TYPE,
        p_nombre IN metodos_pago.nombre%TYPE,
        p_descripcion IN metodos_pago.descripcion%TYPE,
        p_estado IN metodos_pago.estado%TYPE
    ) AS
    BEGIN
        UPDATE metodos_pago
        SET
            nombre = p_nombre,
            descripcion = p_descripcion,
            estado = p_estado
        WHERE metodo_pago_id = p_metodo_pago_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21202,
                'No se encontró el método de pago indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21989,
                'Error inesperado al actualizar método de pago: ' || SQLERRM
            );
    END actualizar_metodo_pago;


    PROCEDURE eliminar_metodo_pago (
        p_metodo_pago_id IN metodos_pago.metodo_pago_id%TYPE
    ) AS
    BEGIN
        DELETE FROM metodos_pago
        WHERE metodo_pago_id = p_metodo_pago_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21203,
                'No se encontró el método de pago indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21988,
                'Error inesperado al eliminar método de pago: ' || SQLERRM
            );
    END eliminar_metodo_pago;


    PROCEDURE listar_metodos_pago (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                metodo_pago_id,
                nombre,
                descripcion,
                estado
            FROM metodos_pago
            ORDER BY metodo_pago_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21987,
                'Error inesperado al listar métodos de pago: ' || SQLERRM
            );
    END listar_metodos_pago;


    /*
        ============================================================
        CRUD PAGOS
        ============================================================
    */

    PROCEDURE crear_pago (
        p_factura_id IN pagos.factura_id%TYPE,
        p_metodo_pago_id IN pagos.metodo_pago_id%TYPE,
        p_monto IN pagos.monto%TYPE,
        p_fecha_pago IN pagos.fecha_pago%TYPE,
        p_numero_referencia IN pagos.numero_referencia%TYPE,
        p_estado IN pagos.estado%TYPE,
        p_pago_id OUT pagos.pago_id%TYPE
    ) AS
    BEGIN
        INSERT INTO pagos (
            factura_id,
            metodo_pago_id,
            monto,
            fecha_pago,
            numero_referencia,
            estado
        )
        VALUES (
            p_factura_id,
            p_metodo_pago_id,
            p_monto,
            NVL(p_fecha_pago, SYSDATE),
            p_numero_referencia,
            p_estado
        )
        RETURNING pago_id INTO p_pago_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21986,
                'Error inesperado al crear pago: ' || SQLERRM
            );
    END crear_pago;


    PROCEDURE actualizar_pago (
        p_pago_id IN pagos.pago_id%TYPE,
        p_factura_id IN pagos.factura_id%TYPE,
        p_metodo_pago_id IN pagos.metodo_pago_id%TYPE,
        p_monto IN pagos.monto%TYPE,
        p_fecha_pago IN pagos.fecha_pago%TYPE,
        p_numero_referencia IN pagos.numero_referencia%TYPE,
        p_estado IN pagos.estado%TYPE
    ) AS
    BEGIN
        UPDATE pagos
        SET
            factura_id = p_factura_id,
            metodo_pago_id = p_metodo_pago_id,
            monto = p_monto,
            fecha_pago = p_fecha_pago,
            numero_referencia = p_numero_referencia,
            estado = p_estado
        WHERE pago_id = p_pago_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21302,
                'No se encontró el pago indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21985,
                'Error inesperado al actualizar pago: ' || SQLERRM
            );
    END actualizar_pago;


    PROCEDURE eliminar_pago (
        p_pago_id IN pagos.pago_id%TYPE
    ) AS
    BEGIN
        DELETE FROM pagos
        WHERE pago_id = p_pago_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21303,
                'No se encontró el pago indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21984,
                'Error inesperado al eliminar pago: ' || SQLERRM
            );
    END eliminar_pago;


    PROCEDURE listar_pagos (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                p.pago_id,
                p.factura_id,
                f.numero_factura,
                p.metodo_pago_id,
                mp.nombre AS metodo_pago_nombre,
                p.monto,
                p.fecha_pago,
                p.numero_referencia,
                p.estado
            FROM pagos p
            INNER JOIN facturas f
                ON p.factura_id = f.factura_id
            INNER JOIN metodos_pago mp
                ON p.metodo_pago_id = mp.metodo_pago_id
            ORDER BY p.pago_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21983,
                'Error inesperado al listar pagos: ' || SQLERRM
            );
    END listar_pagos;


    PROCEDURE listar_pagos_por_factura (
        p_factura_id IN pagos.factura_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                p.pago_id,
                p.factura_id,
                f.numero_factura,
                p.metodo_pago_id,
                mp.nombre AS metodo_pago_nombre,
                p.monto,
                p.fecha_pago,
                p.numero_referencia,
                p.estado
            FROM pagos p
            INNER JOIN facturas f
                ON p.factura_id = f.factura_id
            INNER JOIN metodos_pago mp
                ON p.metodo_pago_id = mp.metodo_pago_id
            WHERE p.factura_id = p_factura_id
            ORDER BY p.pago_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21982,
                'Error inesperado al listar pagos por factura: ' || SQLERRM
            );
    END listar_pagos_por_factura;


    /*
        ============================================================
        CRUD COMPROBANTES
        ============================================================
    */

    PROCEDURE crear_comprobante (
        p_pago_id IN comprobantes.pago_id%TYPE,
        p_numero_comprobante IN comprobantes.numero_comprobante%TYPE,
        p_tipo_comprobante IN comprobantes.tipo_comprobante%TYPE,
        p_fecha_emision IN comprobantes.fecha_emision%TYPE,
        p_detalle IN comprobantes.detalle%TYPE,
        p_comprobante_id OUT comprobantes.comprobante_id%TYPE
    ) AS
    BEGIN
        INSERT INTO comprobantes (
            pago_id,
            numero_comprobante,
            tipo_comprobante,
            fecha_emision,
            detalle
        )
        VALUES (
            p_pago_id,
            p_numero_comprobante,
            p_tipo_comprobante,
            NVL(p_fecha_emision, SYSDATE),
            p_detalle
        )
        RETURNING comprobante_id INTO p_comprobante_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -21401,
                'No se pudo crear el comprobante porque el pago o número de comprobante ya existen.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21981,
                'Error inesperado al crear comprobante: ' || SQLERRM
            );
    END crear_comprobante;


    PROCEDURE actualizar_comprobante (
        p_comprobante_id IN comprobantes.comprobante_id%TYPE,
        p_pago_id IN comprobantes.pago_id%TYPE,
        p_numero_comprobante IN comprobantes.numero_comprobante%TYPE,
        p_tipo_comprobante IN comprobantes.tipo_comprobante%TYPE,
        p_fecha_emision IN comprobantes.fecha_emision%TYPE,
        p_detalle IN comprobantes.detalle%TYPE
    ) AS
    BEGIN
        UPDATE comprobantes
        SET
            pago_id = p_pago_id,
            numero_comprobante = p_numero_comprobante,
            tipo_comprobante = p_tipo_comprobante,
            fecha_emision = p_fecha_emision,
            detalle = p_detalle
        WHERE comprobante_id = p_comprobante_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21402,
                'No se encontró el comprobante indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21980,
                'Error inesperado al actualizar comprobante: ' || SQLERRM
            );
    END actualizar_comprobante;


    PROCEDURE eliminar_comprobante (
        p_comprobante_id IN comprobantes.comprobante_id%TYPE
    ) AS
    BEGIN
        DELETE FROM comprobantes
        WHERE comprobante_id = p_comprobante_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -21403,
                'No se encontró el comprobante indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21979,
                'Error inesperado al eliminar comprobante: ' || SQLERRM
            );
    END eliminar_comprobante;


    PROCEDURE listar_comprobantes (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                c.comprobante_id,
                c.pago_id,
                p.factura_id,
                f.numero_factura,
                p.monto,
                c.numero_comprobante,
                c.tipo_comprobante,
                c.fecha_emision,
                c.detalle
            FROM comprobantes c
            INNER JOIN pagos p
                ON c.pago_id = p.pago_id
            INNER JOIN facturas f
                ON p.factura_id = f.factura_id
            ORDER BY c.comprobante_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -21978,
                'Error inesperado al listar comprobantes: ' || SQLERRM
            );
    END listar_comprobantes;

END pkg_smilecare_crud_finanzas;
/

SHOW ERRORS PACKAGE BODY pkg_smilecare_crud_finanzas;


PROMPT ============================================================
PROMPT VERIFICANDO ESTADO DEL PAQUETE
PROMPT ============================================================

SELECT
    object_name,
    object_type,
    status
FROM user_objects
WHERE object_name = 'PKG_SMILECARE_CRUD_FINANZAS'
ORDER BY object_type;