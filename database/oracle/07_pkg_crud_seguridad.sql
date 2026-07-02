SET SERVEROUTPUT ON;

PROMPT ============================================================
PROMPT PAQUETE CRUD SEGURIDAD - SMILECARE
PROMPT ============================================================

/*
    Archivo: 07_pkg_crud_seguridad.sql
    Proyecto: SmileCare
    Curso: SC-504 Lenguajes de Base de Datos

    Objetivo:
    Crear un paquete Oracle con procedimientos CRUD para las tablas
    relacionadas con seguridad y control de acceso.

    Tablas incluidas:
    - ROLES
    - PERMISOS
    - ROL_PERMISOS
    - USUARIOS
*/

CREATE OR REPLACE PACKAGE pkg_smilecare_crud_seguridad AS

    /*
        ============================================================
        CRUD ROLES
        ============================================================
    */

    PROCEDURE crear_rol (
        p_nombre_rol IN roles.nombre_rol%TYPE,
        p_descripcion IN roles.descripcion%TYPE,
        p_estado IN roles.estado%TYPE,
        p_rol_id OUT roles.rol_id%TYPE
    );

    PROCEDURE actualizar_rol (
        p_rol_id IN roles.rol_id%TYPE,
        p_nombre_rol IN roles.nombre_rol%TYPE,
        p_descripcion IN roles.descripcion%TYPE,
        p_estado IN roles.estado%TYPE
    );

    PROCEDURE eliminar_rol (
        p_rol_id IN roles.rol_id%TYPE
    );

    PROCEDURE listar_roles (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD PERMISOS
        ============================================================
    */

    PROCEDURE crear_permiso (
        p_codigo_permiso IN permisos.codigo_permiso%TYPE,
        p_descripcion IN permisos.descripcion%TYPE,
        p_modulo IN permisos.modulo%TYPE,
        p_permiso_id OUT permisos.permiso_id%TYPE
    );

    PROCEDURE actualizar_permiso (
        p_permiso_id IN permisos.permiso_id%TYPE,
        p_codigo_permiso IN permisos.codigo_permiso%TYPE,
        p_descripcion IN permisos.descripcion%TYPE,
        p_modulo IN permisos.modulo%TYPE
    );

    PROCEDURE eliminar_permiso (
        p_permiso_id IN permisos.permiso_id%TYPE
    );

    PROCEDURE listar_permisos (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD USUARIOS
        ============================================================
    */

    PROCEDURE crear_usuario (
        p_rol_id IN usuarios.rol_id%TYPE,
        p_nombre_usuario IN usuarios.nombre_usuario%TYPE,
        p_password_hash IN usuarios.password_hash%TYPE,
        p_estado IN usuarios.estado%TYPE,
        p_usuario_id OUT usuarios.usuario_id%TYPE
    );

    PROCEDURE actualizar_usuario (
        p_usuario_id IN usuarios.usuario_id%TYPE,
        p_rol_id IN usuarios.rol_id%TYPE,
        p_nombre_usuario IN usuarios.nombre_usuario%TYPE,
        p_password_hash IN usuarios.password_hash%TYPE,
        p_estado IN usuarios.estado%TYPE
    );

    PROCEDURE eliminar_usuario (
        p_usuario_id IN usuarios.usuario_id%TYPE
    );

    PROCEDURE listar_usuarios (
        p_resultado OUT SYS_REFCURSOR
    );

    /*
        ============================================================
        CRUD ROL_PERMISOS
        ============================================================
    */

    PROCEDURE asignar_permiso_rol (
        p_rol_id IN rol_permisos.rol_id%TYPE,
        p_permiso_id IN rol_permisos.permiso_id%TYPE
    );

    PROCEDURE actualizar_permiso_rol (
        p_rol_id_actual IN rol_permisos.rol_id%TYPE,
        p_permiso_id_actual IN rol_permisos.permiso_id%TYPE,
        p_rol_id_nuevo IN rol_permisos.rol_id%TYPE,
        p_permiso_id_nuevo IN rol_permisos.permiso_id%TYPE
    );

    PROCEDURE eliminar_permiso_rol (
        p_rol_id IN rol_permisos.rol_id%TYPE,
        p_permiso_id IN rol_permisos.permiso_id%TYPE
    );

    PROCEDURE listar_rol_permisos (
        p_resultado OUT SYS_REFCURSOR
    );

    PROCEDURE listar_permisos_por_rol (
        p_rol_id IN rol_permisos.rol_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    );

END pkg_smilecare_crud_seguridad;
/

SHOW ERRORS PACKAGE pkg_smilecare_crud_seguridad;


CREATE OR REPLACE PACKAGE BODY pkg_smilecare_crud_seguridad AS

    /*
        ============================================================
        CRUD ROLES
        ============================================================
    */

    PROCEDURE crear_rol (
        p_nombre_rol IN roles.nombre_rol%TYPE,
        p_descripcion IN roles.descripcion%TYPE,
        p_estado IN roles.estado%TYPE,
        p_rol_id OUT roles.rol_id%TYPE
    ) AS
    BEGIN
        INSERT INTO roles (
            nombre_rol,
            descripcion,
            estado
        )
        VALUES (
            p_nombre_rol,
            p_descripcion,
            p_estado
        )
        RETURNING rol_id INTO p_rol_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -25001,
                'No se pudo crear el rol porque el nombre ya existe.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25999,
                'Error inesperado al crear rol: ' || SQLERRM
            );
    END crear_rol;


    PROCEDURE actualizar_rol (
        p_rol_id IN roles.rol_id%TYPE,
        p_nombre_rol IN roles.nombre_rol%TYPE,
        p_descripcion IN roles.descripcion%TYPE,
        p_estado IN roles.estado%TYPE
    ) AS
    BEGIN
        UPDATE roles
        SET
            nombre_rol = p_nombre_rol,
            descripcion = p_descripcion,
            estado = p_estado
        WHERE rol_id = p_rol_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -25002,
                'No se encontró el rol indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25998,
                'Error inesperado al actualizar rol: ' || SQLERRM
            );
    END actualizar_rol;


    PROCEDURE eliminar_rol (
        p_rol_id IN roles.rol_id%TYPE
    ) AS
    BEGIN
        DELETE FROM roles
        WHERE rol_id = p_rol_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -25003,
                'No se encontró el rol indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25997,
                'Error inesperado al eliminar rol: ' || SQLERRM
            );
    END eliminar_rol;


    PROCEDURE listar_roles (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                rol_id,
                nombre_rol,
                descripcion,
                estado
            FROM roles
            ORDER BY rol_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25996,
                'Error inesperado al listar roles: ' || SQLERRM
            );
    END listar_roles;


    /*
        ============================================================
        CRUD PERMISOS
        ============================================================
    */

    PROCEDURE crear_permiso (
        p_codigo_permiso IN permisos.codigo_permiso%TYPE,
        p_descripcion IN permisos.descripcion%TYPE,
        p_modulo IN permisos.modulo%TYPE,
        p_permiso_id OUT permisos.permiso_id%TYPE
    ) AS
    BEGIN
        INSERT INTO permisos (
            codigo_permiso,
            descripcion,
            modulo
        )
        VALUES (
            p_codigo_permiso,
            p_descripcion,
            p_modulo
        )
        RETURNING permiso_id INTO p_permiso_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -25101,
                'No se pudo crear el permiso porque el código ya existe.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25995,
                'Error inesperado al crear permiso: ' || SQLERRM
            );
    END crear_permiso;


    PROCEDURE actualizar_permiso (
        p_permiso_id IN permisos.permiso_id%TYPE,
        p_codigo_permiso IN permisos.codigo_permiso%TYPE,
        p_descripcion IN permisos.descripcion%TYPE,
        p_modulo IN permisos.modulo%TYPE
    ) AS
    BEGIN
        UPDATE permisos
        SET
            codigo_permiso = p_codigo_permiso,
            descripcion = p_descripcion,
            modulo = p_modulo
        WHERE permiso_id = p_permiso_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -25102,
                'No se encontró el permiso indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25994,
                'Error inesperado al actualizar permiso: ' || SQLERRM
            );
    END actualizar_permiso;


    PROCEDURE eliminar_permiso (
        p_permiso_id IN permisos.permiso_id%TYPE
    ) AS
    BEGIN
        DELETE FROM permisos
        WHERE permiso_id = p_permiso_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -25103,
                'No se encontró el permiso indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25993,
                'Error inesperado al eliminar permiso: ' || SQLERRM
            );
    END eliminar_permiso;


    PROCEDURE listar_permisos (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                permiso_id,
                codigo_permiso,
                descripcion,
                modulo
            FROM permisos
            ORDER BY permiso_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25992,
                'Error inesperado al listar permisos: ' || SQLERRM
            );
    END listar_permisos;


    /*
        ============================================================
        CRUD USUARIOS
        ============================================================
    */

    PROCEDURE crear_usuario (
        p_rol_id IN usuarios.rol_id%TYPE,
        p_nombre_usuario IN usuarios.nombre_usuario%TYPE,
        p_password_hash IN usuarios.password_hash%TYPE,
        p_estado IN usuarios.estado%TYPE,
        p_usuario_id OUT usuarios.usuario_id%TYPE
    ) AS
    BEGIN
        INSERT INTO usuarios (
            rol_id,
            nombre_usuario,
            password_hash,
            estado
        )
        VALUES (
            p_rol_id,
            p_nombre_usuario,
            p_password_hash,
            p_estado
        )
        RETURNING usuario_id INTO p_usuario_id;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -25201,
                'No se pudo crear el usuario porque el nombre de usuario ya existe.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25991,
                'Error inesperado al crear usuario: ' || SQLERRM
            );
    END crear_usuario;


    PROCEDURE actualizar_usuario (
        p_usuario_id IN usuarios.usuario_id%TYPE,
        p_rol_id IN usuarios.rol_id%TYPE,
        p_nombre_usuario IN usuarios.nombre_usuario%TYPE,
        p_password_hash IN usuarios.password_hash%TYPE,
        p_estado IN usuarios.estado%TYPE
    ) AS
    BEGIN
        UPDATE usuarios
        SET
            rol_id = p_rol_id,
            nombre_usuario = p_nombre_usuario,
            password_hash = p_password_hash,
            estado = p_estado
        WHERE usuario_id = p_usuario_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -25202,
                'No se encontró el usuario indicado para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25990,
                'Error inesperado al actualizar usuario: ' || SQLERRM
            );
    END actualizar_usuario;


    PROCEDURE eliminar_usuario (
        p_usuario_id IN usuarios.usuario_id%TYPE
    ) AS
    BEGIN
        DELETE FROM usuarios
        WHERE usuario_id = p_usuario_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -25203,
                'No se encontró el usuario indicado para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25989,
                'Error inesperado al eliminar usuario: ' || SQLERRM
            );
    END eliminar_usuario;


    PROCEDURE listar_usuarios (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                u.usuario_id,
                u.rol_id,
                r.nombre_rol,
                u.nombre_usuario,
                u.estado
            FROM usuarios u
            INNER JOIN roles r
                ON u.rol_id = r.rol_id
            ORDER BY u.usuario_id;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25988,
                'Error inesperado al listar usuarios: ' || SQLERRM
            );
    END listar_usuarios;


    /*
        ============================================================
        CRUD ROL_PERMISOS
        ============================================================
    */

    PROCEDURE asignar_permiso_rol (
        p_rol_id IN rol_permisos.rol_id%TYPE,
        p_permiso_id IN rol_permisos.permiso_id%TYPE
    ) AS
    BEGIN
        INSERT INTO rol_permisos (
            rol_id,
            permiso_id
        )
        VALUES (
            p_rol_id,
            p_permiso_id
        );

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -25301,
                'El permiso ya está asignado al rol.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25987,
                'Error inesperado al asignar permiso a rol: ' || SQLERRM
            );
    END asignar_permiso_rol;


    PROCEDURE actualizar_permiso_rol (
        p_rol_id_actual IN rol_permisos.rol_id%TYPE,
        p_permiso_id_actual IN rol_permisos.permiso_id%TYPE,
        p_rol_id_nuevo IN rol_permisos.rol_id%TYPE,
        p_permiso_id_nuevo IN rol_permisos.permiso_id%TYPE
    ) AS
    BEGIN
        UPDATE rol_permisos
        SET
            rol_id = p_rol_id_nuevo,
            permiso_id = p_permiso_id_nuevo
        WHERE rol_id = p_rol_id_actual
          AND permiso_id = p_permiso_id_actual;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -25302,
                'No se encontró la asignación rol-permiso indicada para actualizar.'
            );
        END IF;

    EXCEPTION
        WHEN DUP_VAL_ON_INDEX THEN
            RAISE_APPLICATION_ERROR(
                -25303,
                'No se puede actualizar porque la nueva asignación ya existe.'
            );

        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25986,
                'Error inesperado al actualizar permiso de rol: ' || SQLERRM
            );
    END actualizar_permiso_rol;


    PROCEDURE eliminar_permiso_rol (
        p_rol_id IN rol_permisos.rol_id%TYPE,
        p_permiso_id IN rol_permisos.permiso_id%TYPE
    ) AS
    BEGIN
        DELETE FROM rol_permisos
        WHERE rol_id = p_rol_id
          AND permiso_id = p_permiso_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(
                -25304,
                'No se encontró la asignación rol-permiso indicada para eliminar.'
            );
        END IF;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25985,
                'Error inesperado al eliminar permiso de rol: ' || SQLERRM
            );
    END eliminar_permiso_rol;


    PROCEDURE listar_rol_permisos (
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                rp.rol_id,
                r.nombre_rol,
                rp.permiso_id,
                p.codigo_permiso,
                p.descripcion,
                p.modulo
            FROM rol_permisos rp
            INNER JOIN roles r
                ON rp.rol_id = r.rol_id
            INNER JOIN permisos p
                ON rp.permiso_id = p.permiso_id
            ORDER BY r.nombre_rol, p.codigo_permiso;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25984,
                'Error inesperado al listar rol-permisos: ' || SQLERRM
            );
    END listar_rol_permisos;


    PROCEDURE listar_permisos_por_rol (
        p_rol_id IN rol_permisos.rol_id%TYPE,
        p_resultado OUT SYS_REFCURSOR
    ) AS
    BEGIN
        OPEN p_resultado FOR
            SELECT
                rp.rol_id,
                r.nombre_rol,
                rp.permiso_id,
                p.codigo_permiso,
                p.descripcion,
                p.modulo
            FROM rol_permisos rp
            INNER JOIN roles r
                ON rp.rol_id = r.rol_id
            INNER JOIN permisos p
                ON rp.permiso_id = p.permiso_id
            WHERE rp.rol_id = p_rol_id
            ORDER BY p.codigo_permiso;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE_APPLICATION_ERROR(
                -25983,
                'Error inesperado al listar permisos por rol: ' || SQLERRM
            );
    END listar_permisos_por_rol;

END pkg_smilecare_crud_seguridad;
/

SHOW ERRORS PACKAGE BODY pkg_smilecare_crud_seguridad;


PROMPT ============================================================
PROMPT VERIFICANDO ESTADO DEL PAQUETE
PROMPT ============================================================

SELECT
    object_name,
    object_type,
    status
FROM user_objects
WHERE object_name = 'PKG_SMILECARE_CRUD_SEGURIDAD'
ORDER BY object_type;