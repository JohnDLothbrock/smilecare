-- ============================================================
-- PROYECTO SMILECARE
-- 09_rbac_usuarios_demo.sql
--
-- Objetivo:
--
-- 1. Crear los cuatro roles finales del sistema.
-- 2. Crear los permisos utilizados por FastAPI y React.
-- 3. Asignar permisos a cada rol.
-- 4. Crear cuatro cuentas de demostración.
--
-- El script puede ejecutarse más de una vez.
-- ============================================================


SET DEFINE OFF;
SET SERVEROUTPUT ON;


PROMPT ============================================================
PROMPT CONFIGURANDO ROLES Y PERMISOS DE SMILECARE
PROMPT ============================================================


-- ============================================================
-- 1. ROLES
-- ============================================================


MERGE INTO roles r
USING (
    SELECT
        'ADMIN' AS nombre_rol,
        'Acceso completo al sistema.' AS descripcion,
        'ACTIVO' AS estado
    FROM dual

    UNION ALL

    SELECT
        'DOCTOR',
        'Acceso clínico y operativo sin administración.',
        'ACTIVO'
    FROM dual

    UNION ALL

    SELECT
        'INVENTARIO',
        'Gestión de proveedores, compras e inventario.',
        'ACTIVO'
    FROM dual

    UNION ALL

    SELECT
        'RECEPCIONISTA',
        'Gestión de pacientes, agenda y finanzas.',
        'ACTIVO'
    FROM dual
) src
ON (
    UPPER(r.nombre_rol)
    =
    UPPER(src.nombre_rol)
)
WHEN MATCHED THEN
    UPDATE SET
        r.descripcion = src.descripcion,
        r.estado = src.estado
WHEN NOT MATCHED THEN
    INSERT (
        nombre_rol,
        descripcion,
        estado
    )
    VALUES (
        src.nombre_rol,
        src.descripcion,
        src.estado
    );


-- ============================================================
-- 2. PERMISOS
-- ============================================================


MERGE INTO permisos p
USING (
    SELECT
        'PACIENTES_VER' AS codigo_permiso,
        'Ver información de pacientes.' AS descripcion,
        'Clínica' AS modulo
    FROM dual

    UNION ALL

    SELECT
        'CITAS_GESTIONAR',
        'Gestionar citas médicas.',
        'Clínica'
    FROM dual

    UNION ALL

    SELECT
        'ADMIN_GESTIONAR',
        'Gestionar usuarios, roles y permisos.',
        'Administración'
    FROM dual

    UNION ALL

    SELECT
        'FACTURAS_VER',
        'Ver y revisar facturas.',
        'Finanzas'
    FROM dual

    UNION ALL

    SELECT
        'PACIENTES_GESTIONAR',
        'Crear, editar y eliminar pacientes.',
        'Clínica'
    FROM dual

    UNION ALL

    SELECT
        'PROVEEDORES_GESTIONAR',
        'Gestionar proveedores.',
        'Inventario'
    FROM dual

    UNION ALL

    SELECT
        'EXPEDIENTE_GESTIONAR',
        'Gestionar expediente clínico.',
        'Clínica'
    FROM dual

    UNION ALL

    SELECT
        'INVENTARIO_VER',
        'Ver inventario y existencias.',
        'Inventario'
    FROM dual

    UNION ALL

    SELECT
        'CAJA_USAR',
        'Gestionar caja, facturación y cobros.',
        'Finanzas'
    FROM dual

    UNION ALL

    SELECT
        'INVENTARIO_GESTIONAR',
        'Gestionar existencias y movimientos.',
        'Inventario'
    FROM dual

    UNION ALL

    SELECT
        'COMPRAS_GESTIONAR',
        'Gestionar compras e insumos.',
        'Inventario'
    FROM dual

    UNION ALL

    SELECT
        'DOCTORES_GESTIONAR',
        'Gestionar doctores y especialidades.',
        'Clínica'
    FROM dual

    UNION ALL

    SELECT
        'CONSULTAS_GESTIONAR',
        'Gestionar consultas y atención clínica.',
        'Clínica'
    FROM dual

    UNION ALL

    SELECT
        'METODOS_PAGO_GESTIONAR',
        'Gestionar métodos de pago.',
        'Finanzas'
    FROM dual

    UNION ALL

    SELECT
        'AGENDA_GESTIONAR',
        'Gestionar horarios y disponibilidad médica.',
        'Clínica'
    FROM dual

    UNION ALL

    SELECT
        'TRATAMIENTOS_GESTIONAR',
        'Gestionar catálogo de tratamientos.',
        'Clínica'
    FROM dual

    UNION ALL

    SELECT
        'PAGOS_VER',
        'Ver pagos registrados.',
        'Finanzas'
    FROM dual
) src
ON (
    UPPER(p.codigo_permiso)
    =
    UPPER(src.codigo_permiso)
)
WHEN MATCHED THEN
    UPDATE SET
        p.descripcion = src.descripcion,
        p.modulo = src.modulo
