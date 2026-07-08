SET SERVEROUTPUT ON;

PROMPT ============================================================
PROMPT PAQUETE CRUD CORE - SMILECARE
PROMPT ============================================================

/*
    Archivo: 02_pkg_crud_core.sql
    Proyecto: SmileCare
    Curso: SC-504 Lenguajes de Base de Datos

    Objetivo:
    Crear un paquete Oracle con procedimientos CRUD para tablas principales
    del sistema clínico.

    Tablas incluidas en este paquete:
    - PACIENTES
    - ESPECIALIDADES
    - DOCTORES
    - CITAS

    Este paquete también incluye procedimientos con SYS_REFCURSOR,
    lo cual ayuda a cumplir el requisito del proyecto de usar cursores.
*/

CREATE OR REPLACE PACKAGE pkg_smilecare_crud_core AS

    /*
        ============================================================
        CRUD PACIENTES
        ============================================================
    */

    PROCEDURE crear_paciente (
        p_usuario_id IN pacientes.usuario_id%TYPE,
        p_nombre IN pacientes.nombre%TYPE,
        p_apellido IN pacientes.apellido%TYPE,
        p_telefono IN pacientes.telefono%TYPE,
        p_correo IN pacientes.correo%TYPE,
        p_direccion IN pacientes.direccion%TYPE,
        p_fecha_nacimiento IN pacientes.fecha_nacimiento%TYPE,
        p_paciente_id OUT pacientes.paciente_id%TYPE
    );

    PROCEDURE actualizar_paciente (
        p_paciente_id IN pacientes.paciente_id%TYPE,
        p_usuario_id IN pacientes.usuario_id%TYPE,
        p_nombre IN pacientes.nombre%TYPE,
        p_apellido IN pacientes.apellido%TYPE,
        p_telefono IN pacientes.telefono%TYPE,
        p_correo IN pacientes.correo%TYPE,
        p_direccion IN pacientes.direccion%TYPE,
        p_fecha_nacimiento IN pacientes.fecha_nacimiento%TYPE
    );

    PROCEDURE eliminar_paciente (
        p_paciente_id IN pacientes.paciente_id%TYPE
    );

    PROCEDURE listar_pacientes (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD ESPECIALIDADES
        ============================================================
    */

    PROCEDURE crear_especialidad (
        p_nombre IN especialidades.nombre%TYPE,
        p_descripcion IN especialidades.descripcion%TYPE,
        p_especialidad_id OUT especialidades.especialidad_id%TYPE
    );

    PROCEDURE actualizar_especialidad (
        p_especialidad_id IN especialidades.especialidad_id%TYPE,
        p_nombre IN especialidades.nombre%TYPE,
        p_descripcion IN especialidades.descripcion%TYPE
    );

    PROCEDURE eliminar_especialidad (
        p_especialidad_id IN especialidades.especialidad_id%TYPE
    );

    PROCEDURE listar_especialidades (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD DOCTORES
        ============================================================
    */

    PROCEDURE crear_doctor (
        p_usuario_id IN doctores.usuario_id%TYPE,
        p_especialidad_id IN doctores.especialidad_id%TYPE,
        p_nombre IN doctores.nombre%TYPE,
        p_apellido IN doctores.apellido%TYPE,
        p_telefono IN doctores.telefono%TYPE,
        p_correo IN doctores.correo%TYPE,
        p_doctor_id OUT doctores.doctor_id%TYPE
    );

    PROCEDURE actualizar_doctor (
        p_doctor_id IN doctores.doctor_id%TYPE,
        p_usuario_id IN doctores.usuario_id%TYPE,
        p_especialidad_id IN doctores.especialidad_id%TYPE,
        p_nombre IN doctores.nombre%TYPE,
        p_apellido IN doctores.apellido%TYPE,
        p_telefono IN doctores.telefono%TYPE,
        p_correo IN doctores.correo%TYPE
    );

    PROCEDURE eliminar_doctor (
        p_doctor_id IN doctores.doctor_id%TYPE
    );

    PROCEDURE listar_doctores (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD CITAS
        ============================================================
    */

    PROCEDURE crear_cita (
        p_paciente_id IN citas.paciente_id%TYPE,
        p_doctor_id IN citas.doctor_id%TYPE,
        p_fecha_hora_inicio IN citas.fecha_hora_inicio%TYPE,
        p_duracion_minutos IN citas.duracion_minutos%TYPE,
        p_estado IN citas.estado%TYPE,
        p_motivo IN citas.motivo%TYPE,
        p_cita_id OUT citas.cita_id%TYPE
    );

    PROCEDURE actualizar_cita (
        p_cita_id IN citas.cita_id%TYPE,
        p_paciente_id IN citas.paciente_id%TYPE,
        p_doctor_id IN citas.doctor_id%TYPE,
        p_fecha_hora_inicio IN citas.fecha_hora_inicio%TYPE,
        p_duracion_minutos IN citas.duracion_minutos%TYPE,
        p_estado IN citas.estado%TYPE,
        p_motivo IN citas.motivo%TYPE
    );

    PROCEDURE eliminar_cita (
        p_cita_id IN citas.cita_id%TYPE
    );

    PROCEDURE listar_citas (
        p_resultado OUT SYS_REFCURSOR
    );

END pkg_smilecare_crud_core;
/

SHOW ERRORS PACKAGE pkg_smilecare_crud_core;


CREATE OR REPLACE PACKAGE BODY pkg_smilecare_crud_core AS

    /*
        ============================================================
        CRUD PACIENTES
        ============================================================
    */

    PROCEDURE crear_paciente (
        p_usuario_id IN pacientes.usuario_id%TYPE,
        p_nombre IN pacientes.nombre%TYPE,
        p_apellido IN pacientes.apellido%TYPE,
        p_telefono IN pacientes.telefono%TYPE,
        p_correo IN pacientes.correo%TYPE,
        p_direccion IN pacientes.direccion%TYPE,
        p_fecha_nacimiento IN pacientes.fecha_nacimiento%TYPE,
        p_paciente_id OUT pacientes.paciente_id%TYPE
    ) AS
    BEGIN
        INSERT INTO pacientes (
            usuario_id,
            nombre,
            apellido,
            telefono,
            correo,
            direccion,
            fecha_nacimiento
        )
        VALUES (
            p_usuario_id,
            p_nombre,
            p_apellido,
            p_telefono,
            p_correo,
            p_direccion,
            p_fecha_nacimiento
        )
        RETURNING paciente_id INTO p_paciente_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -20001,
                'No se pudo crear el paciente porque existe un valor único repetido.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20999,
                'Error inesperado al crear paciente: ' || SQLERRM
            );
    END crear_paciente;


    PROCEDURE actualizar_paciente (
        p_paciente_id IN pacientes.paciente_id%TYPE,
        p_usuario_id IN pacientes.usuario_id%TYPE,
        p_nombre IN pacientes.nombre%TYPE,
        p_apellido IN pacientes.apellido%TYPE,
        p_telefono IN pacientes.telefono%TYPE,
        p_correo IN pacientes.correo%TYPE,
        p_direccion IN pacientes.direccion%TYPE,
        p_fecha_nacimiento IN pacientes.fecha_nacimiento%TYPE
    ) AS
    BEGIN
        UPDATE pacientes
        SET
            usuario_id = p_usuario_id,
            nombre = p_nombre,
            apellido = p_apellido,
            telefono = p_telefono,
            correo = p_correo,
            direccion = p_direccion,
            fecha_nacimiento = p_fecha_nacimiento
        WHERE paciente_id = p_paciente_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20002,
                'No se encontró el paciente indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20998,
                'Error inesperado al actualizar paciente: ' || SQLERRM
            );
    END actualizar_paciente;


    PROCEDURE eliminar_paciente (
        p_paciente_id IN pacientes.paciente_id%TYPE
    ) AS
    BEGIN
        DELETE FROM pacientes
        WHERE paciente_id = p_paciente_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20003,
                'No se encontró el paciente indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20997,
                'Error inesperado al eliminar paciente: ' || SQLERRM
            );
    END eliminar_paciente;


    PROCEDURE listar_pacientes (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                paciente_id,
                usuario_id,
                nombre,
                apellido,
                telefono,
                correo,
                direccion,
                fecha_nacimiento
            FROM pacientes
            ORDER BY paciente_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20996,
                'Error inesperado al listar pacientes: ' || SQLERRM
            );
    END listar_pacientes;


    /*
        ============================================================
        CRUD ESPECIALIDADES
        ============================================================
    */

    PROCEDURE crear_especialidad (
        p_nombre IN especialidades.nombre%TYPE,
        p_descripcion IN especialidades.descripcion%TYPE,
        p_especialidad_id OUT especialidades.especialidad_id%TYPE
    ) AS
    BEGIN
        INSERT INTO especialidades (
            nombre,
            descripcion
        )
        VALUES (
            p_nombre,
            p_descripcion
        )
        RETURNING especialidad_id INTO p_especialidad_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -20101,
                'No se pudo crear la especialidad porque existe un valor único repetido.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20995,
                'Error inesperado al crear especialidad: ' || SQLERRM
            );
    END crear_especialidad;


    PROCEDURE actualizar_especialidad (
        p_especialidad_id IN especialidades.especialidad_id%TYPE,
        p_nombre IN especialidades.nombre%TYPE,
        p_descripcion IN especialidades.descripcion%TYPE
    ) AS
    BEGIN
        UPDATE especialidades
        SET
            nombre = p_nombre,
            descripcion = p_descripcion
        WHERE especialidad_id = p_especialidad_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20102,
                'No se encontró la especialidad indicada para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20994,
                'Error inesperado al actualizar especialidad: ' || SQLERRM
            );
    END actualizar_especialidad;


    PROCEDURE eliminar_especialidad (
        p_especialidad_id IN especialidades.especialidad_id%TYPE
    ) AS
    BEGIN
        DELETE FROM especialidades
        WHERE especialidad_id = p_especialidad_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20103,
                'No se encontró la especialidad indicada para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20993,
                'Error inesperado al eliminar especialidad: ' || SQLERRM
            );
    END eliminar_especialidad;


    PROCEDURE listar_especialidades (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                especialidad_id,
                nombre,
                descripcion
            FROM especialidades
            ORDER BY especialidad_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20992,
                'Error inesperado al listar especialidades: ' || SQLERRM
            );
    END listar_especialidades;


    /*
        ============================================================
        CRUD DOCTORES
        ============================================================
    */

    PROCEDURE crear_doctor (
        p_usuario_id IN doctores.usuario_id%TYPE,
        p_especialidad_id IN doctores.especialidad_id%TYPE,
        p_nombre IN doctores.nombre%TYPE,
        p_apellido IN doctores.apellido%TYPE,
        p_telefono IN doctores.telefono%TYPE,
        p_correo IN doctores.correo%TYPE,
        p_doctor_id OUT doctores.doctor_id%TYPE
    ) AS
    BEGIN
        INSERT INTO doctores (
            usuario_id,
            especialidad_id,
            nombre,
            apellido,
            telefono,
            correo
        )
        VALUES (
            p_usuario_id,
            p_especialidad_id,
            p_nombre,
            p_apellido,
            p_telefono,
            p_correo
        )
        RETURNING doctor_id INTO p_doctor_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -20201,
                'No se pudo crear el doctor porque existe un valor único repetido.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20991,
                'Error inesperado al crear doctor: ' || SQLERRM
            );
    END crear_doctor;


    PROCEDURE actualizar_doctor (
        p_doctor_id IN doctores.doctor_id%TYPE,
        p_usuario_id IN doctores.usuario_id%TYPE,
        p_especialidad_id IN doctores.especialidad_id%TYPE,
        p_nombre IN doctores.nombre%TYPE,
        p_apellido IN doctores.apellido%TYPE,
        p_telefono IN doctores.telefono%TYPE,
        p_correo IN doctores.correo%TYPE
    ) AS
    BEGIN
        UPDATE doctores
        SET
            usuario_id = p_usuario_id,
            especialidad_id = p_especialidad_id,
            nombre = p_nombre,
            apellido = p_apellido,
            telefono = p_telefono,
            correo = p_correo
        WHERE doctor_id = p_doctor_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20202,
                'No se encontró el doctor indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20990,
                'Error inesperado al actualizar doctor: ' || SQLERRM
            );
    END actualizar_doctor;


    PROCEDURE eliminar_doctor (
        p_doctor_id IN doctores.doctor_id%TYPE
    ) AS
    BEGIN
        DELETE FROM doctores
        WHERE doctor_id = p_doctor_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20203,
                'No se encontró el doctor indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20989,
                'Error inesperado al eliminar doctor: ' || SQLERRM
            );
    END eliminar_doctor;


    PROCEDURE listar_doctores (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
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
            ORDER BY d.doctor_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20988,
                'Error inesperado al listar doctores: ' || SQLERRM
            );
    END listar_doctores;


    /*
        ============================================================
        CRUD CITAS
        ============================================================
    */

    PROCEDURE crear_cita (
        p_paciente_id IN citas.paciente_id%TYPE,
        p_doctor_id IN citas.doctor_id%TYPE,
        p_fecha_hora_inicio IN citas.fecha_hora_inicio%TYPE,
        p_duracion_minutos IN citas.duracion_minutos%TYPE,
        p_estado IN citas.estado%TYPE,
        p_motivo IN citas.motivo%TYPE,
        p_cita_id OUT citas.cita_id%TYPE
    ) AS
    BEGIN
        INSERT INTO citas (
            paciente_id,
            doctor_id,
            fecha_hora_inicio,
            duracion_minutos,
            estado,
            motivo
        )
        VALUES (
            p_paciente_id,
            p_doctor_id,
            p_fecha_hora_inicio,
            p_duracion_minutos,
            p_estado,
            p_motivo
        )
        RETURNING cita_id INTO p_cita_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20987,
                'Error inesperado al crear cita: ' || SQLERRM
            );
    END crear_cita;


    PROCEDURE actualizar_cita (
        p_cita_id IN citas.cita_id%TYPE,
        p_paciente_id IN citas.paciente_id%TYPE,
        p_doctor_id IN citas.doctor_id%TYPE,
        p_fecha_hora_inicio IN citas.fecha_hora_inicio%TYPE,
        p_duracion_minutos IN citas.duracion_minutos%TYPE,
        p_estado IN citas.estado%TYPE,
        p_motivo IN citas.motivo%TYPE
    ) AS
    BEGIN
        UPDATE citas
        SET
            paciente_id = p_paciente_id,
            doctor_id = p_doctor_id,
            fecha_hora_inicio = p_fecha_hora_inicio,
            duracion_minutos = p_duracion_minutos,
            estado = p_estado,
            motivo = p_motivo
        WHERE cita_id = p_cita_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20302,
                'No se encontró la cita indicada para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20986,
                'Error inesperado al actualizar cita: ' || SQLERRM
            );
    END actualizar_cita;


    PROCEDURE eliminar_cita (
        p_cita_id IN citas.cita_id%TYPE
    ) AS
    BEGIN
        DELETE FROM citas
        WHERE cita_id = p_cita_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20303,
                'No se encontró la cita indicada para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20985,
                'Error inesperado al eliminar cita: ' || SQLERRM
            );
    END eliminar_cita;


    PROCEDURE listar_citas (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                c.cita_id,
                c.paciente_id,
                p.nombre || ' ' || p.apellido AS paciente_nombre,
                c.doctor_id,
                d.nombre || ' ' || d.apellido AS doctor_nombre,
                c.fecha_hora_inicio,
                c.duracion_minutos,
                c.estado,
                c.motivo
            FROM citas c
            INNER JOIN pacientes p
                ON c.paciente_id = p.paciente_id
            INNER JOIN doctores d
                ON c.doctor_id = d.doctor_id
            ORDER BY c.fecha_hora_inicio;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -20984,
                'Error inesperado al listar citas: ' || SQLERRM
            );
    END listar_citas;

END pkg_smilecare_crud_core;
/

SHOW ERRORS PACKAGE BODY pkg_smilecare_crud_core;


PROMPT ============================================================
PROMPT VERIFICANDO ESTADO DEL PAQUETE
PROMPT ============================================================

SELECT
    object_name,
    object_type,
    status
FROM user_objects
WHERE object_name = 'PKG_SMILECARE_CRUD_CORE'
ORDER BY object_type;