-- ============================================================
-- PROYECTO SMILECARE
-- 10_datos_demo.sql
--
-- Objetivo:
-- Crear información de demostración para:
--
-- 1. Pacientes
-- 2. Doctores
-- 3. Agenda
-- 4. Atención clínica
-- 5. Tratamientos y cirugía
-- 6. Facturación y pagos
-- 7. Proveedores
-- 8. Compras
-- 9. Inventario
--
-- Ejecutar después de:
--
-- 09_rbac_usuarios_demo.sql
-- ============================================================


SET DEFINE OFF;
SET SERVEROUTPUT ON;


PROMPT ============================================================
PROMPT CARGANDO DATOS DEMO DE SMILECARE
PROMPT ============================================================


DECLARE

    -- --------------------------------------------------------
    -- USUARIOS
    -- --------------------------------------------------------

    v_usuario_doctor_id NUMBER;
    v_usuario_inventario_id NUMBER;


    -- --------------------------------------------------------
    -- ESPECIALIDADES
    -- --------------------------------------------------------

    v_especialidad_general_id NUMBER;
    v_especialidad_cirugia_id NUMBER;


    -- --------------------------------------------------------
    -- PACIENTES
    -- --------------------------------------------------------

    v_paciente_1_id NUMBER;
    v_paciente_2_id NUMBER;
    v_paciente_3_id NUMBER;


    -- --------------------------------------------------------
    -- DOCTORES
    -- --------------------------------------------------------

    v_doctor_1_id NUMBER;
    v_doctor_2_id NUMBER;


    -- --------------------------------------------------------
    -- CITAS Y CONSULTAS
    -- --------------------------------------------------------

    v_cita_pasada_id NUMBER;
    v_cita_futura_1_id NUMBER;
    v_cita_futura_2_id NUMBER;

    v_consulta_id NUMBER;


    -- --------------------------------------------------------
    -- TRATAMIENTOS
    -- --------------------------------------------------------

    v_trat_limpieza_id NUMBER;
    v_trat_extraccion_id NUMBER;
    v_trat_resina_id NUMBER;
    v_trat_endodoncia_id NUMBER;

    v_tc_limpieza_id NUMBER;
    v_tc_extraccion_id NUMBER;


    -- --------------------------------------------------------
    -- FINANZAS
    -- --------------------------------------------------------

    v_metodo_efectivo_id NUMBER;
    v_metodo_tarjeta_id NUMBER;
    v_metodo_sinpe_id NUMBER;

    v_factura_id NUMBER;
    v_pago_id NUMBER;


    -- --------------------------------------------------------
    -- INVENTARIO
    -- --------------------------------------------------------

    v_proveedor_1_id NUMBER;
    v_proveedor_2_id NUMBER;

    v_insumo_guantes_id NUMBER;
    v_insumo_anestesia_id NUMBER;
    v_insumo_resina_id NUMBER;
    v_insumo_sutura_id NUMBER;

    v_compra_id NUMBER;
    v_detalle_guantes_id NUMBER;
    v_detalle_anestesia_id NUMBER;


    -- --------------------------------------------------------
    -- UTILIDAD
    -- --------------------------------------------------------

    v_count NUMBER;


