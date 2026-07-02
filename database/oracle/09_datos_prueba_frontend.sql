SET SERVEROUTPUT ON;

PROMPT ============================================================
PROMPT DATOS DE PRUEBA PARA FRONTEND - SMILECARE
PROMPT ============================================================

DECLARE
    v_rol_admin_id NUMBER;
    v_rol_doctor_id NUMBER;
    v_usuario_admin_id NUMBER;
    v_usuario_doctor_1_id NUMBER;
    v_usuario_doctor_2_id NUMBER;
    v_especialidad_1_id NUMBER;
    v_especialidad_2_id NUMBER;
    v_paciente_1_id NUMBER;
    v_paciente_2_id NUMBER;
    v_paciente_3_id NUMBER;
    v_doctor_1_id NUMBER;
    v_doctor_2_id NUMBER;
    v_count NUMBER;
BEGIN
    /*
        ============================================================
        ROLES
        ============================================================
    */

    SELECT COUNT(*)
    INTO v_count
    FROM roles
    WHERE nombre_rol = 'ADMIN_TEST';

    IF v_count = 0 THEN
        INSERT INTO roles (
            nombre_rol,
            descripcion,
            estado
        )
        VALUES (
            'ADMIN_TEST',
            'Rol administrativo para pruebas del frontend.',
            'ACTIVO'
        )
        RETURNING rol_id INTO v_rol_admin_id;
    ELSE
        SELECT rol_id
        INTO v_rol_admin_id
        FROM roles
        WHERE nombre_rol = 'ADMIN_TEST';
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM roles
    WHERE nombre_rol = 'DOCTOR_TEST';

    IF v_count = 0 THEN
        INSERT INTO roles (
            nombre_rol,
            descripcion,
            estado
        )
        VALUES (
            'DOCTOR_TEST',
            'Rol de doctor para pruebas del frontend.',
            'ACTIVO'
        )
        RETURNING rol_id INTO v_rol_doctor_id;
    ELSE
        SELECT rol_id
        INTO v_rol_doctor_id
        FROM roles
        WHERE nombre_rol = 'DOCTOR_TEST';
    END IF;


    /*
        ============================================================
        USUARIOS
        ============================================================
    */

    SELECT COUNT(*)
    INTO v_count
    FROM usuarios
    WHERE nombre_usuario = 'admin_test';

    IF v_count = 0 THEN
        INSERT INTO usuarios (
            rol_id,
            nombre_usuario,
            password_hash,
            estado
        )
        VALUES (
            v_rol_admin_id,
            'admin_test',
            'hash_dummy_admin_123',
            'ACTIVO'
        )
        RETURNING usuario_id INTO v_usuario_admin_id;
    ELSE
        SELECT usuario_id
        INTO v_usuario_admin_id
        FROM usuarios
        WHERE nombre_usuario = 'admin_test';
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM usuarios
    WHERE nombre_usuario = 'doctor_test_1';

    IF v_count = 0 THEN
        INSERT INTO usuarios (
            rol_id,
            nombre_usuario,
            password_hash,
            estado
        )
        VALUES (
            v_rol_doctor_id,
            'doctor_test_1',
            'hash_dummy_doctor_1',
            'ACTIVO'
        )
        RETURNING usuario_id INTO v_usuario_doctor_1_id;
    ELSE
        SELECT usuario_id
        INTO v_usuario_doctor_1_id
        FROM usuarios
        WHERE nombre_usuario = 'doctor_test_1';
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM usuarios
    WHERE nombre_usuario = 'doctor_test_2';

    IF v_count = 0 THEN
        INSERT INTO usuarios (
            rol_id,
            nombre_usuario,
            password_hash,
            estado
        )
        VALUES (
            v_rol_doctor_id,
            'doctor_test_2',
            'hash_dummy_doctor_2',
            'ACTIVO'
        )
        RETURNING usuario_id INTO v_usuario_doctor_2_id;
    ELSE
        SELECT usuario_id
        INTO v_usuario_doctor_2_id
        FROM usuarios
        WHERE nombre_usuario = 'doctor_test_2';
    END IF;


    /*
        ============================================================
        ESPECIALIDADES
        ============================================================
    */

    SELECT COUNT(*)
    INTO v_count
    FROM especialidades
    WHERE nombre = 'Odontología General';

    IF v_count = 0 THEN
        INSERT INTO especialidades (
            nombre,
            descripcion
        )
        VALUES (
            'Odontología General',
            'Atención odontológica general y revisiones dentales.'
        )
        RETURNING especialidad_id INTO v_especialidad_1_id;
    ELSE
        SELECT especialidad_id
        INTO v_especialidad_1_id
        FROM especialidades
        WHERE nombre = 'Odontología General';
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM especialidades
    WHERE nombre = 'Ortodoncia';

    IF v_count = 0 THEN
        INSERT INTO especialidades (
            nombre,
            descripcion
        )
        VALUES (
            'Ortodoncia',
            'Tratamientos de alineación dental y brackets.'
        )
        RETURNING especialidad_id INTO v_especialidad_2_id;
    ELSE
        SELECT especialidad_id
        INTO v_especialidad_2_id
        FROM especialidades
        WHERE nombre = 'Ortodoncia';
    END IF;


    /*
        ============================================================
        PACIENTES
        ============================================================
    */

    SELECT COUNT(*)
    INTO v_count
    FROM pacientes
    WHERE correo = 'maria.prueba@smilecare.com';

    IF v_count = 0 THEN
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
            NULL,
            'María',
            'González',
            '8888-1111',
            'maria.prueba@smilecare.com',
            'Heredia, Costa Rica',
            TO_DATE('1995-03-15', 'YYYY-MM-DD')
        )
        RETURNING paciente_id INTO v_paciente_1_id;
    ELSE
        SELECT paciente_id
        INTO v_paciente_1_id
        FROM pacientes
        WHERE correo = 'maria.prueba@smilecare.com';
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM pacientes
    WHERE correo = 'carlos.prueba@smilecare.com';

    IF v_count = 0 THEN
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
            NULL,
            'Carlos',
            'Ramírez',
            '8888-2222',
            'carlos.prueba@smilecare.com',
            'San José, Costa Rica',
            TO_DATE('1988-07-22', 'YYYY-MM-DD')
        )
        RETURNING paciente_id INTO v_paciente_2_id;
    ELSE
        SELECT paciente_id
        INTO v_paciente_2_id
        FROM pacientes
        WHERE correo = 'carlos.prueba@smilecare.com';
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM pacientes
    WHERE correo = 'ana.prueba@smilecare.com';

    IF v_count = 0 THEN
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
            NULL,
            'Ana',
            'Mora',
            '8888-3333',
            'ana.prueba@smilecare.com',
            'Alajuela, Costa Rica',
            TO_DATE('2001-11-05', 'YYYY-MM-DD')
        )
        RETURNING paciente_id INTO v_paciente_3_id;
    ELSE
        SELECT paciente_id
        INTO v_paciente_3_id
        FROM pacientes
        WHERE correo = 'ana.prueba@smilecare.com';
    END IF;


    /*
        ============================================================
        DOCTORES
        ============================================================
    */

    SELECT COUNT(*)
    INTO v_count
    FROM doctores
    WHERE correo = 'laura.mendez@smilecare.com';

    IF v_count = 0 THEN
        INSERT INTO doctores (
            usuario_id,
            especialidad_id,
            nombre,
            apellido,
            telefono,
            correo
        )
        VALUES (
            v_usuario_doctor_1_id,
            v_especialidad_1_id,
            'Laura',
            'Méndez',
            '2222-1111',
            'laura.mendez@smilecare.com'
        )
        RETURNING doctor_id INTO v_doctor_1_id;
    ELSE
        SELECT doctor_id
        INTO v_doctor_1_id
        FROM doctores
        WHERE correo = 'laura.mendez@smilecare.com';
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM doctores
    WHERE correo = 'andres.soto@smilecare.com';

    IF v_count = 0 THEN
        INSERT INTO doctores (
            usuario_id,
            especialidad_id,
            nombre,
            apellido,
            telefono,
            correo
        )
        VALUES (
            v_usuario_doctor_2_id,
            v_especialidad_2_id,
            'Andrés',
            'Soto',
            '2222-2222',
            'andres.soto@smilecare.com'
        )
        RETURNING doctor_id INTO v_doctor_2_id;
    ELSE
        SELECT doctor_id
        INTO v_doctor_2_id
        FROM doctores
        WHERE correo = 'andres.soto@smilecare.com';
    END IF;


    /*
        ============================================================
        CITAS
        ============================================================
    */

    SELECT COUNT(*)
    INTO v_count
    FROM citas
    WHERE paciente_id = v_paciente_1_id
      AND doctor_id = v_doctor_1_id
      AND fecha_hora_inicio = TO_TIMESTAMP(
            TO_CHAR(SYSDATE + 1, 'YYYY-MM-DD') || ' 09:00:00',
            'YYYY-MM-DD HH24:MI:SS'
          );

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
                TO_CHAR(SYSDATE + 1, 'YYYY-MM-DD') || ' 09:00:00',
                'YYYY-MM-DD HH24:MI:SS'
            ),
            30,
            'PROGRAMADA',
            'Revisión general'
        );
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM citas
    WHERE paciente_id = v_paciente_2_id
      AND doctor_id = v_doctor_2_id
      AND fecha_hora_inicio = TO_TIMESTAMP(
            TO_CHAR(SYSDATE + 2, 'YYYY-MM-DD') || ' 10:30:00',
            'YYYY-MM-DD HH24:MI:SS'
          );

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
                TO_CHAR(SYSDATE + 2, 'YYYY-MM-DD') || ' 10:30:00',
                'YYYY-MM-DD HH24:MI:SS'
            ),
            45,
            'PROGRAMADA',
            'Consulta de ortodoncia'
        );
    END IF;


    SELECT COUNT(*)
    INTO v_count
    FROM citas
    WHERE paciente_id = v_paciente_3_id
      AND doctor_id = v_doctor_1_id
      AND fecha_hora_inicio = TO_TIMESTAMP(
            TO_CHAR(SYSDATE + 3, 'YYYY-MM-DD') || ' 14:00:00',
            'YYYY-MM-DD HH24:MI:SS'
          );

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
            v_paciente_3_id,
            v_doctor_1_id,
            TO_TIMESTAMP(
                TO_CHAR(SYSDATE + 3, 'YYYY-MM-DD') || ' 14:00:00',
                'YYYY-MM-DD HH24:MI:SS'
            ),
            30,
            'CONFIRMADA',
            'Dolor dental'
        );
    END IF;


    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Datos de prueba creados correctamente.');
    DBMS_OUTPUT.PUT_LINE('Paciente 1 ID: ' || v_paciente_1_id);
    DBMS_OUTPUT.PUT_LINE('Paciente 2 ID: ' || v_paciente_2_id);
    DBMS_OUTPUT.PUT_LINE('Paciente 3 ID: ' || v_paciente_3_id);
    DBMS_OUTPUT.PUT_LINE('Doctor 1 ID: ' || v_doctor_1_id);
    DBMS_OUTPUT.PUT_LINE('Doctor 2 ID: ' || v_doctor_2_id);

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;

        DBMS_OUTPUT.PUT_LINE('Error creando datos de prueba.');
        DBMS_OUTPUT.PUT_LINE(SQLERRM);

        RAISE;
END;
/