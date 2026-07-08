-- ============================================================
-- PROYECTO SMILECARE
-- 11_verificacion_final.sql
--
-- Objetivo:
-- Verificar automáticamente que la instalación final contiene:
--
-- 1. 30 tablas
-- 2. 5 paquetes válidos
-- 3. 5 package bodies válidos
-- 4. 6 triggers de auditoría habilitados
-- 5. Al menos 4 procedimientos con SYS_REFCURSOR
-- 6. Los 4 roles finales
-- 7. Los 17 permisos utilizados por la aplicación
-- 8. Los 4 usuarios demo
-- ============================================================


SET DEFINE OFF;
SET SERVEROUTPUT ON;


PROMPT ============================================================
PROMPT VERIFICACION FINAL DE SMILECARE
PROMPT ============================================================


DECLARE

    v_tablas NUMBER;

    v_packages NUMBER;

    v_package_bodies NUMBER;

    v_triggers NUMBER;

    v_cursores NUMBER;

    v_roles NUMBER;

    v_permisos NUMBER;

    v_usuarios_demo NUMBER;

    v_invalidos NUMBER;


BEGIN

    -- ========================================================
    -- 1. TABLAS
    -- ========================================================


    SELECT COUNT(*)
    INTO v_tablas
    FROM user_tables
    WHERE table_name IN (
        'ROLES',
        'PERMISOS',
        'ROL_PERMISOS',
        'USUARIOS',

        'PACIENTES',
        'ESPECIALIDADES',
        'DOCTORES',

        'CITAS',
        'CONSULTAS',
        'HISTORIAL_MEDICO',
        'HORARIOS_DOCTORES',
        'DISPONIBILIDAD_DOCTORES',
        'TRATAMIENTOS',
        'TRATAMIENTOS_CONSULTA',
        'CIRUGIAS',

        'METODOS_PAGO',
        'FACTURAS',
        'DETALLE_FACTURA',
        'PAGOS',
        'COMPROBANTES',

        'PROVEEDORES',
        'INSUMOS',
        'INVENTARIO_STOCK',
        'COMPRAS',
        'DETALLE_COMPRA',
        'MOVIMIENTOS_INVENTARIO',

        'AUDITORIA_ACCIONES',
        'AUDITORIA_SISTEMA',
        'HISTORIAL_ACCESOS',
        'PASSWORD_RESET_TOKENS'
    );


    -- ========================================================
    -- 2. PACKAGE SPECS
    -- ========================================================


    SELECT COUNT(*)
    INTO v_packages
    FROM user_objects
    WHERE object_type = 'PACKAGE'
      AND status = 'VALID'
      AND object_name IN (
            'PKG_SMILECARE_CRUD_CORE',
            'PKG_SMILECARE_CRUD_FINANZAS',
            'PKG_SMILECARE_CRUD_INVENTARIO',
            'PKG_SMILECARE_CRUD_CLINICO',
            'PKG_SMILECARE_CRUD_SEGURIDAD'
      );


    -- ========================================================
    -- 3. PACKAGE BODIES
    -- ========================================================


    SELECT COUNT(*)
    INTO v_package_bodies
    FROM user_objects
    WHERE object_type = 'PACKAGE BODY'
      AND status = 'VALID'
      AND object_name IN (
            'PKG_SMILECARE_CRUD_CORE',
            'PKG_SMILECARE_CRUD_FINANZAS',
            'PKG_SMILECARE_CRUD_INVENTARIO',
            'PKG_SMILECARE_CRUD_CLINICO',
            'PKG_SMILECARE_CRUD_SEGURIDAD'
      );


    -- ========================================================
    -- 4. TRIGGERS
    -- ========================================================


    SELECT COUNT(*)
    INTO v_triggers
    FROM user_triggers
    WHERE status = 'ENABLED'
      AND trigger_name IN (
            'TRG_AUD_PACIENTES_INSERT',
            'TRG_AUD_DOCTORES_INSERT',
            'TRG_AUD_CITAS_UPDATE',
            'TRG_AUD_FACTURAS_UPDATE',
            'TRG_AUD_TRATAMIENTOS_CONSULTA_DELETE',
            'TRG_AUD_MOVIMIENTOS_INVENTARIO_DELETE'
      );


    -- ========================================================
    -- 5. PROCEDIMIENTOS CON CURSOR
    -- ========================================================
    --
    -- Cada referencia SYS_REFCURSOR en las especificaciones
    -- de los paquetes representa un procedimiento que devuelve
    -- un cursor.
    -- ========================================================


    SELECT COUNT(*)
    INTO v_cursores
    FROM user_source
    WHERE type = 'PACKAGE'
      AND name IN (
            'PKG_SMILECARE_CRUD_CORE',
            'PKG_SMILECARE_CRUD_FINANZAS',
            'PKG_SMILECARE_CRUD_INVENTARIO',
            'PKG_SMILECARE_CRUD_CLINICO',
            'PKG_SMILECARE_CRUD_SEGURIDAD'
      )
      AND UPPER(text) LIKE '%SYS_REFCURSOR%';


    -- ========================================================
    -- 6. ROLES
    -- ========================================================


    SELECT COUNT(*)
    INTO v_roles
    FROM roles
    WHERE nombre_rol IN (
        'ADMIN',
        'DOCTOR',
        'INVENTARIO',
        'RECEPCIONISTA'
    );


    -- ========================================================
    -- 7. PERMISOS
    -- ========================================================


    SELECT COUNT(*)
    INTO v_permisos
    FROM permisos
    WHERE codigo_permiso IN (
        'PACIENTES_VER',
        'CITAS_GESTIONAR',
        'ADMIN_GESTIONAR',
        'FACTURAS_VER',
        'PACIENTES_GESTIONAR',
        'PROVEEDORES_GESTIONAR',
        'EXPEDIENTE_GESTIONAR',
        'INVENTARIO_VER',
        'CAJA_USAR',
        'INVENTARIO_GESTIONAR',
        'COMPRAS_GESTIONAR',
        'DOCTORES_GESTIONAR',
        'CONSULTAS_GESTIONAR',
        'METODOS_PAGO_GESTIONAR',
        'AGENDA_GESTIONAR',
        'TRATAMIENTOS_GESTIONAR',
        'PAGOS_VER'
    );


    -- ========================================================
    -- 8. USUARIOS DEMO
    -- ========================================================


    SELECT COUNT(*)
    INTO v_usuarios_demo
    FROM usuarios
    WHERE nombre_usuario IN (
        'admin',
        'doctor',
        'inventario',
        'recepcionista'
    );


    -- ========================================================
    -- 9. OBJETOS INVALIDOS
    -- ========================================================


    SELECT COUNT(*)
    INTO v_invalidos
    FROM user_objects
    WHERE status = 'INVALID'
      AND (
            object_name IN (
                'PKG_SMILECARE_CRUD_CORE',
                'PKG_SMILECARE_CRUD_FINANZAS',
                'PKG_SMILECARE_CRUD_INVENTARIO',
                'PKG_SMILECARE_CRUD_CLINICO',
                'PKG_SMILECARE_CRUD_SEGURIDAD'
            )

            OR object_name IN (
                'TRG_AUD_PACIENTES_INSERT',
                'TRG_AUD_DOCTORES_INSERT',
                'TRG_AUD_CITAS_UPDATE',
                'TRG_AUD_FACTURAS_UPDATE',
                'TRG_AUD_TRATAMIENTOS_CONSULTA_DELETE',
                'TRG_AUD_MOVIMIENTOS_INVENTARIO_DELETE'
            )
      );


    -- ========================================================
    -- RESULTADOS
    -- ========================================================


    DBMS_OUTPUT.PUT_LINE(
        '============================================================'
    );

    DBMS_OUTPUT.PUT_LINE(
        'RESULTADOS DE VERIFICACION'
    );

    DBMS_OUTPUT.PUT_LINE(
        '============================================================'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Tablas encontradas: '
        || v_tablas
        || ' / 30'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Paquetes VALID: '
        || v_packages
        || ' / 5'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Package bodies VALID: '
        || v_package_bodies
        || ' / 5'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Triggers ENABLED: '
        || v_triggers
        || ' / 6'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Procedimientos con cursor detectados: '
        || v_cursores
        || ' (mínimo requerido: 4)'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Roles finales: '
        || v_roles
        || ' / 4'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Permisos de aplicación: '
        || v_permisos
        || ' / 17'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Usuarios demo: '
        || v_usuarios_demo
        || ' / 4'
    );


    DBMS_OUTPUT.PUT_LINE(
        'Objetos inválidos encontrados: '
        || v_invalidos
    );


    DBMS_OUTPUT.PUT_LINE(
        '============================================================'
    );


    -- ========================================================
    -- RESULTADO FINAL
    -- ========================================================


    IF
        v_tablas = 30
        AND v_packages = 5
        AND v_package_bodies = 5
        AND v_triggers = 6
        AND v_cursores >= 4
        AND v_roles = 4
        AND v_permisos = 17
        AND v_usuarios_demo = 4
        AND v_invalidos = 0
    THEN

        DBMS_OUTPUT.PUT_LINE(
            'RESULTADO: Verificacion Oracle correcta.'
        );

    ELSE

        DBMS_OUTPUT.PUT_LINE(
            'RESULTADO: La instalacion requiere revision.'
        );

        RAISE_APPLICATION_ERROR(
            -20020,
            'La verificacion final de SmileCare '
            || 'no cumplio todos los requisitos.'
        );

    END IF;