BEGIN

    -- ========================================================
    -- 1. USUARIOS NECESARIOS
    -- ========================================================


    SELECT usuario_id
    INTO v_usuario_doctor_id
    FROM usuarios
    WHERE nombre_usuario = 'doctor';


    SELECT usuario_id
    INTO v_usuario_inventario_id
    FROM usuarios
    WHERE nombre_usuario = 'inventario';


    -- ========================================================
    -- 2. ESPECIALIDADES
    -- ========================================================


    MERGE INTO especialidades e
    USING (
        SELECT
            'Odontología General' AS nombre,
            'Atención odontológica general y preventiva.'
                AS descripcion
        FROM dual
    ) src
    ON (
        UPPER(e.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            e.descripcion = src.descripcion
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion
        )
        VALUES (
            src.nombre,
            src.descripcion
        );


    MERGE INTO especialidades e
    USING (
        SELECT
            'Cirugía Oral' AS nombre,
            'Procedimientos quirúrgicos odontológicos.'
                AS descripcion
        FROM dual
    ) src
    ON (
        UPPER(e.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            e.descripcion = src.descripcion
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion
        )
        VALUES (
            src.nombre,
            src.descripcion
        );


    SELECT especialidad_id
    INTO v_especialidad_general_id
    FROM especialidades
    WHERE nombre = 'Odontología General';


    SELECT especialidad_id
    INTO v_especialidad_cirugia_id
    FROM especialidades
    WHERE nombre = 'Cirugía Oral';


    -- ========================================================
    -- 3. PACIENTES
    -- ========================================================


    MERGE INTO pacientes p
    USING (
        SELECT
            'María' AS nombre,
            'Rodríguez' AS apellido,
            '8888-1111' AS telefono,
            'maria.rodriguez@smilecare.demo'
                AS correo,
            'Heredia, Costa Rica' AS direccion,
            TO_DATE(
                '1992-04-18',
                'YYYY-MM-DD'
            ) AS fecha_nacimiento
        FROM dual
    ) src
    ON (
        p.correo = src.correo
    )
    WHEN MATCHED THEN
        UPDATE SET
            p.nombre = src.nombre,
            p.apellido = src.apellido,
            p.telefono = src.telefono,
            p.direccion = src.direccion,
            p.fecha_nacimiento =
                src.fecha_nacimiento
    WHEN NOT MATCHED THEN
        INSERT (
            usuario_id,
            nombre,
            apellido,
            telefono,
            correo,
            direccion,
            fecha_nacimiento
        )
        VALUES (
            NULL,
            src.nombre,
            src.apellido,
            src.telefono,
            src.correo,
            src.direccion,
            src.fecha_nacimiento
        );


    MERGE INTO pacientes p
    USING (
        SELECT
            'Carlos' AS nombre,
            'Jiménez' AS apellido,
            '8888-2222' AS telefono,
            'carlos.jimenez@smilecare.demo'
                AS correo,
            'San José, Costa Rica' AS direccion,
            TO_DATE(
                '1987-09-23',
                'YYYY-MM-DD'
            ) AS fecha_nacimiento
        FROM dual
    ) src
    ON (
        p.correo = src.correo
    )
    WHEN MATCHED THEN
        UPDATE SET
            p.nombre = src.nombre,
            p.apellido = src.apellido,
            p.telefono = src.telefono,
            p.direccion = src.direccion,
            p.fecha_nacimiento =
                src.fecha_nacimiento
    WHEN NOT MATCHED THEN
        INSERT (
            usuario_id,
            nombre,
            apellido,
            telefono,
            correo,
            direccion,
            fecha_nacimiento
        )
        VALUES (
            NULL,
            src.nombre,
            src.apellido,
            src.telefono,
            src.correo,
            src.direccion,
            src.fecha_nacimiento
        );


    MERGE INTO pacientes p
    USING (
        SELECT
            'Ana' AS nombre,
            'Mora' AS apellido,
            '8888-3333' AS telefono,
            'ana.mora@smilecare.demo'
                AS correo,
            'Alajuela, Costa Rica' AS direccion,
            TO_DATE(
                '2001-11-05',
                'YYYY-MM-DD'
            ) AS fecha_nacimiento
        FROM dual
    ) src
    ON (
        p.correo = src.correo
    )
    WHEN MATCHED THEN
        UPDATE SET
            p.nombre = src.nombre,
            p.apellido = src.apellido,
            p.telefono = src.telefono,
            p.direccion = src.direccion,
            p.fecha_nacimiento =
                src.fecha_nacimiento
    WHEN NOT MATCHED THEN
        INSERT (
            usuario_id,
            nombre,
            apellido,
            telefono,
            correo,
            direccion,
            fecha_nacimiento
        )
        VALUES (
            NULL,
            src.nombre,
            src.apellido,
            src.telefono,
            src.correo,
            src.direccion,
            src.fecha_nacimiento
        );


    SELECT paciente_id
    INTO v_paciente_1_id
    FROM pacientes
    WHERE correo =
        'maria.rodriguez@smilecare.demo';


    SELECT paciente_id
    INTO v_paciente_2_id
    FROM pacientes
    WHERE correo =
        'carlos.jimenez@smilecare.demo';


    SELECT paciente_id
    INTO v_paciente_3_id
    FROM pacientes
    WHERE correo =
        'ana.mora@smilecare.demo';


    -- ========================================================
    -- 4. DOCTORES
    -- ========================================================


    MERGE INTO doctores d
    USING (
        SELECT
            v_usuario_doctor_id AS usuario_id,
            v_especialidad_general_id
                AS especialidad_id,
            'Laura' AS nombre,
            'Méndez' AS apellido,
            '2222-1111' AS telefono,
            'laura.mendez@smilecare.demo'
                AS correo
        FROM dual
    ) src
    ON (
        d.correo = src.correo
    )
    WHEN MATCHED THEN
        UPDATE SET
            d.usuario_id = src.usuario_id,
            d.especialidad_id =
                src.especialidad_id,
            d.nombre = src.nombre,
            d.apellido = src.apellido,
            d.telefono = src.telefono
    WHEN NOT MATCHED THEN
        INSERT (
            usuario_id,
            especialidad_id,
            nombre,
            apellido,
            telefono,
            correo
        )
        VALUES (
            src.usuario_id,
            src.especialidad_id,
            src.nombre,
            src.apellido,
            src.telefono,
            src.correo
        );


    MERGE INTO doctores d
    USING (
        SELECT
            CAST(NULL AS NUMBER) AS usuario_id,
            v_especialidad_cirugia_id
                AS especialidad_id,
            'Andrés' AS nombre,
            'Soto' AS apellido,
            '2222-2222' AS telefono,
            'andres.soto@smilecare.demo'
                AS correo
        FROM dual
    ) src
    ON (
        d.correo = src.correo
    )
    WHEN MATCHED THEN
        UPDATE SET
            d.especialidad_id =
                src.especialidad_id,
            d.nombre = src.nombre,
            d.apellido = src.apellido,
            d.telefono = src.telefono
    WHEN NOT MATCHED THEN
        INSERT (
            usuario_id,
            especialidad_id,
            nombre,
            apellido,
            telefono,
            correo
        )
        VALUES (
            src.usuario_id,
            src.especialidad_id,
            src.nombre,
            src.apellido,
            src.telefono,
            src.correo
        );


    SELECT doctor_id
    INTO v_doctor_1_id
    FROM doctores
    WHERE correo =
        'laura.mendez@smilecare.demo';


    SELECT doctor_id
    INTO v_doctor_2_id
    FROM doctores
    WHERE correo =
        'andres.soto@smilecare.demo';


    -- ========================================================
    -- 5. HORARIOS DE DOCTORES
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM horarios_doctores
    WHERE doctor_id = v_doctor_1_id
      AND dia_semana = 'LUNES'
      AND hora_inicio = '08:00'
      AND hora_fin = '17:00';

    IF v_count = 0 THEN
        INSERT INTO horarios_doctores (
            doctor_id,
            dia_semana,
            hora_inicio,
            hora_fin,
            estado
        )
        VALUES (
            v_doctor_1_id,
            'LUNES',
            '08:00',
            '17:00',
            'ACTIVO'
        );
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM horarios_doctores
    WHERE doctor_id = v_doctor_1_id
      AND dia_semana = 'MIERCOLES'
      AND hora_inicio = '08:00'
      AND hora_fin = '17:00';

    IF v_count = 0 THEN
        INSERT INTO horarios_doctores (
            doctor_id,
            dia_semana,
            hora_inicio,
            hora_fin,
            estado
        )
        VALUES (
            v_doctor_1_id,
            'MIERCOLES',
            '08:00',
            '17:00',
            'ACTIVO'
        );
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM horarios_doctores
    WHERE doctor_id = v_doctor_2_id
      AND dia_semana = 'MARTES'
      AND hora_inicio = '09:00'
      AND hora_fin = '18:00';

    IF v_count = 0 THEN
        INSERT INTO horarios_doctores (
            doctor_id,
            dia_semana,
            hora_inicio,
            hora_fin,
            estado
        )
        VALUES (
            v_doctor_2_id,
            'MARTES',
            '09:00',
            '18:00',
            'ACTIVO'
        );
    END IF;


    -- ========================================================
    -- 6. DISPONIBILIDAD ESPECIFICA
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM disponibilidad_doctores
    WHERE doctor_id = v_doctor_1_id
      AND fecha = TRUNC(SYSDATE) + 1
      AND hora_inicio = '09:00'
      AND hora_fin = '12:00';

    IF v_count = 0 THEN
        INSERT INTO disponibilidad_doctores (
            doctor_id,
            fecha,
            hora_inicio,
            hora_fin,
            estado
        )
        VALUES (
            v_doctor_1_id,
            TRUNC(SYSDATE) + 1,
            '09:00',
            '12:00',
            'DISPONIBLE'
        );
    END IF;


    -- ========================================================
    -- 7. TRATAMIENTOS
    -- ========================================================


    MERGE INTO tratamientos t
    USING (
        SELECT
            'Limpieza Dental' AS nombre,
            'Limpieza preventiva y eliminación de placa.'
                AS descripcion,
            25000 AS costo_base,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        UPPER(t.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            t.descripcion = src.descripcion,
            t.costo_base = src.costo_base,
            t.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion,
            costo_base,
            estado
        )
        VALUES (
            src.nombre,
            src.descripcion,
            src.costo_base,
            src.estado
        );


    MERGE INTO tratamientos t
    USING (
        SELECT
            'Extracción Dental' AS nombre,
            'Extracción quirúrgica de pieza dental.'
                AS descripcion,
            45000 AS costo_base,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        UPPER(t.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            t.descripcion = src.descripcion,
            t.costo_base = src.costo_base,
            t.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion,
            costo_base,
            estado
        )
        VALUES (
            src.nombre,
            src.descripcion,
            src.costo_base,
            src.estado
        );


    MERGE INTO tratamientos t
    USING (
        SELECT
            'Resina Dental' AS nombre,
            'Restauración estética de pieza dental.'
                AS descripcion,
            35000 AS costo_base,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        UPPER(t.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            t.descripcion = src.descripcion,
            t.costo_base = src.costo_base,
            t.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion,
            costo_base,
            estado
        )
        VALUES (
            src.nombre,
            src.descripcion,
            src.costo_base,
            src.estado
        );


    MERGE INTO tratamientos t
    USING (
        SELECT
            'Endodoncia' AS nombre,
            'Tratamiento del conducto radicular.'
                AS descripcion,
            85000 AS costo_base,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        UPPER(t.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            t.descripcion = src.descripcion,
            t.costo_base = src.costo_base,
            t.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion,
            costo_base,
            estado
        )
        VALUES (
            src.nombre,
            src.descripcion,
            src.costo_base,
            src.estado
        );


    SELECT tratamiento_id
    INTO v_trat_limpieza_id
    FROM tratamientos
    WHERE nombre = 'Limpieza Dental';


    SELECT tratamiento_id
    INTO v_trat_extraccion_id
    FROM tratamientos
    WHERE nombre = 'Extracción Dental';


    SELECT tratamiento_id
    INTO v_trat_resina_id
    FROM tratamientos
    WHERE nombre = 'Resina Dental';


    SELECT tratamiento_id
    INTO v_trat_endodoncia_id
    FROM tratamientos
    WHERE nombre = 'Endodoncia';


    -- ========================================================
    -- 8. HISTORIAL MEDICO
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM historial_medico
    WHERE paciente_id = v_paciente_1_id
      AND observaciones =
          'Registro clínico inicial de demostración.';

    IF v_count = 0 THEN
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
            v_paciente_1_id,
            v_doctor_1_id,
            'Penicilina',
            'Ninguna enfermedad crónica reportada',
            'Ninguno',
            'Extracción de cordales en 2018',
            'Registro clínico inicial de demostración.',
            SYSDATE - 30
        );
    END IF;


    -- ========================================================
    -- 9. CITA PASADA PARA ATENCION CLINICA
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM citas
    WHERE paciente_id = v_paciente_1_id
      AND motivo =
          'Control y limpieza de demostración';

    IF v_count = 0 THEN
        INSERT INTO citas (
            paciente_id,
            doctor_id,
            fecha_hora_inicio,
            duracion_minutos,
            estado,
            motivo
        )
        VALUES (
            v_paciente_1_id,
            v_doctor_1_id,
            TO_TIMESTAMP(
                TO_CHAR(
                    TRUNC(SYSDATE) - 7,
                    'YYYY-MM-DD'
                )
                || ' 10:00:00',
                'YYYY-MM-DD HH24:MI:SS'
            ),
            60,
            'COMPLETADA',
            'Control y limpieza de demostración'
        )
        RETURNING cita_id
        INTO v_cita_pasada_id;
    ELSE
        SELECT MAX(cita_id)
        INTO v_cita_pasada_id
        FROM citas
        WHERE paciente_id =
            v_paciente_1_id
          AND motivo =
            'Control y limpieza de demostración';
    END IF;


    -- ========================================================
    -- 10. CITAS FUTURAS
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM citas
    WHERE paciente_id = v_paciente_1_id
      AND motivo =
          'Revisión de seguimiento';

    IF v_count = 0 THEN
        INSERT INTO citas (
            paciente_id,
            doctor_id,
            fecha_hora_inicio,
            duracion_minutos,
            estado,
            motivo
        )
        VALUES (
            v_paciente_1_id,
            v_doctor_1_id,
            TO_TIMESTAMP(
                TO_CHAR(
                    TRUNC(SYSDATE) + 1,
                    'YYYY-MM-DD'
                )
                || ' 09:00:00',
                'YYYY-MM-DD HH24:MI:SS'
            ),
            30,
            'PROGRAMADA',
            'Revisión de seguimiento'
        )
        RETURNING cita_id
        INTO v_cita_futura_1_id;
    ELSE
        SELECT MAX(cita_id)
        INTO v_cita_futura_1_id
        FROM citas
        WHERE paciente_id =
            v_paciente_1_id
          AND motivo =
            'Revisión de seguimiento';
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM citas
    WHERE paciente_id = v_paciente_2_id
      AND motivo =
          'Evaluación para cirugía oral';

    IF v_count = 0 THEN
        INSERT INTO citas (
            paciente_id,
            doctor_id,
            fecha_hora_inicio,
            duracion_minutos,
            estado,
            motivo
        )
        VALUES (
            v_paciente_2_id,
            v_doctor_2_id,
            TO_TIMESTAMP(
                TO_CHAR(
                    TRUNC(SYSDATE) + 2,
                    'YYYY-MM-DD'
                )
                || ' 14:30:00',
                'YYYY-MM-DD HH24:MI:SS'
            ),
            60,
            'PROGRAMADA',
            'Evaluación para cirugía oral'
        )
        RETURNING cita_id
        INTO v_cita_futura_2_id;
    ELSE
        SELECT MAX(cita_id)
        INTO v_cita_futura_2_id
        FROM citas
        WHERE paciente_id =
            v_paciente_2_id
          AND motivo =
            'Evaluación para cirugía oral';
    END IF;


    -- ========================================================
    -- 11. CONSULTA
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM consultas
    WHERE cita_id = v_cita_pasada_id;

    IF v_count = 0 THEN
        INSERT INTO consultas (
            cita_id,
            diagnostico,
            observaciones,
            fecha_atencion
        )
        VALUES (
            v_cita_pasada_id,
            'Acumulación de placa y pieza dental con indicación de extracción.',
            'Paciente estable. Se brindaron recomendaciones de higiene oral.',
            TO_TIMESTAMP(
                TO_CHAR(
                    TRUNC(SYSDATE) - 7,
                    'YYYY-MM-DD'
                )
                || ' 11:00:00',
                'YYYY-MM-DD HH24:MI:SS'
            )
        )
        RETURNING consulta_id
        INTO v_consulta_id;
    ELSE
        SELECT consulta_id
        INTO v_consulta_id
        FROM consultas
        WHERE cita_id = v_cita_pasada_id;
    END IF;


    -- ========================================================
    -- 12. TRATAMIENTOS APLICADOS
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM tratamientos_consulta
    WHERE consulta_id = v_consulta_id
      AND tratamiento_id =
          v_trat_limpieza_id;

    IF v_count = 0 THEN
        INSERT INTO tratamientos_consulta (
            consulta_id,
            tratamiento_id,
            cantidad,
            precio_unitario,
            subtotal
        )
        VALUES (
            v_consulta_id,
            v_trat_limpieza_id,
            1,
            25000,
            25000
        )
        RETURNING tratamiento_consulta_id
        INTO v_tc_limpieza_id;
    ELSE
        SELECT MAX(tratamiento_consulta_id)
        INTO v_tc_limpieza_id
        FROM tratamientos_consulta
        WHERE consulta_id =
            v_consulta_id
          AND tratamiento_id =
            v_trat_limpieza_id;
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM tratamientos_consulta
    WHERE consulta_id = v_consulta_id
      AND tratamiento_id =
          v_trat_extraccion_id;

    IF v_count = 0 THEN
        INSERT INTO tratamientos_consulta (
            consulta_id,
            tratamiento_id,
            cantidad,
            precio_unitario,
            subtotal
        )
        VALUES (
            v_consulta_id,
            v_trat_extraccion_id,
            1,
            45000,
            45000
        )
        RETURNING tratamiento_consulta_id
        INTO v_tc_extraccion_id;
    ELSE
        SELECT MAX(tratamiento_consulta_id)
        INTO v_tc_extraccion_id
        FROM tratamientos_consulta
        WHERE consulta_id =
            v_consulta_id
          AND tratamiento_id =
            v_trat_extraccion_id;
    END IF;


    -- ========================================================
    -- 13. CIRUGIA
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM cirugias
    WHERE tratamiento_consulta_id =
        v_tc_extraccion_id;

    IF v_count = 0 THEN
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
            v_tc_extraccion_id,
            v_doctor_2_id,
            TO_TIMESTAMP(
                TO_CHAR(
                    TRUNC(SYSDATE) - 7,
                    'YYYY-MM-DD'
                )
                || ' 11:30:00',
                'YYYY-MM-DD HH24:MI:SS'
            ),
            'Extracción simple de pieza dental sin complicaciones.',
            'Anestesia local',
            'Paciente toleró correctamente el procedimiento.',
            'COMPLETADA'
        );
    END IF;


    -- ========================================================
    -- 14. METODOS DE PAGO
    -- ========================================================


    MERGE INTO metodos_pago m
    USING (
        SELECT
            'Efectivo' AS nombre,
            'Pago realizado en efectivo.'
                AS descripcion,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        UPPER(m.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            m.descripcion = src.descripcion,
            m.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion,
            estado
        )
        VALUES (
            src.nombre,
            src.descripcion,
            src.estado
        );


    MERGE INTO metodos_pago m
    USING (
        SELECT
            'Tarjeta' AS nombre,
            'Pago con tarjeta de débito o crédito.'
                AS descripcion,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        UPPER(m.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            m.descripcion = src.descripcion,
            m.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion,
            estado
        )
        VALUES (
            src.nombre,
            src.descripcion,
            src.estado
        );


    MERGE INTO metodos_pago m
    USING (
        SELECT
            'SINPE Móvil' AS nombre,
            'Pago mediante transferencia SINPE.'
                AS descripcion,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        UPPER(m.nombre)
        =
        UPPER(src.nombre)
    )
    WHEN MATCHED THEN
        UPDATE SET
            m.descripcion = src.descripcion,
            m.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            descripcion,
            estado
        )
        VALUES (
            src.nombre,
            src.descripcion,
            src.estado
        );


    SELECT metodo_pago_id
    INTO v_metodo_efectivo_id
    FROM metodos_pago
    WHERE nombre = 'Efectivo';


    SELECT metodo_pago_id
    INTO v_metodo_tarjeta_id
    FROM metodos_pago
    WHERE nombre = 'Tarjeta';


    SELECT metodo_pago_id
    INTO v_metodo_sinpe_id
    FROM metodos_pago
    WHERE nombre = 'SINPE Móvil';


    -- ========================================================
    -- 15. FACTURA
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM facturas
    WHERE numero_factura =
        'FAC-DEMO-0001';

    IF v_count = 0 THEN
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
            v_paciente_1_id,
            v_consulta_id,
            'FAC-DEMO-0001',
            SYSDATE - 7,
            70000,
            9100,
            79100,
            'PAGADA'
        )
        RETURNING factura_id
        INTO v_factura_id;
    ELSE
        SELECT factura_id
        INTO v_factura_id
        FROM facturas
        WHERE numero_factura =
            'FAC-DEMO-0001';
    END IF;


    -- ========================================================
    -- 16. DETALLES DE FACTURA
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM detalle_factura
    WHERE factura_id = v_factura_id
      AND descripcion =
          'Limpieza Dental';

    IF v_count = 0 THEN
        INSERT INTO detalle_factura (
            factura_id,
            tratamiento_consulta_id,
            descripcion,
            cantidad,
            precio_unitario,
            subtotal
        )
        VALUES (
            v_factura_id,
            v_tc_limpieza_id,
            'Limpieza Dental',
            1,
            25000,
            25000
        );
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM detalle_factura
    WHERE factura_id = v_factura_id
      AND descripcion =
          'Extracción Dental';

    IF v_count = 0 THEN
        INSERT INTO detalle_factura (
            factura_id,
            tratamiento_consulta_id,
            descripcion,
            cantidad,
            precio_unitario,
            subtotal
        )
        VALUES (
            v_factura_id,
            v_tc_extraccion_id,
            'Extracción Dental',
            1,
            45000,
            45000
        );
    END IF;


    -- ========================================================
    -- 17. PAGO
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM pagos
    WHERE numero_referencia =
        'DEMO-PAGO-001';

    IF v_count = 0 THEN
        INSERT INTO pagos (
            factura_id,
            metodo_pago_id,
            monto,
            fecha_pago,
            numero_referencia,
            estado
        )
        VALUES (
            v_factura_id,
            v_metodo_tarjeta_id,
            79100,
            SYSDATE - 7,
            'DEMO-PAGO-001',
            'APLICADO'
        )
        RETURNING pago_id
        INTO v_pago_id;
    ELSE
        SELECT pago_id
        INTO v_pago_id
        FROM pagos
        WHERE numero_referencia =
            'DEMO-PAGO-001';
    END IF;


    -- ========================================================
    -- 18. COMPROBANTE
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM comprobantes
    WHERE numero_comprobante =
        'COMP-DEMO-0001';

    IF v_count = 0 THEN
        INSERT INTO comprobantes (
            pago_id,
            numero_comprobante,
            tipo_comprobante,
            fecha_emision,
            detalle
        )
        VALUES (
            v_pago_id,
            'COMP-DEMO-0001',
            'RECIBO',
            SYSDATE - 7,
            'Pago completo de factura de demostración.'
        );
    END IF;


    -- ========================================================
    -- 19. PROVEEDORES
    -- ========================================================


    MERGE INTO proveedores p
    USING (
        SELECT
            'Dental Supply CR' AS nombre,
            '2200-1000' AS telefono,
            'ventas@dentalsupply.demo'
                AS correo,
            'San José, Costa Rica'
                AS direccion,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        p.correo = src.correo
    )
    WHEN MATCHED THEN
        UPDATE SET
            p.nombre = src.nombre,
            p.telefono = src.telefono,
            p.direccion = src.direccion,
            p.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            telefono,
            correo,
            direccion,
            estado
        )
        VALUES (
            src.nombre,
            src.telefono,
            src.correo,
            src.direccion,
            src.estado
        );


    MERGE INTO proveedores p
    USING (
        SELECT
            'Odonto Materiales' AS nombre,
            '2200-2000' AS telefono,
            'pedidos@odontomateriales.demo'
                AS correo,
            'Heredia, Costa Rica'
                AS direccion,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        p.correo = src.correo
    )
    WHEN MATCHED THEN
        UPDATE SET
            p.nombre = src.nombre,
            p.telefono = src.telefono,
            p.direccion = src.direccion,
            p.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            nombre,
            telefono,
            correo,
            direccion,
            estado
        )
        VALUES (
            src.nombre,
            src.telefono,
            src.correo,
            src.direccion,
            src.estado
        );


    SELECT proveedor_id
    INTO v_proveedor_1_id
    FROM proveedores
    WHERE correo =
        'ventas@dentalsupply.demo';


    SELECT proveedor_id
    INTO v_proveedor_2_id
    FROM proveedores
    WHERE correo =
        'pedidos@odontomateriales.demo';


    -- ========================================================
    -- 20. INSUMOS
    -- ========================================================


    MERGE INTO insumos i
    USING (
        SELECT
            'INS-001' AS codigo,
            'Guantes de Nitrilo' AS nombre,
            'Caja de guantes para uso clínico.'
                AS descripcion,
            'CAJA' AS unidad_medida,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        i.codigo = src.codigo
    )
    WHEN MATCHED THEN
        UPDATE SET
            i.nombre = src.nombre,
            i.descripcion = src.descripcion,
            i.unidad_medida =
                src.unidad_medida,
            i.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            codigo,
            nombre,
            descripcion,
            unidad_medida,
            estado
        )
        VALUES (
            src.codigo,
            src.nombre,
            src.descripcion,
            src.unidad_medida,
            src.estado
        );


    MERGE INTO insumos i
    USING (
        SELECT
            'INS-002' AS codigo,
            'Anestesia Local' AS nombre,
            'Cartuchos de anestesia local.'
                AS descripcion,
            'UNIDAD' AS unidad_medida,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        i.codigo = src.codigo
    )
    WHEN MATCHED THEN
        UPDATE SET
            i.nombre = src.nombre,
            i.descripcion = src.descripcion,
            i.unidad_medida =
                src.unidad_medida,
            i.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            codigo,
            nombre,
            descripcion,
            unidad_medida,
            estado
        )
        VALUES (
            src.codigo,
            src.nombre,
            src.descripcion,
            src.unidad_medida,
            src.estado
        );


    MERGE INTO insumos i
    USING (
        SELECT
            'INS-003' AS codigo,
            'Resina Compuesta' AS nombre,
            'Material restaurativo fotopolimerizable.'
                AS descripcion,
            'UNIDAD' AS unidad_medida,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        i.codigo = src.codigo
    )
    WHEN MATCHED THEN
        UPDATE SET
            i.nombre = src.nombre,
            i.descripcion = src.descripcion,
            i.unidad_medida =
                src.unidad_medida,
            i.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            codigo,
            nombre,
            descripcion,
            unidad_medida,
            estado
        )
        VALUES (
            src.codigo,
            src.nombre,
            src.descripcion,
            src.unidad_medida,
            src.estado
        );


    MERGE INTO insumos i
    USING (
        SELECT
            'INS-004' AS codigo,
            'Sutura Quirúrgica' AS nombre,
            'Sutura para procedimientos orales.'
                AS descripcion,
            'UNIDAD' AS unidad_medida,
            'ACTIVO' AS estado
        FROM dual
    ) src
    ON (
        i.codigo = src.codigo
    )
    WHEN MATCHED THEN
        UPDATE SET
            i.nombre = src.nombre,
            i.descripcion = src.descripcion,
            i.unidad_medida =
                src.unidad_medida,
            i.estado = src.estado
    WHEN NOT MATCHED THEN
        INSERT (
            codigo,
            nombre,
            descripcion,
            unidad_medida,
            estado
        )
        VALUES (
            src.codigo,
            src.nombre,
            src.descripcion,
            src.unidad_medida,
            src.estado
        );


    SELECT insumo_id
    INTO v_insumo_guantes_id
    FROM insumos
    WHERE codigo = 'INS-001';


    SELECT insumo_id
    INTO v_insumo_anestesia_id
    FROM insumos
    WHERE codigo = 'INS-002';


    SELECT insumo_id
    INTO v_insumo_resina_id
    FROM insumos
    WHERE codigo = 'INS-003';


    SELECT insumo_id
    INTO v_insumo_sutura_id
    FROM insumos
    WHERE codigo = 'INS-004';


    -- ========================================================
    -- 21. STOCK
    -- ========================================================


    MERGE INTO inventario_stock s
    USING (
        SELECT
            v_insumo_guantes_id AS insumo_id,
            70 AS stock_actual,
            20 AS stock_minimo,
            'Bodega principal' AS ubicacion
        FROM dual
    ) src
    ON (
        s.insumo_id = src.insumo_id
    )
    WHEN MATCHED THEN
        UPDATE SET
            s.stock_actual =
                src.stock_actual,
            s.stock_minimo =
                src.stock_minimo,
            s.ubicacion =
                src.ubicacion
    WHEN NOT MATCHED THEN
        INSERT (
            insumo_id,
            stock_actual,
            stock_minimo,
            ubicacion
        )
        VALUES (
            src.insumo_id,
            src.stock_actual,
            src.stock_minimo,
            src.ubicacion
        );


    MERGE INTO inventario_stock s
    USING (
        SELECT
            v_insumo_anestesia_id AS insumo_id,
            25 AS stock_actual,
            10 AS stock_minimo,
            'Gabinete clínico' AS ubicacion
        FROM dual
    ) src
    ON (
        s.insumo_id = src.insumo_id
    )
    WHEN MATCHED THEN
        UPDATE SET
            s.stock_actual =
                src.stock_actual,
            s.stock_minimo =
                src.stock_minimo,
            s.ubicacion =
                src.ubicacion
    WHEN NOT MATCHED THEN
        INSERT (
            insumo_id,
            stock_actual,
            stock_minimo,
            ubicacion
        )
        VALUES (
            src.insumo_id,
            src.stock_actual,
            src.stock_minimo,
            src.ubicacion
        );


    MERGE INTO inventario_stock s
    USING (
        SELECT
            v_insumo_resina_id AS insumo_id,
            15 AS stock_actual,
            5 AS stock_minimo,
            'Gabinete clínico' AS ubicacion
        FROM dual
    ) src
    ON (
        s.insumo_id = src.insumo_id
    )
    WHEN MATCHED THEN
        UPDATE SET
            s.stock_actual =
                src.stock_actual,
            s.stock_minimo =
                src.stock_minimo,
            s.ubicacion =
                src.ubicacion
    WHEN NOT MATCHED THEN
        INSERT (
            insumo_id,
            stock_actual,
            stock_minimo,
            ubicacion
        )
        VALUES (
            src.insumo_id,
            src.stock_actual,
            src.stock_minimo,
            src.ubicacion
        );


    MERGE INTO inventario_stock s
    USING (
        SELECT
            v_insumo_sutura_id AS insumo_id,
            3 AS stock_actual,
            5 AS stock_minimo,
            'Gabinete quirúrgico' AS ubicacion
        FROM dual
    ) src
    ON (
        s.insumo_id = src.insumo_id
    )
    WHEN MATCHED THEN
        UPDATE SET
            s.stock_actual =
                src.stock_actual,
            s.stock_minimo =
                src.stock_minimo,
            s.ubicacion =
                src.ubicacion
    WHEN NOT MATCHED THEN
        INSERT (
            insumo_id,
            stock_actual,
            stock_minimo,
            ubicacion
        )
        VALUES (
            src.insumo_id,
            src.stock_actual,
            src.stock_minimo,
            src.ubicacion
        );


    -- ========================================================
    -- 22. COMPRA DEMO
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM compras
    WHERE proveedor_id =
        v_proveedor_1_id
      AND usuario_id =
        v_usuario_inventario_id
      AND total = 45500
      AND estado = 'RECIBIDA';

    IF v_count = 0 THEN
        INSERT INTO compras (
            proveedor_id,
            usuario_id,
            fecha_compra,
            total,
            estado
        )
        VALUES (
            v_proveedor_1_id,
            v_usuario_inventario_id,
            SYSDATE - 2,
            45500,
            'RECIBIDA'
        )
        RETURNING compra_id
        INTO v_compra_id;
    ELSE
        SELECT MAX(compra_id)
        INTO v_compra_id
        FROM compras
        WHERE proveedor_id =
            v_proveedor_1_id
          AND usuario_id =
            v_usuario_inventario_id
          AND total = 45500
          AND estado = 'RECIBIDA';
    END IF;


    -- ========================================================
    -- 23. DETALLES DE COMPRA
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM detalle_compra
    WHERE compra_id = v_compra_id
      AND insumo_id =
          v_insumo_guantes_id;

    IF v_count = 0 THEN
        INSERT INTO detalle_compra (
            compra_id,
            insumo_id,
            cantidad,
            costo_unitario,
            subtotal
        )
        VALUES (
            v_compra_id,
            v_insumo_guantes_id,
            20,
            1500,
            30000
        )
        RETURNING detalle_compra_id
        INTO v_detalle_guantes_id;
    ELSE
        SELECT MAX(detalle_compra_id)
        INTO v_detalle_guantes_id
        FROM detalle_compra
        WHERE compra_id =
            v_compra_id
          AND insumo_id =
            v_insumo_guantes_id;
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM detalle_compra
    WHERE compra_id = v_compra_id
      AND insumo_id =
          v_insumo_anestesia_id;

    IF v_count = 0 THEN
        INSERT INTO detalle_compra (
            compra_id,
            insumo_id,
            cantidad,
            costo_unitario,
            subtotal
        )
        VALUES (
            v_compra_id,
            v_insumo_anestesia_id,
            5,
            3100,
            15500
        )
        RETURNING detalle_compra_id
        INTO v_detalle_anestesia_id;
    ELSE
        SELECT MAX(detalle_compra_id)
        INTO v_detalle_anestesia_id
        FROM detalle_compra
        WHERE compra_id =
            v_compra_id
          AND insumo_id =
            v_insumo_anestesia_id;
    END IF;


    -- ========================================================
    -- 24. MOVIMIENTOS AUTOMATICOS DE COMPRA
    -- ========================================================


    SELECT COUNT(*)
    INTO v_count
    FROM movimientos_inventario
    WHERE detalle_compra_id =
        v_detalle_guantes_id;

    IF v_count = 0 THEN
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
            v_insumo_guantes_id,
            v_usuario_inventario_id,
            v_detalle_guantes_id,
            NULL,
            'ENTRADA',
            20,
            SYSDATE - 2,
            'Entrada automática por compra DEMO'
        );
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM movimientos_inventario
    WHERE detalle_compra_id =
        v_detalle_anestesia_id;

    IF v_count = 0 THEN
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
            v_insumo_anestesia_id,
            v_usuario_inventario_id,
            v_detalle_anestesia_id,
            NULL,
            'ENTRADA',
            5,
            SYSDATE - 2,
            'Entrada automática por compra DEMO'
        );
    END IF;


    COMMIT;


    DBMS_OUTPUT.PUT_LINE(
        'Datos demo cargados correctamente.'
    );