WHEN NOT MATCHED THEN
    INSERT (
        codigo_permiso,
        descripcion,
        modulo
    )
    VALUES (
        src.codigo_permiso,
        src.descripcion,
        src.modulo
    );


-- ============================================================
-- 3. LIMPIAR ASIGNACIONES DE LOS CUATRO ROLES FINALES
-- ============================================================
--
-- Se eliminan únicamente sus asignaciones.
--
-- Después se reconstruyen de acuerdo con el modelo final.
-- ============================================================


DELETE FROM rol_permisos
WHERE rol_id IN (
    SELECT rol_id
    FROM roles
    WHERE nombre_rol IN (
        'ADMIN',
        'DOCTOR',
        'INVENTARIO',
        'RECEPCIONISTA'
    )
);


-- ============================================================
-- 4. ADMIN
-- ============================================================
--
-- ADMIN recibe todos los permisos.
-- ============================================================


INSERT INTO rol_permisos (
    rol_id,
    permiso_id
)
SELECT
    r.rol_id,
    p.permiso_id
FROM roles r
CROSS JOIN permisos p
WHERE r.nombre_rol = 'ADMIN';


-- ============================================================
-- 5. DOCTOR
-- ============================================================
--
-- DOCTOR recibe todos los permisos excepto:
--
-- ADMIN_GESTIONAR
-- ============================================================


INSERT INTO rol_permisos (
    rol_id,
    permiso_id
)
SELECT
    r.rol_id,
    p.permiso_id
FROM roles r
CROSS JOIN permisos p
WHERE r.nombre_rol = 'DOCTOR'
  AND p.codigo_permiso <> 'ADMIN_GESTIONAR';


-- ============================================================
-- 6. INVENTARIO
-- ============================================================


INSERT INTO rol_permisos (
    rol_id,
    permiso_id
)
SELECT
    r.rol_id,
    p.permiso_id
FROM roles r
CROSS JOIN permisos p
WHERE r.nombre_rol = 'INVENTARIO'
  AND p.codigo_permiso IN (
        'PROVEEDORES_GESTIONAR',
        'INVENTARIO_VER',
        'INVENTARIO_GESTIONAR',
        'COMPRAS_GESTIONAR'
  );


-- ============================================================
-- 7. RECEPCIONISTA
-- ============================================================


INSERT INTO rol_permisos (
    rol_id,
    permiso_id
)
SELECT
    r.rol_id,
    p.permiso_id
FROM roles r
CROSS JOIN permisos p
WHERE r.nombre_rol = 'RECEPCIONISTA'
  AND p.codigo_permiso IN (
        'PACIENTES_VER',
        'PACIENTES_GESTIONAR',
        'CITAS_GESTIONAR',
        'AGENDA_GESTIONAR',
        'FACTURAS_VER',
        'CAJA_USAR',
        'METODOS_PAGO_GESTIONAR',
        'PAGOS_VER'
  );


-- ============================================================
-- 8. USUARIOS DEMO
-- ============================================================
--
-- Contraseña inicial para todas las cuentas:
--
-- SmileCare123!
--
-- La contraseña está almacenada como hash Argon2id.
--
-- IMPORTANTE:
--
-- Estas credenciales son únicamente para:
--
-- - desarrollo local
-- - pruebas
-- - demostraciones académicas
--
-- No utilizar en producción.
-- ============================================================