END;
/


-- ============================================================
-- DETALLE DE PAQUETES
-- ============================================================


PROMPT ============================================================
PROMPT ESTADO DE PAQUETES
PROMPT ============================================================


SELECT
    object_name,
    object_type,
    status
FROM user_objects
WHERE object_name IN (
    'PKG_SMILECARE_CRUD_CORE',
    'PKG_SMILECARE_CRUD_FINANZAS',
    'PKG_SMILECARE_CRUD_INVENTARIO',
    'PKG_SMILECARE_CRUD_CLINICO',
    'PKG_SMILECARE_CRUD_SEGURIDAD'
)
ORDER BY
    object_name,
    object_type;


-- ============================================================
-- DETALLE DE TRIGGERS
-- ============================================================


PROMPT ============================================================
PROMPT ESTADO DE TRIGGERS
PROMPT ============================================================


SELECT
    trigger_name,
    table_name,
    triggering_event,
    status
FROM user_triggers
WHERE trigger_name IN (
    'TRG_AUD_PACIENTES_INSERT',
    'TRG_AUD_DOCTORES_INSERT',
    'TRG_AUD_CITAS_UPDATE',
    'TRG_AUD_FACTURAS_UPDATE',
    'TRG_AUD_TRATAMIENTOS_CONSULTA_DELETE',
    'TRG_AUD_MOVIMIENTOS_INVENTARIO_DELETE'
)
ORDER BY trigger_name;


-- ============================================================
-- DETALLE DE ROLES Y PERMISOS
-- ============================================================


PROMPT ============================================================
PROMPT PERMISOS POR ROL
PROMPT ============================================================


SELECT
    r.nombre_rol,
    COUNT(rp.permiso_id)
        AS cantidad_permisos
FROM roles r
LEFT JOIN rol_permisos rp
    ON rp.rol_id = r.rol_id
WHERE r.nombre_rol IN (
    'ADMIN',
    'DOCTOR',
    'INVENTARIO',
    'RECEPCIONISTA'
)
GROUP BY r.nombre_rol
ORDER BY r.nombre_rol;


-- ============================================================
-- TABLAS DE AUDITORIA Y RECUPERACION
-- ============================================================


PROMPT ============================================================
PROMPT TABLAS DE AUDITORIA Y RECUPERACION
PROMPT ============================================================


SELECT
    table_name
FROM user_tables
WHERE table_name IN (
    'AUDITORIA_ACCIONES',
    'AUDITORIA_SISTEMA',
    'HISTORIAL_ACCESOS',
    'PASSWORD_RESET_TOKENS'
)
ORDER BY table_name;


PROMPT ============================================================
PROMPT FIN DE 11_verificacion_final.sql
PROMPT ============================================================