EXCEPTION

    WHEN NO_DATA_FOUND THEN
        ROLLBACK;

        RAISE_APPLICATION_ERROR(
            -20010,
            'No se encontraron datos base requeridos. '
            || 'Ejecute primero '
            || '09_rbac_usuarios_demo.sql.'
        );


    WHEN OTHERS THEN
        ROLLBACK;

        RAISE;

END;
/


PROMPT ============================================================
PROMPT RESUMEN DE DATOS DEMO
PROMPT ============================================================


SELECT
    'PACIENTES' AS entidad,
    COUNT(*) AS cantidad
FROM pacientes

UNION ALL

SELECT
    'DOCTORES',
    COUNT(*)
FROM doctores

UNION ALL

SELECT
    'CITAS',
    COUNT(*)
FROM citas

UNION ALL

SELECT
    'CONSULTAS',
    COUNT(*)
FROM consultas

UNION ALL

SELECT
    'TRATAMIENTOS',
    COUNT(*)
FROM tratamientos

UNION ALL

SELECT
    'FACTURAS',
    COUNT(*)
FROM facturas

UNION ALL

SELECT
    'PAGOS',
    COUNT(*)
FROM pagos

UNION ALL

SELECT
    'PROVEEDORES',
    COUNT(*)
FROM proveedores

UNION ALL

SELECT
    'INSUMOS',
    COUNT(*)
FROM insumos

UNION ALL

SELECT
    'COMPRAS',
    COUNT(*)
FROM compras

UNION ALL

SELECT
    'MOVIMIENTOS_INVENTARIO',
    COUNT(*)
FROM movimientos_inventario;


PROMPT ============================================================
PROMPT FIN DE 10_datos_demo.sql
PROMPT ============================================================