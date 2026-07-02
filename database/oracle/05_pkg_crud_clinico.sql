SET SERVEROUTPUT ON;

PROMPT ============================================================
PROMPT PAQUETE CRUD CLINICO - SMILECARE
PROMPT ============================================================

/*
    Archivo: 05_pkg_crud_clinico.sql
    Proyecto: SmileCare
    Curso: SC-504 Lenguajes de Base de Datos

    Objetivo:
    Crear un paquete Oracle con procedimientos CRUD para el área clínica
    y de agenda del sistema.

    Tablas incluidas:
    - CONSULTAS
    - TRATAMIENTOS
    - TRATAMIENTOS_CONSULTA
    - HISTORIAL_MEDICO
    - CIRUGIAS
    - HORARIOS_DOCTORES
    - DISPONIBILIDAD_DOCTORES
*/

CREATE OR REPLACE PACKAGE pkg_smilecare_crud_clinico AS

    /*
        ============================================================
        CRUD CONSULTAS
        ============================================================
    */

    PROCEDURE crear_consulta (
        p_cita_id IN consultas.cita_id%TYPE,
        p_diagnostico IN consultas.diagnostico%TYPE,
        p_observaciones IN consultas.observaciones%TYPE,
        p_fecha_atencion IN consultas.fecha_atencion%TYPE,
        p_consulta_id OUT consultas.consulta_id%TYPE
    );

    PROCEDURE actualizar_consulta (
        p_consulta_id IN consultas.consulta_id%TYPE,
        p_cita_id IN consultas.cita_id%TYPE,
        p_diagnostico IN consultas.diagnostico%TYPE,
        p_observaciones IN consultas.observaciones%TYPE,
        p_fecha_atencion IN consultas.fecha_atencion%TYPE
    );

    PROCEDURE eliminar_consulta (
        p_consulta_id IN consultas.consulta_id%TYPE
    );

    PROCEDURE listar_consultas (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD TRATAMIENTOS
        ============================================================
    */

    PROCEDURE crear_tratamiento (
        p_nombre IN tratamientos.nombre%TYPE,
        p_descripcion IN tratamientos.descripcion%TYPE,
        p_costo_base IN tratamientos.costo_base%TYPE,
        p_estado IN tratamientos.estado%TYPE,
        p_tratamiento_id OUT tratamientos.tratamiento_id%TYPE
    );

    PROCEDURE actualizar_tratamiento (
        p_tratamiento_id IN tratamientos.tratamiento_id%TYPE,
        p_nombre IN tratamientos.nombre%TYPE,
        p_descripcion IN tratamientos.descripcion%TYPE,
        p_costo_base IN tratamientos.costo_base%TYPE,
        p_estado IN tratamientos.estado%TYPE
    );

    PROCEDURE eliminar_tratamiento (
        p_tratamiento_id IN tratamientos.tratamiento_id%TYPE
    );

    PROCEDURE listar_tratamientos (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD TRATAMIENTOS_CONSULTA
        ============================================================
    */

    PROCEDURE crear_tratamiento_consulta (
        p_consulta_id IN tratamientos_consulta.consulta_id%TYPE,
        p_tratamiento_id IN tratamientos_consulta.tratamiento_id%TYPE,
        p_cantidad IN tratamientos_consulta.cantidad%TYPE,
        p_precio_unitario IN tratamientos_consulta.precio_unitario%TYPE,
        p_tratamiento_consulta_id OUT tratamientos_consulta.tratamiento_consulta_id%TYPE
    );

    PROCEDURE actualizar_tratamiento_consulta (
        p_tratamiento_consulta_id IN tratamientos_consulta.tratamiento_consulta_id%TYPE,
        p_consulta_id IN tratamientos_consulta.consulta_id%TYPE,
        p_tratamiento_id IN tratamientos_consulta.tratamiento_id%TYPE,
        p_cantidad IN tratamientos_consulta.cantidad%TYPE,
        p_precio_unitario IN tratamientos_consulta.precio_unitario%TYPE
    );

    PROCEDURE eliminar_tratamiento_consulta (
        p_tratamiento_consulta_id IN tratamientos_consulta.tratamiento_consulta_id%TYPE
    );

    PROCEDURE listar_tratamientos_consulta (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_tratamientos_por_consulta (
        p_consulta_id IN tratamientos_consulta.consulta_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD HISTORIAL_MEDICO
        ============================================================
    */

    PROCEDURE crear_historial_medico (
        p_paciente_id IN historial_medico.paciente_id%TYPE,
        p_doctor_id IN historial_medico.doctor_id%TYPE,
        p_alergias IN historial_medico.alergias%TYPE,
        p_enfermedades IN historial_medico.enfermedades%TYPE,
        p_medicamentos IN historial_medico.medicamentos%TYPE,
        p_antecedentes_quirurgicos IN historial_medico.antecedentes_quirurgicos%TYPE,
        p_observaciones IN historial_medico.observaciones%TYPE,
        p_fecha_registro IN historial_medico.fecha_registro%TYPE,
        p_historial_id OUT historial_medico.historial_id%TYPE
    );

    PROCEDURE actualizar_historial_medico (
        p_historial_id IN historial_medico.historial_id%TYPE,
        p_paciente_id IN historial_medico.paciente_id%TYPE,
        p_doctor_id IN historial_medico.doctor_id%TYPE,
        p_alergias IN historial_medico.alergias%TYPE,
        p_enfermedades IN historial_medico.enfermedades%TYPE,
        p_medicamentos IN historial_medico.medicamentos%TYPE,
        p_antecedentes_quirurgicos IN historial_medico.antecedentes_quirurgicos%TYPE,
        p_observaciones IN historial_medico.observaciones%TYPE,
        p_fecha_registro IN historial_medico.fecha_registro%TYPE
    );

    PROCEDURE eliminar_historial_medico (
        p_historial_id IN historial_medico.historial_id%TYPE
    );

    PROCEDURE listar_historial_medico (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_historial_por_paciente (
        p_paciente_id IN historial_medico.paciente_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD CIRUGIAS
        ============================================================
    */

    PROCEDURE crear_cirugia (
        p_tratamiento_consulta_id IN cirugias.tratamiento_consulta_id%TYPE,
        p_doctor_id IN cirugias.doctor_id%TYPE,
        p_fecha_cirugia IN cirugias.fecha_cirugia%TYPE,
        p_descripcion_quirurgica IN cirugias.descripcion_quirurgica%TYPE,
        p_anestesia IN cirugias.anestesia%TYPE,
        p_observaciones IN cirugias.observaciones%TYPE,
        p_estado IN cirugias.estado%TYPE,
        p_cirugia_id OUT cirugias.cirugia_id%TYPE
    );

    PROCEDURE actualizar_cirugia (
        p_cirugia_id IN cirugias.cirugia_id%TYPE,
        p_tratamiento_consulta_id IN cirugias.tratamiento_consulta_id%TYPE,
        p_doctor_id IN cirugias.doctor_id%TYPE,
        p_fecha_cirugia IN cirugias.fecha_cirugia%TYPE,
        p_descripcion_quirurgica IN cirugias.descripcion_quirurgica%TYPE,
        p_anestesia IN cirugias.anestesia%TYPE,
        p_observaciones IN cirugias.observaciones%TYPE,
        p_estado IN cirugias.estado%TYPE
    );

    PROCEDURE eliminar_cirugia (
        p_cirugia_id IN cirugias.cirugia_id%TYPE
    );

    PROCEDURE listar_cirugias (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD HORARIOS_DOCTORES
        ============================================================
    */

    PROCEDURE crear_horario_doctor (
        p_doctor_id IN horarios_doctores.doctor_id%TYPE,
        p_dia_semana IN horarios_doctores.dia_semana%TYPE,
        p_hora_inicio IN horarios_doctores.hora_inicio%TYPE,
        p_hora_fin IN horarios_doctores.hora_fin%TYPE,
        p_estado IN horarios_doctores.estado%TYPE,
        p_horario_id OUT horarios_doctores.horario_id%TYPE
    );

    PROCEDURE actualizar_horario_doctor (
        p_horario_id IN horarios_doctores.horario_id%TYPE,
        p_doctor_id IN horarios_doctores.doctor_id%TYPE,
        p_dia_semana IN horarios_doctores.dia_semana%TYPE,
        p_hora_inicio IN horarios_doctores.hora_inicio%TYPE,
        p_hora_fin IN horarios_doctores.hora_fin%TYPE,
        p_estado IN horarios_doctores.estado%TYPE
    );

    PROCEDURE eliminar_horario_doctor (
        p_horario_id IN horarios_doctores.horario_id%TYPE
    );

    PROCEDURE listar_horarios_doctores (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_horarios_por_doctor (
        p_doctor_id IN horarios_doctores.doctor_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD DISPONIBILIDAD_DOCTORES
        ============================================================
    */

    PROCEDURE crear_disponibilidad_doctor (
        p_doctor_id IN disponibilidad_doctores.doctor_id%TYPE,
        p_fecha IN disponibilidad_doctores.fecha%TYPE,
        p_hora_inicio IN disponibilidad_doctores.hora_inicio%TYPE,
        p_hora_fin IN disponibilidad_doctores.hora_fin%TYPE,
        p_estado IN disponibilidad_doctores.estado%TYPE,
        p_disponibilidad_id OUT disponibilidad_doctores.disponibilidad_id%TYPE
    );

    PROCEDURE actualizar_disponibilidad_doctor (
        p_disponibilidad_id IN disponibilidad_doctores.disponibilidad_id%TYPE,
        p_doctor_id IN disponibilidad_doctores.doctor_id%TYPE,
        p_fecha IN disponibilidad_doctores.fecha%TYPE,
        p_hora_inicio IN disponibilidad_doctores.hora_inicio%TYPE,
        p_hora_fin IN disponibilidad_doctores.hora_fin%TYPE,
        p_estado IN disponibilidad_doctores.estado%TYPE
    );

    PROCEDURE eliminar_disponibilidad_doctor (
        p_disponibilidad_id IN disponibilidad_doctores.disponibilidad_id%TYPE
    );

    PROCEDURE listar_disponibilidad_doctores (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_disponibilidad_por_doctor (
        p_doctor_id IN disponibilidad_doctores.doctor_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

END pkg_smilecare_crud_clinico;
/

SHOW ERRORS PACKAGE pkg_smilecare_crud_clinico;


CREATE OR REPLACE PACKAGE BODY pkg_smilecare_crud_clinico AS

    /*
        ============================================================
        CRUD CONSULTAS
        ============================================================
    */

    PROCEDURE crear_consulta (
        p_cita_id IN consultas.cita_id%TYPE,
        p_diagnostico IN consultas.diagnostico%TYPE,
        p_observaciones IN consultas.observaciones%TYPE,
        p_fecha_atencion IN consultas.fecha_atencion%TYPE,
        p_consulta_id OUT consultas.consulta_id%TYPE
    ) AS
    BEGIN
        INSERT INTO consultas (
            cita_id,
            diagnostico,
            observaciones,
            fecha_atencion
        )
        VALUES (
            p_cita_id,
            p_diagnostico,
            p_observaciones,
            NVL(p_fecha_atencion, SYSTIMESTAMP)
        )
        RETURNING consulta_id INTO p_consulta_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -24001,
                'No se pudo crear la consulta porque la cita ya tiene una consulta registrada.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24999,
                'Error inesperado al crear consulta: ' || SQLERRM
            );
    END crear_consulta;


    PROCEDURE actualizar_consulta (
        p_consulta_id IN consultas.consulta_id%TYPE,
        p_cita_id IN consultas.cita_id%TYPE,
        p_diagnostico IN consultas.diagnostico%TYPE,
        p_observaciones IN consultas.observaciones%TYPE,
        p_fecha_atencion IN consultas.fecha_atencion%TYPE
    ) AS
    BEGIN
        UPDATE consultas
        SET
            cita_id = p_cita_id,
            diagnostico = p_diagnostico,
            observaciones = p_observaciones,
            fecha_atencion = p_fecha_atencion
        WHERE consulta_id = p_consulta_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24002,
                'No se encontró la consulta indicada para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24998,
                'Error inesperado al actualizar consulta: ' || SQLERRM
            );
    END actualizar_consulta;


    PROCEDURE eliminar_consulta (
        p_consulta_id IN consultas.consulta_id%TYPE
    ) AS
    BEGIN
        DELETE FROM consultas
        WHERE consulta_id = p_consulta_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24003,
                'No se encontró la consulta indicada para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24997,
                'Error inesperado al eliminar consulta: ' || SQLERRM
            );
    END eliminar_consulta;


    PROCEDURE listar_consultas (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                co.consulta_id,
                co.cita_id,
                c.paciente_id,
                p.nombre || ' ' || p.apellido AS paciente_nombre,
                c.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                co.diagnostico,
                co.observaciones,
                co.fecha_atencion
            FROM consultas co
            INNER JOIN citas c
                ON co.cita_id = c.cita_id
            INNER JOIN pacientes p
                ON c.paciente_id = p.paciente_id
            INNER JOIN doctores d
                ON c.doctor_id = d.doctor_id
            ORDER BY co.consulta_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24996,
                'Error inesperado al listar consultas: ' || SQLERRM
            );
    END listar_consultas;


    /*
        ============================================================
        CRUD TRATAMIENTOS
        ============================================================
    */

    PROCEDURE crear_tratamiento (
        p_nombre IN tratamientos.nombre%TYPE,
        p_descripcion IN tratamientos.descripcion%TYPE,
        p_costo_base IN tratamientos.costo_base%TYPE,
        p_estado IN tratamientos.estado%TYPE,
        p_tratamiento_id OUT tratamientos.tratamiento_id%TYPE
    ) AS
    BEGIN
        INSERT INTO tratamientos (
            nombre,
            descripcion,
            costo_base,
            estado
        )
        VALUES (
            p_nombre,
            p_descripcion,
            p_costo_base,
            p_estado
        )
        RETURNING tratamiento_id INTO p_tratamiento_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24995,
                'Error inesperado al crear tratamiento: ' || SQLERRM
            );
    END crear_tratamiento;


    PROCEDURE actualizar_tratamiento (
        p_tratamiento_id IN tratamientos.tratamiento_id%TYPE,
        p_nombre IN tratamientos.nombre%TYPE,
        p_descripcion IN tratamientos.descripcion%TYPE,
        p_costo_base IN tratamientos.costo_base%TYPE,
        p_estado IN tratamientos.estado%TYPE
    ) AS
    BEGIN
        UPDATE tratamientos
        SET
            nombre = p_nombre,
            descripcion = p_descripcion,
            costo_base = p_costo_base,
            estado = p_estado
        WHERE tratamiento_id = p_tratamiento_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24101,
                'No se encontró el tratamiento indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24994,
                'Error inesperado al actualizar tratamiento: ' || SQLERRM
            );
    END actualizar_tratamiento;


    PROCEDURE eliminar_tratamiento (
        p_tratamiento_id IN tratamientos.tratamiento_id%TYPE
    ) AS
    BEGIN
        DELETE FROM tratamientos
        WHERE tratamiento_id = p_tratamiento_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24102,
                'No se encontró el tratamiento indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24993,
                'Error inesperado al eliminar tratamiento: ' || SQLERRM
            );
    END eliminar_tratamiento;


    PROCEDURE listar_tratamientos (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                tratamiento_id,
                nombre,
                descripcion,
                costo_base,
                estado
            FROM tratamientos
            ORDER BY tratamiento_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24992,
                'Error inesperado al listar tratamientos: ' || SQLERRM
            );
    END listar_tratamientos;


    /*
        ============================================================
        CRUD TRATAMIENTOS_CONSULTA
        ============================================================
    */

    PROCEDURE crear_tratamiento_consulta (
        p_consulta_id IN tratamientos_consulta.consulta_id%TYPE,
        p_tratamiento_id IN tratamientos_consulta.tratamiento_id%TYPE,
        p_cantidad IN tratamientos_consulta.cantidad%TYPE,
        p_precio_unitario IN tratamientos_consulta.precio_unitario%TYPE,
        p_tratamiento_consulta_id OUT tratamientos_consulta.tratamiento_consulta_id%TYPE
    ) AS
        v_subtotal tratamientos_consulta.subtotal%TYPE;
    BEGIN
        v_subtotal := NVL(p_cantidad, 0) * NVL(p_precio_unitario, 0);

        INSERT INTO tratamientos_consulta (
            consulta_id,
            tratamiento_id,
            cantidad,
            precio_unitario,
            subtotal
        )
        VALUES (
            p_consulta_id,
            p_tratamiento_id,
            p_cantidad,
            p_precio_unitario,
            v_subtotal
        )
        RETURNING tratamiento_consulta_id INTO p_tratamiento_consulta_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24991,
                'Error inesperado al crear tratamiento de consulta: ' || SQLERRM
            );
    END crear_tratamiento_consulta;


    PROCEDURE actualizar_tratamiento_consulta (
        p_tratamiento_consulta_id IN tratamientos_consulta.tratamiento_consulta_id%TYPE,
        p_consulta_id IN tratamientos_consulta.consulta_id%TYPE,
        p_tratamiento_id IN tratamientos_consulta.tratamiento_id%TYPE,
        p_cantidad IN tratamientos_consulta.cantidad%TYPE,
        p_precio_unitario IN tratamientos_consulta.precio_unitario%TYPE
    ) AS
        v_subtotal tratamientos_consulta.subtotal%TYPE;
    BEGIN
        v_subtotal := NVL(p_cantidad, 0) * NVL(p_precio_unitario, 0);

        UPDATE tratamientos_consulta
        SET
            consulta_id = p_consulta_id,
            tratamiento_id = p_tratamiento_id,
            cantidad = p_cantidad,
            precio_unitario = p_precio_unitario,
            subtotal = v_subtotal
        WHERE tratamiento_consulta_id = p_tratamiento_consulta_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24201,
                'No se encontró el tratamiento de consulta indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24990,
                'Error inesperado al actualizar tratamiento de consulta: ' || SQLERRM
            );
    END actualizar_tratamiento_consulta;


    PROCEDURE eliminar_tratamiento_consulta (
        p_tratamiento_consulta_id IN tratamientos_consulta.tratamiento_consulta_id%TYPE
    ) AS
    BEGIN
        DELETE FROM tratamientos_consulta
        WHERE tratamiento_consulta_id = p_tratamiento_consulta_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24202,
                'No se encontró el tratamiento de consulta indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24989,
                'Error inesperado al eliminar tratamiento de consulta: ' || SQLERRM
            );
    END eliminar_tratamiento_consulta;


    PROCEDURE listar_tratamientos_consulta (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                tc.tratamiento_consulta_id,
                tc.consulta_id,
                tc.tratamiento_id,
                t.nombre AS tratamiento_nombre,
                tc.cantidad,
                tc.precio_unitario,
                tc.subtotal
            FROM tratamientos_consulta tc
            INNER JOIN tratamientos t
                ON tc.tratamiento_id = t.tratamiento_id
            ORDER BY tc.tratamiento_consulta_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24988,
                'Error inesperado al listar tratamientos de consulta: ' || SQLERRM
            );
    END listar_tratamientos_consulta;


    PROCEDURE listar_tratamientos_por_consulta (
        p_consulta_id IN tratamientos_consulta.consulta_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                tc.tratamiento_consulta_id,
                tc.consulta_id,
                tc.tratamiento_id,
                t.nombre AS tratamiento_nombre,
                tc.cantidad,
                tc.precio_unitario,
                tc.subtotal
            FROM tratamientos_consulta tc
            INNER JOIN tratamientos t
                ON tc.tratamiento_id = t.tratamiento_id
            WHERE tc.consulta_id = p_consulta_id
            ORDER BY tc.tratamiento_consulta_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24987,
                'Error inesperado al listar tratamientos por consulta: ' || SQLERRM
            );
    END listar_tratamientos_por_consulta;


    /*
        ============================================================
        CRUD HISTORIAL_MEDICO
        ============================================================
    */

    PROCEDURE crear_historial_medico (
        p_paciente_id IN historial_medico.paciente_id%TYPE,
        p_doctor_id IN historial_medico.doctor_id%TYPE,
        p_alergias IN historial_medico.alergias%TYPE,
        p_enfermedades IN historial_medico.enfermedades%TYPE,
        p_medicamentos IN historial_medico.medicamentos%TYPE,
        p_antecedentes_quirurgicos IN historial_medico.antecedentes_quirurgicos%TYPE,
        p_observaciones IN historial_medico.observaciones%TYPE,
        p_fecha_registro IN historial_medico.fecha_registro%TYPE,
        p_historial_id OUT historial_medico.historial_id%TYPE
    ) AS
    BEGIN
        INSERT INTO historial_medico (
            paciente_id,
            doctor_id,
            alergias,
            enfermedades,
            medicamentos,
            antecedentes_quirurgicos,
            observaciones,
            fecha_registro
        )
        VALUES (
            p_paciente_id,
            p_doctor_id,
            p_alergias,
            p_enfermedades,
            p_medicamentos,
            p_antecedentes_quirurgicos,
            p_observaciones,
            NVL(p_fecha_registro, SYSDATE)
        )
        RETURNING historial_id INTO p_historial_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24986,
                'Error inesperado al crear historial médico: ' || SQLERRM
            );
    END crear_historial_medico;


    PROCEDURE actualizar_historial_medico (
        p_historial_id IN historial_medico.historial_id%TYPE,
        p_paciente_id IN historial_medico.paciente_id%TYPE,
        p_doctor_id IN historial_medico.doctor_id%TYPE,
        p_alergias IN historial_medico.alergias%TYPE,
        p_enfermedades IN historial_medico.enfermedades%TYPE,
        p_medicamentos IN historial_medico.medicamentos%TYPE,
        p_antecedentes_quirurgicos IN historial_medico.antecedentes_quirurgicos%TYPE,
        p_observaciones IN historial_medico.observaciones%TYPE,
        p_fecha_registro IN historial_medico.fecha_registro%TYPE
    ) AS
    BEGIN
        UPDATE historial_medico
        SET
            paciente_id = p_paciente_id,
            doctor_id = p_doctor_id,
            alergias = p_alergias,
            enfermedades = p_enfermedades,
            medicamentos = p_medicamentos,
            antecedentes_quirurgicos = p_antecedentes_quirurgicos,
            observaciones = p_observaciones,
            fecha_registro = p_fecha_registro
        WHERE historial_id = p_historial_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24301,
                'No se encontró el historial médico indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24985,
                'Error inesperado al actualizar historial médico: ' || SQLERRM
            );
    END actualizar_historial_medico;


    PROCEDURE eliminar_historial_medico (
        p_historial_id IN historial_medico.historial_id%TYPE
    ) AS
    BEGIN
        DELETE FROM historial_medico
        WHERE historial_id = p_historial_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24302,
                'No se encontró el historial médico indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24984,
                'Error inesperado al eliminar historial médico: ' || SQLERRM
            );
    END eliminar_historial_medico;


    PROCEDURE listar_historial_medico (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                hm.historial_id,
                hm.paciente_id,
                p.nombre || ' ' || p.apellido AS paciente_nombre,
                hm.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                hm.alergias,
                hm.enfermedades,
                hm.medicamentos,
                hm.antecedentes_quirurgicos,
                hm.observaciones,
                hm.fecha_registro
            FROM historial_medico hm
            INNER JOIN pacientes p
                ON hm.paciente_id = p.paciente_id
            INNER JOIN doctores d
                ON hm.doctor_id = d.doctor_id
            ORDER BY hm.historial_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24983,
                'Error inesperado al listar historial médico: ' || SQLERRM
            );
    END listar_historial_medico;


    PROCEDURE listar_historial_por_paciente (
        p_paciente_id IN historial_medico.paciente_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                hm.historial_id,
                hm.paciente_id,
                p.nombre || ' ' || p.apellido AS paciente_nombre,
                hm.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                hm.alergias,
                hm.enfermedades,
                hm.medicamentos,
                hm.antecedentes_quirurgicos,
                hm.observaciones,
                hm.fecha_registro
            FROM historial_medico hm
            INNER JOIN pacientes p
                ON hm.paciente_id = p.paciente_id
            INNER JOIN doctores d
                ON hm.doctor_id = d.doctor_id
            WHERE hm.paciente_id = p_paciente_id
            ORDER BY hm.fecha_registro DESC;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24982,
                'Error inesperado al listar historial por paciente: ' || SQLERRM
            );
    END listar_historial_por_paciente;


    /*
        ============================================================
        CRUD CIRUGIAS
        ============================================================
    */

    PROCEDURE crear_cirugia (
        p_tratamiento_consulta_id IN cirugias.tratamiento_consulta_id%TYPE,
        p_doctor_id IN cirugias.doctor_id%TYPE,
        p_fecha_cirugia IN cirugias.fecha_cirugia%TYPE,
        p_descripcion_quirurgica IN cirugias.descripcion_quirurgica%TYPE,
        p_anestesia IN cirugias.anestesia%TYPE,
        p_observaciones IN cirugias.observaciones%TYPE,
        p_estado IN cirugias.estado%TYPE,
        p_cirugia_id OUT cirugias.cirugia_id%TYPE
    ) AS
    BEGIN
        INSERT INTO cirugias (
            tratamiento_consulta_id,
            doctor_id,
            fecha_cirugia,
            descripcion_quirurgica,
            anestesia,
            observaciones,
            estado
        )
        VALUES (
            p_tratamiento_consulta_id,
            p_doctor_id,
            p_fecha_cirugia,
            p_descripcion_quirurgica,
            p_anestesia,
            p_observaciones,
            p_estado
        )
        RETURNING cirugia_id INTO p_cirugia_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -24401,
                'No se pudo crear la cirugía porque el tratamiento de consulta ya tiene cirugía.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24981,
                'Error inesperado al crear cirugía: ' || SQLERRM
            );
    END crear_cirugia;


    PROCEDURE actualizar_cirugia (
        p_cirugia_id IN cirugias.cirugia_id%TYPE,
        p_tratamiento_consulta_id IN cirugias.tratamiento_consulta_id%TYPE,
        p_doctor_id IN cirugias.doctor_id%TYPE,
        p_fecha_cirugia IN cirugias.fecha_cirugia%TYPE,
        p_descripcion_quirurgica IN cirugias.descripcion_quirurgica%TYPE,
        p_anestesia IN cirugias.anestesia%TYPE,
        p_observaciones IN cirugias.observaciones%TYPE,
        p_estado IN cirugias.estado%TYPE
    ) AS
    BEGIN
        UPDATE cirugias
        SET
            tratamiento_consulta_id = p_tratamiento_consulta_id,
            doctor_id = p_doctor_id,
            fecha_cirugia = p_fecha_cirugia,
            descripcion_quirurgica = p_descripcion_quirurgica,
            anestesia = p_anestesia,
            observaciones = p_observaciones,
            estado = p_estado
        WHERE cirugia_id = p_cirugia_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24402,
                'No se encontró la cirugía indicada para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24980,
                'Error inesperado al actualizar cirugía: ' || SQLERRM
            );
    END actualizar_cirugia;


    PROCEDURE eliminar_cirugia (
        p_cirugia_id IN cirugias.cirugia_id%TYPE
    ) AS
    BEGIN
        DELETE FROM cirugias
        WHERE cirugia_id = p_cirugia_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24403,
                'No se encontró la cirugía indicada para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24979,
                'Error inesperado al eliminar cirugía: ' || SQLERRM
            );
    END eliminar_cirugia;


    PROCEDURE listar_cirugias (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                ci.cirugia_id,
                ci.tratamiento_consulta_id,
                tc.consulta_id,
                t.nombre AS tratamiento_nombre,
                ci.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                ci.fecha_cirugia,
                ci.descripcion_quirurgica,
                ci.anestesia,
                ci.observaciones,
                ci.estado
            FROM cirugias ci
            INNER JOIN tratamientos_consulta tc
                ON ci.tratamiento_consulta_id = tc.tratamiento_consulta_id
            INNER JOIN tratamientos t
                ON tc.tratamiento_id = t.tratamiento_id
            INNER JOIN doctores d
                ON ci.doctor_id = d.doctor_id
            ORDER BY ci.cirugia_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24978,
                'Error inesperado al listar cirugías: ' || SQLERRM
            );
    END listar_cirugias;


    /*
        ============================================================
        CRUD HORARIOS_DOCTORES
        ============================================================
    */

    PROCEDURE crear_horario_doctor (
        p_doctor_id IN horarios_doctores.doctor_id%TYPE,
        p_dia_semana IN horarios_doctores.dia_semana%TYPE,
        p_hora_inicio IN horarios_doctores.hora_inicio%TYPE,
        p_hora_fin IN horarios_doctores.hora_fin%TYPE,
        p_estado IN horarios_doctores.estado%TYPE,
        p_horario_id OUT horarios_doctores.horario_id%TYPE
    ) AS
    BEGIN
        INSERT INTO horarios_doctores (
            doctor_id,
            dia_semana,
            hora_inicio,
            hora_fin,
            estado
        )
        VALUES (
            p_doctor_id,
            p_dia_semana,
            p_hora_inicio,
            p_hora_fin,
            p_estado
        )
        RETURNING horario_id INTO p_horario_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24977,
                'Error inesperado al crear horario de doctor: ' || SQLERRM
            );
    END crear_horario_doctor;


    PROCEDURE actualizar_horario_doctor (
        p_horario_id IN horarios_doctores.horario_id%TYPE,
        p_doctor_id IN horarios_doctores.doctor_id%TYPE,
        p_dia_semana IN horarios_doctores.dia_semana%TYPE,
        p_hora_inicio IN horarios_doctores.hora_inicio%TYPE,
        p_hora_fin IN horarios_doctores.hora_fin%TYPE,
        p_estado IN horarios_doctores.estado%TYPE
    ) AS
    BEGIN
        UPDATE horarios_doctores
        SET
            doctor_id = p_doctor_id,
            dia_semana = p_dia_semana,
            hora_inicio = p_hora_inicio,
            hora_fin = p_hora_fin,
            estado = p_estado
        WHERE horario_id = p_horario_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24501,
                'No se encontró el horario indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24976,
                'Error inesperado al actualizar horario de doctor: ' || SQLERRM
            );
    END actualizar_horario_doctor;


    PROCEDURE eliminar_horario_doctor (
        p_horario_id IN horarios_doctores.horario_id%TYPE
    ) AS
    BEGIN
        DELETE FROM horarios_doctores
        WHERE horario_id = p_horario_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24502,
                'No se encontró el horario indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24975,
                'Error inesperado al eliminar horario de doctor: ' || SQLERRM
            );
    END eliminar_horario_doctor;


    PROCEDURE listar_horarios_doctores (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                h.horario_id,
                h.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                h.dia_semana,
                h.hora_inicio,
                h.hora_fin,
                h.estado
            FROM horarios_doctores h
            INNER JOIN doctores d
                ON h.doctor_id = d.doctor_id
            ORDER BY h.doctor_id, h.dia_semana, h.hora_inicio;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24974,
                'Error inesperado al listar horarios de doctores: ' || SQLERRM
            );
    END listar_horarios_doctores;


    PROCEDURE listar_horarios_por_doctor (
        p_doctor_id IN horarios_doctores.doctor_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                h.horario_id,
                h.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                h.dia_semana,
                h.hora_inicio,
                h.hora_fin,
                h.estado
            FROM horarios_doctores h
            INNER JOIN doctores d
                ON h.doctor_id = d.doctor_id
            WHERE h.doctor_id = p_doctor_id
            ORDER BY h.dia_semana, h.hora_inicio;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24973,
                'Error inesperado al listar horarios por doctor: ' || SQLERRM
            );
    END listar_horarios_por_doctor;


    /*
        ============================================================
        CRUD DISPONIBILIDAD_DOCTORES
        ============================================================
    */

    PROCEDURE crear_disponibilidad_doctor (
        p_doctor_id IN disponibilidad_doctores.doctor_id%TYPE,
        p_fecha IN disponibilidad_doctores.fecha%TYPE,
        p_hora_inicio IN disponibilidad_doctores.hora_inicio%TYPE,
        p_hora_fin IN disponibilidad_doctores.hora_fin%TYPE,
        p_estado IN disponibilidad_doctores.estado%TYPE,
        p_disponibilidad_id OUT disponibilidad_doctores.disponibilidad_id%TYPE
    ) AS
    BEGIN
        INSERT INTO disponibilidad_doctores (
            doctor_id,
            fecha,
            hora_inicio,
            hora_fin,
            estado
        )
        VALUES (
            p_doctor_id,
            p_fecha,
            p_hora_inicio,
            p_hora_fin,
            p_estado
        )
        RETURNING disponibilidad_id INTO p_disponibilidad_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24972,
                'Error inesperado al crear disponibilidad de doctor: ' || SQLERRM
            );
    END crear_disponibilidad_doctor;


    PROCEDURE actualizar_disponibilidad_doctor (
        p_disponibilidad_id IN disponibilidad_doctores.disponibilidad_id%TYPE,
        p_doctor_id IN disponibilidad_doctores.doctor_id%TYPE,
        p_fecha IN disponibilidad_doctores.fecha%TYPE,
        p_hora_inicio IN disponibilidad_doctores.hora_inicio%TYPE,
        p_hora_fin IN disponibilidad_doctores.hora_fin%TYPE,
        p_estado IN disponibilidad_doctores.estado%TYPE
    ) AS
    BEGIN
        UPDATE disponibilidad_doctores
        SET
            doctor_id = p_doctor_id,
            fecha = p_fecha,
            hora_inicio = p_hora_inicio,
            hora_fin = p_hora_fin,
            estado = p_estado
        WHERE disponibilidad_id = p_disponibilidad_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24601,
                'No se encontró la disponibilidad indicada para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24971,
                'Error inesperado al actualizar disponibilidad de doctor: ' || SQLERRM
            );
    END actualizar_disponibilidad_doctor;


    PROCEDURE eliminar_disponibilidad_doctor (
        p_disponibilidad_id IN disponibilidad_doctores.disponibilidad_id%TYPE
    ) AS
    BEGIN
        DELETE FROM disponibilidad_doctores
        WHERE disponibilidad_id = p_disponibilidad_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -24602,
                'No se encontró la disponibilidad indicada para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24970,
                'Error inesperado al eliminar disponibilidad de doctor: ' || SQLERRM
            );
    END eliminar_disponibilidad_doctor;


    PROCEDURE listar_disponibilidad_doctores (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                dis.disponibilidad_id,
                dis.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                dis.fecha,
                dis.hora_inicio,
                dis.hora_fin,
                dis.estado
            FROM disponibilidad_doctores dis
            INNER JOIN doctores d
                ON dis.doctor_id = d.doctor_id
            ORDER BY dis.fecha, dis.hora_inicio;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24969,
                'Error inesperado al listar disponibilidad de doctores: ' || SQLERRM
            );
    END listar_disponibilidad_doctores;


    PROCEDURE listar_disponibilidad_por_doctor (
        p_doctor_id IN disponibilidad_doctores.doctor_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                dis.disponibilidad_id,
                dis.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                dis.fecha,
                dis.hora_inicio,
                dis.hora_fin,
                dis.estado
            FROM disponibilidad_doctores dis
            INNER JOIN doctores d
                ON dis.doctor_id = d.doctor_id
            WHERE dis.doctor_id = p_doctor_id
            ORDER BY dis.fecha, dis.hora_inicio;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -24968,
                'Error inesperado al listar disponibilidad por doctor: ' || SQLERRM
            );
    END listar_disponibilidad_por_doctor;

END pkg_smilecare_crud_clinico;
/

SHOW ERRORS PACKAGE BODY pkg_smilecare_crud_clinico;


PROMPT ============================================================
PROMPT VERIFICANDO ESTADO DEL PAQUETE
PROMPT ============================================================

SELECT
    object_name,
    object_type,
    status
FROM user_objects
WHERE object_name = 'PKG_SMILECARE_CRUD_CLINICO'
ORDER BY object_type;