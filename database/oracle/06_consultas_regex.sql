SET SERVEROUTPUT ON;

PROMPT ============================================================
PROMPT CONSULTAS CON EXPRESIONES REGULARES - SMILECARE
PROMPT ============================================================

/*
    Archivo: 06_consultas_regex.sql
    Proyecto: SmileCare
    Curso: SC-504 Lenguajes de Base de Datos

    Objetivo:
    Cumplir el requisito del proyecto de incluir consultas con expresiones
    regulares en Oracle.

    Este archivo contiene consultas usando:
    - REGEXP_LIKE
    - REGEXP_SUBSTR
    - REGEXP_REPLACE

    Requisito del proyecto:
    - Al menos cuatro consultas deben incluir expresiones regulares.

    Este archivo incluye más de cuatro consultas para dejar evidencia clara.
*/


PROMPT ============================================================
PROMPT 1. PACIENTES CON CORREO VALIDO
PROMPT ============================================================

/*
    Esta consulta valida correos de pacientes usando REGEXP_LIKE.
    Busca correos con formato básico:
    texto@dominio.extension
*/

SELECT
    paciente_id,
    nombre,
    apellido,
    correo
FROM pacientes
WHERE correo IS NOT NULL
  AND REGEXP_LIKE(
        correo,
        '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        'i'
      )
ORDER BY paciente_id;


PROMPT ============================================================
PROMPT 2. PACIENTES CON CORREO INVALIDO
PROMPT ============================================================

/*
    Esta consulta encuentra pacientes cuyo correo NO cumple el formato.
    Sirve como control de calidad de datos.
*/

SELECT
    paciente_id,
    nombre,
    apellido,
    correo
FROM pacientes
WHERE correo IS NOT NULL
  AND NOT REGEXP_LIKE(
        correo,
        '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        'i'
      )
ORDER BY paciente_id;


PROMPT ============================================================
PROMPT 3. DOCTORES CON CORREO VALIDO
PROMPT ============================================================

/*
    Esta consulta valida correos de doctores.
    Usa la misma regla de validación de email.
*/

SELECT
    doctor_id,
    nombre,
    apellido,
    correo
FROM doctores
WHERE correo IS NOT NULL
  AND REGEXP_LIKE(
        correo,
        '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        'i'
      )
ORDER BY doctor_id;


PROMPT ============================================================
PROMPT 4. TELEFONOS DE PACIENTES CON FORMATO COSTA RICA
PROMPT ============================================================

/*
    Esta consulta busca teléfonos con formato básico de Costa Rica.
    Acepta:
    - 88889999
    - 8888-9999
*/

SELECT
    paciente_id,
    nombre,
    apellido,
    telefono
FROM pacientes
WHERE telefono IS NOT NULL
  AND REGEXP_LIKE(
        telefono,
        '^[0-9]{4}-?[0-9]{4}$'
      )
ORDER BY paciente_id;


PROMPT ============================================================
PROMPT 5. TELEFONOS DE DOCTORES CON FORMATO COSTA RICA
PROMPT ============================================================

/*
    Esta consulta busca teléfonos de doctores con 8 dígitos,
    con o sin guion en el centro.
*/

SELECT
    doctor_id,
    nombre,
    apellido,
    telefono
FROM doctores
WHERE telefono IS NOT NULL
  AND REGEXP_LIKE(
        telefono,
        '^[0-9]{4}-?[0-9]{4}$'
      )
ORDER BY doctor_id;


PROMPT ============================================================
PROMPT 6. USUARIOS CON NOMBRE DE USUARIO VALIDO
PROMPT ============================================================

/*
    Esta consulta valida el nombre de usuario.
    Regla:
    - Debe iniciar con letra.
    - Puede contener letras, números y guion bajo.
    - Debe tener mínimo 4 caracteres.
*/

SELECT
    usuario_id,
    nombre_usuario,
    estado
FROM usuarios
WHERE REGEXP_LIKE(
        nombre_usuario,
        '^[A-Za-z][A-Za-z0-9_]{3,49}$'
      )
ORDER BY usuario_id;


PROMPT ============================================================
PROMPT 7. INSUMOS CON CODIGO ALFANUMERICO VALIDO
PROMPT ============================================================

/*
    Esta consulta valida códigos de insumos.
    Regla flexible:
    - Letras mayúsculas al inicio.
    - Puede tener guion.
    - Puede tener números al final.
    Ejemplos válidos:
    - INS-001
    - GUANTES-100
    - ANEST01
*/

SELECT
    insumo_id,
    codigo,
    nombre,
    estado
FROM insumos
WHERE REGEXP_LIKE(
        codigo,
        '^[A-Z]+-?[0-9]+$'
      )
ORDER BY insumo_id;


