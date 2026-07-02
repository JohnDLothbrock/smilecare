SET SERVEROUTPUT ON;

PROMPT ============================================================
PROMPT VERIFICACION FINAL ORACLE - SMILECARE
PROMPT ============================================================


PROMPT ============================================================
PROMPT 1. VERIFICANDO TABLAS PRINCIPALES
PROMPT ============================================================

SELECT
    table_name
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
    'TRATAMIENTOS',
    'TRATAMIENTOS_CONSULTA',
    'FACTURAS',
    'DETALLE_FACTURA',
    'METODOS_PAGO',
    'PAGOS',
    'COMPROBANTES',
    'HISTORIAL_MEDICO',
    'CIRUGIAS',
    'HORARIOS_DOCTORES',
    'DISPONIBILIDAD_DOCTORES',
    'PROVEEDORES',
    'INSUMOS',
    'INVENTARIO_STOCK',
    'COMPRAS',
    'DETALLE_COMPRA',
    'MOVIMIENTOS_INVENTARIO',
    'AUDITORIA_ACCIONES'
)
ORDER BY table_name;


PROMPT ============================================================
PROMPT 2. VERIFICANDO PAQUETES Y PACKAGE BODIES
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
ORDER BY object_name, object_type;


PROMPT ============================================================
PROMPT 3. VERIFICANDO TRIGGERS DE AUDITORIA
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


PROMPT ============================================================
PROMPT 4. VERIFICANDO PROCEDIMIENTOS CON SYS_REFCURSOR
PROMPT ============================================================

/*
    Esta consulta ayuda a evidenciar procedimientos que usan cursores.
    Dependiendo de la versión de Oracle, SYS_REFCURSOR puede aparecer como
    REF CURSOR en USER_ARGUMENTS.
*/

SELECT
    package_name,
    object_name AS procedure_name,
    argument_name,
    in_out,
    data_type
FROM user_arguments
WHERE package_name IN (
    'PKG_SMILECARE_CRUD_CORE',
    'PKG_SMILECARE_CRUD_FINANZAS',
    'PKG_SMILECARE_CRUD_INVENTARIO',
    'PKG_SMILECARE_CRUD_CLINICO',
    'PKG_SMILECARE_CRUD_SEGURIDAD'
)
AND UPPER(argument_name) = 'P_RESULTADO'
ORDER BY package_name, object_name;


PROMPT ============================================================
PROMPT 5. VERIFICANDO CONSULTAS CON REGEXP
PROMPT ============================================================

/*
    Estas consultas usan REGEXP_LIKE para confirmar que las expresiones
    regulares funcionan correctamente sobre las tablas del proyecto.
*/

SELECT
    'Pacientes con correo valido' AS validacion,
    COUNT(*) AS cantidad
FROM pacientes
WHERE correo IS NOT NULL
  AND REGEXP_LIKE(
        correo,
        '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        'i'
      );

SELECT
    'Pacientes con telefono valido' AS validacion,
    COUNT(*) AS cantidad
FROM pacientes
WHERE telefono IS NOT NULL
  AND REGEXP_LIKE(
        telefono,
        '^[0-9]{4}-?[0-9]{4}$'
      );

SELECT
    'Doctores con correo valido' AS validacion,
    COUNT(*) AS cantidad
FROM doctores
WHERE correo IS NOT NULL
  AND REGEXP_LIKE(
        correo,
        '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        'i'
      );

SELECT
    'Usuarios con nombre valido' AS validacion,
    COUNT(*) AS cantidad
FROM usuarios
WHERE REGEXP_LIKE(
        nombre_usuario,
        '^[A-Za-z][A-Za-z0-9_]{3,49}$'
      );


PROMPT ============================================================
PROMPT 6. RESUMEN GENERAL
PROMPT ============================================================

DECLARE
    v_tablas NUMBER;
    v_paquetes_validos NUMBER;
    v_package_bodies_validos NUMBER;
    v_triggers_enabled NUMBER;
    v_cursor_args NUMBER;
BEGIN
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
        'TRATAMIENTOS',
        'TRATAMIENTOS_CONSULTA',
        'FACTURAS',
        'DETALLE_FACTURA',
        'METODOS_PAGO',
        'PAGOS',
        'COMPROBANTES',
        'HISTORIAL_MEDICO',
        'CIRUGIAS',
        'HORARIOS_DOCTORES',
        'DISPONIBILIDAD_DOCTORES',
        'PROVEEDORES',
        'INSUMOS',
        'INVENTARIO_STOCK',
        'COMPRAS',
        'DETALLE_COMPRA',
        'MOVIMIENTOS_INVENTARIO',
        'AUDITORIA_ACCIONES'
    );

    SELECT COUNT(*)
    INTO v_paquetes_validos
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

    SELECT COUNT(*)
    INTO v_package_bodies_validos
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

    SELECT COUNT(*)
    INTO v_triggers_enabled
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

    SELECT COUNT(*)
    INTO v_cursor_args
    FROM user_arguments
    WHERE package_name IN (
        'PKG_SMILECARE_CRUD_CORE',
        'PKG_SMILECARE_CRUD_FINANZAS',
        'PKG_SMILECARE_CRUD_INVENTARIO',
        'PKG_SMILECARE_CRUD_CLINICO',
        'PKG_SMILECARE_CRUD_SEGURIDAD'
    )
    AND UPPER(argument_name) = 'P_RESULTADO';

    DBMS_OUTPUT.PUT_LINE('============================================');
    DBMS_OUTPUT.PUT_LINE('RESUMEN DE VERIFICACION');
    DBMS_OUTPUT.PUT_LINE('============================================');
    DBMS_OUTPUT.PUT_LINE('Tablas encontradas: ' || v_tablas);
    DBMS_OUTPUT.PUT_LINE('Paquetes VALID: ' || v_paquetes_validos);
    DBMS_OUTPUT.PUT_LINE('Package bodies VALID: ' || v_package_bodies_validos);
    DBMS_OUTPUT.PUT_LINE('Triggers ENABLED: ' || v_triggers_enabled);
    DBMS_OUTPUT.PUT_LINE('Procedimientos con cursor detectados: ' || v_cursor_args);
    DBMS_OUTPUT.PUT_LINE('============================================');

    IF v_paquetes_validos = 5
       AND v_package_bodies_validos = 5
       AND v_triggers_enabled >= 6
       AND v_cursor_args >= 4 THEN

        DBMS_OUTPUT.PUT_LINE('RESULTADO: Verificacion Oracle correcta.');

    ELSE
        DBMS_OUTPUT.PUT_LINE('RESULTADO: Revisar objetos faltantes o invalidos.');
    END IF;
END;
/