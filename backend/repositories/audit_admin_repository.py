from typing import Optional


def rows_to_dicts(
    cursor,
    rows
):
    columns = [
        column[0].lower()
        for column in cursor.description
    ]

    return [
        dict(
            zip(
                columns,
                row
            )
        )
        for row in rows
    ]


class AuditAdminRepository:

    def __init__(
        self,
        connection
    ):
        self.connection = connection


    # -----------------------------------------------------
    # INTERNAL COUNT HELPER
    # -----------------------------------------------------

    def _count_records(
        self,
        table_name: str,
        date_column: str,
        fecha_desde=None,
        fecha_hasta_exclusiva=None,
        extra_condition: Optional[str] = None
    ) -> int:
        conditions = []
        params = {}


        if fecha_desde is not None:
            conditions.append(
                f"{date_column} >= :fecha_desde"
            )

            params["fecha_desde"] = (
                fecha_desde
            )


        if fecha_hasta_exclusiva is not None:
            conditions.append(
                f"{date_column} < :fecha_hasta"
            )

            params["fecha_hasta"] = (
                fecha_hasta_exclusiva
            )


        if extra_condition:
            conditions.append(
                extra_condition
            )


        where_clause = ""

        if conditions:
            where_clause = (
                " WHERE "
                + " AND ".join(
                    conditions
                )
            )


        sql = f"""
        SELECT COUNT(*)
        FROM {table_name}
        {where_clause}
        """


        cursor = self.connection.cursor()

        try:
            cursor.execute(
                sql,
                params
            )

            row = cursor.fetchone()

            return int(
                row[0]
            )

        finally:
            cursor.close()


    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    def get_summary(
        self,
        fecha_desde=None,
        fecha_hasta_exclusiva=None
    ) -> dict:
        return {
            "login_exitosos":
                self._count_records(
                    table_name=(
                        "historial_accesos"
                    ),
                    date_column=(
                        "fecha_evento"
                    ),
                    fecha_desde=fecha_desde,
                    fecha_hasta_exclusiva=(
                        fecha_hasta_exclusiva
                    ),
                    extra_condition=(
                        "evento = "
                        "'LOGIN_SUCCESS'"
                    )
                ),

            "login_fallidos":
                self._count_records(
                    table_name=(
                        "historial_accesos"
                    ),
                    date_column=(
                        "fecha_evento"
                    ),
                    fecha_desde=fecha_desde,
                    fecha_hasta_exclusiva=(
                        fecha_hasta_exclusiva
                    ),
                    extra_condition=(
                        "evento = "
                        "'LOGIN_FAILED'"
                    )
                ),

            "logouts":
                self._count_records(
                    table_name=(
                        "historial_accesos"
                    ),
                    date_column=(
                        "fecha_evento"
                    ),
                    fecha_desde=fecha_desde,
                    fecha_hasta_exclusiva=(
                        fecha_hasta_exclusiva
                    ),
                    extra_condition=(
                        "evento = 'LOGOUT'"
                    )
                ),

            "cambios_exitosos":
                self._count_records(
                    table_name=(
                        "auditoria_sistema"
                    ),
                    date_column=(
                        "fecha_accion"
                    ),
                    fecha_desde=fecha_desde,
                    fecha_hasta_exclusiva=(
                        fecha_hasta_exclusiva
                    ),
                    extra_condition=(
                        "resultado = 'EXITOSO' "
                        "AND metodo_http IN "
                        "('POST', 'PUT', "
                        "'PATCH', 'DELETE')"
                    )
                ),

            "accesos_denegados":
                self._count_records(
                    table_name=(
                        "auditoria_sistema"
                    ),
                    date_column=(
                        "fecha_accion"
                    ),
                    fecha_desde=fecha_desde,
                    fecha_hasta_exclusiva=(
                        fecha_hasta_exclusiva
                    ),
                    extra_condition=(
                        "resultado = 'DENEGADO'"
                    )
                ),

            "eventos_triggers":
                self._count_records(
                    table_name=(
                        "auditoria_acciones"
                    ),
                    date_column=(
                        "fecha_accion"
                    ),
                    fecha_desde=fecha_desde,
                    fecha_hasta_exclusiva=(
                        fecha_hasta_exclusiva
                    )
                )
        }


    # -----------------------------------------------------
    # APPLICATION AUDIT
    # -----------------------------------------------------

    def get_system_audit(
        self,
        fecha_desde=None,
        fecha_hasta_exclusiva=None,
        usuario=None,
        modulo=None,
        accion=None,
        resultado=None,
        limite: int = 500
    ):
        conditions = []
        params = {
            "limite": limite
        }


        if fecha_desde is not None:
            conditions.append(
                "fecha_accion >= :fecha_desde"
            )

            params["fecha_desde"] = (
                fecha_desde
            )


        if fecha_hasta_exclusiva is not None:
            conditions.append(
                "fecha_accion < :fecha_hasta"
            )

            params["fecha_hasta"] = (
                fecha_hasta_exclusiva
            )


        if usuario:
            conditions.append(
                """
                UPPER(nombre_usuario)
                = UPPER(:usuario)
                """
            )

            params["usuario"] = usuario


        if modulo:
            conditions.append(
                """
                UPPER(modulo)
                = UPPER(:modulo)
                """
            )

            params["modulo"] = modulo


        if accion:
            conditions.append(
                """
                UPPER(accion)
                = UPPER(:accion)
                """
            )

            params["accion"] = accion


        if resultado:
            conditions.append(
                """
                UPPER(resultado)
                = UPPER(:resultado)
                """
            )

            params["resultado"] = resultado


        where_clause = ""

        if conditions:
            where_clause = (
                "WHERE "
                + " AND ".join(
                    conditions
                )
            )


        sql = f"""
        SELECT *
        FROM (
            SELECT
                auditoria_sistema_id,
                usuario_id,
                nombre_usuario,
                nombre_rol,
                modulo,
                entidad,
                accion,
                metodo_http,
                ruta,
                valor_llave,
                resultado,
                status_code,
                detalle,
                ip_origen,
                request_id,
                fecha_accion
            FROM auditoria_sistema
            {where_clause}
            ORDER BY
                fecha_accion DESC,
                auditoria_sistema_id DESC
        )
        WHERE ROWNUM <= :limite
        """


        cursor = self.connection.cursor()

        try:
            cursor.execute(
                sql,
                params
            )

            rows = cursor.fetchall()

            return rows_to_dicts(
                cursor,
                rows
            )

        finally:
            cursor.close()


    # -----------------------------------------------------
    # ACCESS HISTORY
    # -----------------------------------------------------

    def get_access_history(
        self,
        fecha_desde=None,
        fecha_hasta_exclusiva=None,
        usuario=None,
        accion=None,
        resultado=None,
        limite: int = 500
    ):
        conditions = []
        params = {
            "limite": limite
        }


        if fecha_desde is not None:
            conditions.append(
                "fecha_evento >= :fecha_desde"
            )

            params["fecha_desde"] = (
                fecha_desde
            )


        if fecha_hasta_exclusiva is not None:
            conditions.append(
                "fecha_evento < :fecha_hasta"
            )

            params["fecha_hasta"] = (
                fecha_hasta_exclusiva
            )


        if usuario:
            conditions.append(
                """
                UPPER(nombre_usuario)
                = UPPER(:usuario)
                """
            )

            params["usuario"] = usuario


        if accion:
            conditions.append(
                """
                UPPER(evento)
                = UPPER(:accion)
                """
            )

            params["accion"] = accion


        if resultado:
            conditions.append(
                """
                UPPER(resultado)
                = UPPER(:resultado)
                """
            )

            params["resultado"] = resultado


        where_clause = ""

        if conditions:
            where_clause = (
                "WHERE "
                + " AND ".join(
                    conditions
                )
            )


        sql = f"""
        SELECT *
        FROM (
            SELECT
                acceso_id,
                usuario_id,
                nombre_usuario,
                nombre_rol,
                evento,
                resultado,
                detalle,
                ip_origen,
                user_agent,
                request_id,
                fecha_evento
            FROM historial_accesos
            {where_clause}
            ORDER BY
                fecha_evento DESC,
                acceso_id DESC
        )
        WHERE ROWNUM <= :limite
        """


        cursor = self.connection.cursor()

        try:
            cursor.execute(
                sql,
                params
            )

            rows = cursor.fetchall()

            return rows_to_dicts(
                cursor,
                rows
            )

        finally:
            cursor.close()


    # -----------------------------------------------------
    # ORACLE TRIGGER AUDIT
    # -----------------------------------------------------

    def get_trigger_audit(
        self,
        fecha_desde=None,
        fecha_hasta_exclusiva=None,
        usuario=None,
        accion=None,
        limite: int = 500
    ):
        conditions = []
        params = {
            "limite": limite
        }


        if fecha_desde is not None:
            conditions.append(
                "fecha_accion >= :fecha_desde"
            )

            params["fecha_desde"] = (
                fecha_desde
            )


        if fecha_hasta_exclusiva is not None:
            conditions.append(
                "fecha_accion < :fecha_hasta"
            )

            params["fecha_hasta"] = (
                fecha_hasta_exclusiva
            )


        if usuario:
            conditions.append(
                """
                UPPER(usuario_bd)
                = UPPER(:usuario)
                """
            )

            params["usuario"] = usuario


        if accion:
            conditions.append(
                """
                UPPER(accion)
                = UPPER(:accion)
                """
            )

            params["accion"] = accion


        where_clause = ""

        if conditions:
            where_clause = (
                "WHERE "
                + " AND ".join(
                    conditions
                )
            )


        sql = f"""
        SELECT *
        FROM (
            SELECT
                auditoria_id,
                nombre_tabla,
                accion,
                valor_llave,
                usuario_bd,
                fecha_accion,
                detalle
            FROM auditoria_acciones
            {where_clause}
            ORDER BY
                fecha_accion DESC,
                auditoria_id DESC
        )
        WHERE ROWNUM <= :limite
        """


        cursor = self.connection.cursor()

        try:
            cursor.execute(
                sql,
                params
            )

            rows = cursor.fetchall()

            return rows_to_dicts(
                cursor,
                rows
            )

        finally:
            cursor.close()