MERGE INTO usuarios u
USING (
    SELECT
        r.rol_id,
        'admin' AS nombre_usuario,
        CAST(NULL AS VARCHAR2(150)) AS correo,
        '$argon2id$v=19$m=65536,t=3,p=4$buv7IPi+peg/enJyVo8DIg$P2//9cT2hfQHAkD2xVLwQ35Mobsm4z0Bq6aXIef+2Yc'
            AS password_hash,
        'ACTIVO' AS estado
    FROM roles r
    WHERE r.nombre_rol = 'ADMIN'

    UNION ALL

    SELECT
        r.rol_id,
        'doctor',
        CAST(NULL AS VARCHAR2(150)),
        '$argon2id$v=19$m=65536,t=3,p=4$buv7IPi+peg/enJyVo8DIg$P2//9cT2hfQHAkD2xVLwQ35Mobsm4z0Bq6aXIef+2Yc',
        'ACTIVO'
    FROM roles r
    WHERE r.nombre_rol = 'DOCTOR'

    UNION ALL

    SELECT
        r.rol_id,
        'inventario',
        CAST(NULL AS VARCHAR2(150)),
        '$argon2id$v=19$m=65536,t=3,p=4$buv7IPi+peg/enJyVo8DIg$P2//9cT2hfQHAkD2xVLwQ35Mobsm4z0Bq6aXIef+2Yc',
        'ACTIVO'
    FROM roles r
    WHERE r.nombre_rol = 'INVENTARIO'

    UNION ALL

    SELECT
        r.rol_id,
        'recepcionista',
        CAST(NULL AS VARCHAR2(150)),
        '$argon2id$v=19$m=65536,t=3,p=4$buv7IPi+peg/enJyVo8DIg$P2//9cT2hfQHAkD2xVLwQ35Mobsm4z0Bq6aXIef+2Yc',
        'ACTIVO'
    FROM roles r
    WHERE r.nombre_rol = 'RECEPCIONISTA'
) src
ON (
    UPPER(u.nombre_usuario)
    =
    UPPER(src.nombre_usuario)
)
WHEN MATCHED THEN
    UPDATE SET
        u.rol_id = src.rol_id,
        u.estado = src.estado
WHEN NOT MATCHED THEN
    INSERT (
        rol_id,
        nombre_usuario,
        correo,
        password_hash,
        estado
    )
    VALUES (
        src.rol_id,
        src.nombre_usuario,
        src.correo,
        src.password_hash,
        src.estado
    );


COMMIT;


-- ============================================================
-- 9. CORREO DE RECUPERACION
-- ============================================================
--
-- Por seguridad no se incluye un correo personal real.
--
-- Para probar recuperación de contraseña:
--
-- 1. Inicie sesión como ADMIN.
-- 2. Abra Administración.
-- 3. Edite el usuario.
-- 4. Agregue un correo real.
--
-- También puede hacerse directamente con:
--
-- UPDATE usuarios
-- SET correo = 'correo_real@ejemplo.com'
-- WHERE nombre_usuario = 'admin';
--
-- COMMIT;
-- ============================================================


PROMPT ============================================================
PROMPT CREDENCIALES DEMO
PROMPT ============================================================

PROMPT Usuario: admin
PROMPT Usuario: doctor
PROMPT Usuario: inventario
PROMPT Usuario: recepcionista
PROMPT
PROMPT Contraseña para todos:
PROMPT SmileCare123!


PROMPT ============================================================
PROMPT ROLES CREADOS
PROMPT ============================================================


SELECT
    rol_id,
    nombre_rol,
    estado
FROM roles
WHERE nombre_rol IN (
    'ADMIN',
    'DOCTOR',
    'INVENTARIO',
    'RECEPCIONISTA'
)
ORDER BY nombre_rol;


PROMPT ============================================================
PROMPT PERMISOS POR ROL
PROMPT ============================================================


SELECT
    r.nombre_rol,
    COUNT(*) AS cantidad_permisos
FROM rol_permisos rp
INNER JOIN roles r
    ON r.rol_id = rp.rol_id
WHERE r.nombre_rol IN (
    'ADMIN',
    'DOCTOR',
    'INVENTARIO',
    'RECEPCIONISTA'
)
GROUP BY r.nombre_rol
ORDER BY r.nombre_rol;


PROMPT ============================================================
PROMPT USUARIOS DEMO
PROMPT ============================================================


SELECT
    u.usuario_id,
    u.nombre_usuario,
    r.nombre_rol,
    u.correo,
    u.estado
FROM usuarios u
INNER JOIN roles r
    ON r.rol_id = u.rol_id
WHERE u.nombre_usuario IN (
    'admin',
    'doctor',
    'inventario',
    'recepcionista'
)
ORDER BY u.usuario_id;


PROMPT ============================================================
PROMPT FIN DE 09_rbac_usuarios_demo.sql
PROMPT ============================================================