PROMPT ============================================================
PROMPT 8. PROVEEDORES CON CORREO CORPORATIVO O COMERCIAL
PROMPT ============================================================

/*
    Esta consulta busca proveedores cuyo correo tenga dominios comunes.
    Usa REGEXP_LIKE con varias opciones.
*/

SELECT
    proveedor_id,
    nombre,
    correo,
    estado
FROM proveedores
WHERE correo IS NOT NULL
  AND REGEXP_LIKE(
        correo,
        '@(gmail|outlook|hotmail|yahoo|empresa|clinic|dental|medical)\.',
        'i'
      )
ORDER BY proveedor_id;


PROMPT ============================================================
PROMPT 9. EXTRAER DOMINIO DEL CORREO DE PACIENTES
PROMPT ============================================================

/*
    Esta consulta usa REGEXP_SUBSTR para extraer el dominio del correo.
    Ejemplo:
    juan@gmail.com -> gmail.com
*/

SELECT
    paciente_id,
    nombre,
    apellido,
    correo,
    REGEXP_SUBSTR(
        correo,
        '[^@]+$'
    ) AS dominio_correo
FROM pacientes
WHERE correo IS NOT NULL
ORDER BY paciente_id;


PROMPT ============================================================
PROMPT 10. LIMPIAR TELEFONOS DE PACIENTES
PROMPT ============================================================

/*
    Esta consulta usa REGEXP_REPLACE para dejar solo números.
    Ejemplo:
    8888-9999 -> 88889999
*/

SELECT
    paciente_id,
    nombre,
    apellido,
    telefono,
    REGEXP_REPLACE(
        telefono,
        '[^0-9]',
        ''
    ) AS telefono_solo_numeros
FROM pacientes
WHERE telefono IS NOT NULL
ORDER BY paciente_id;


PROMPT ============================================================
PROMPT 11. PACIENTES CON CARACTERES NO VALIDOS EN NOMBRE
PROMPT ============================================================

/*
    Esta consulta detecta nombres con caracteres no esperados.
    Permite letras, espacios y vocales con tilde.
*/

SELECT
    paciente_id,
    nombre,
    apellido
FROM pacientes
WHERE REGEXP_LIKE(
        nombre || ' ' || apellido,
        '[^A-Za-zÁÉÍÓÚáéíóúÑñ ]'
      )
ORDER BY paciente_id;


PROMPT ============================================================
PROMPT 12. FACTURAS CON NUMERO DE FACTURA CON FORMATO ESPERADO
PROMPT ============================================================

/*
    Esta consulta valida números de factura.
    Regla sugerida:
    - FAC-
    - cuatro dígitos de año
    - guion
    - número consecutivo de 3 a 8 dígitos

    Ejemplo:
    FAC-2026-001
    FAC-2026-000123
*/

SELECT
    factura_id,
    numero_factura,
    fecha_emision,
    total,
    estado
FROM facturas
WHERE REGEXP_LIKE(
        numero_factura,
        '^FAC-[0-9]{4}-[0-9]{3,8}$'
      )
ORDER BY factura_id;


PROMPT ============================================================
PROMPT RESUMEN DE VALIDACIONES REGEX
PROMPT ============================================================

/*
    Este bloque imprime un resumen de algunas validaciones.
*/

DECLARE
    v_pacientes_correo_valido NUMBER;
    v_pacientes_correo_invalido NUMBER;
    v_doctores_correo_valido NUMBER;
    v_telefonos_pacientes_validos NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_pacientes_correo_valido
    FROM pacientes
    WHERE correo IS NOT NULL
      AND REGEXP_LIKE(
            correo,
            '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            'i'
          );

    SELECT COUNT(*)
    INTO v_pacientes_correo_invalido
    FROM pacientes
    WHERE correo IS NOT NULL
      AND NOT REGEXP_LIKE(
            correo,
            '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            'i'
          );

    SELECT COUNT(*)
    INTO v_doctores_correo_valido
    FROM doctores
    WHERE correo IS NOT NULL
      AND REGEXP_LIKE(
            correo,
            '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            'i'
          );

    SELECT COUNT(*)
    INTO v_telefonos_pacientes_validos
    FROM pacientes
    WHERE telefono IS NOT NULL
      AND REGEXP_LIKE(
            telefono,
            '^[0-9]{4}-?[0-9]{4}$'
          );

    DBMS_OUTPUT.PUT_LINE('Pacientes con correo válido: ' || v_pacientes_correo_valido);
    DBMS_OUTPUT.PUT_LINE('Pacientes con correo inválido: ' || v_pacientes_correo_invalido);
    DBMS_OUTPUT.PUT_LINE('Doctores con correo válido: ' || v_doctores_correo_valido);
    DBMS_OUTPUT.PUT_LINE('Pacientes con teléfono válido: ' || v_telefonos_pacientes_validos);
END;
/