from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from backend.core.security import (
    hash_password
)
from backend.database import get_db


router = APIRouter()


# ---------------------------------------------------------
# SCHEMAS
# ---------------------------------------------------------

class UsuarioCreate(BaseModel):
    rol_id: int

    nombre_usuario: str = Field(
        min_length=3,
        max_length=50
    )

    correo: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    estado: str = Field(
        pattern="^(ACTIVO|INACTIVO|BLOQUEADO)$"
    )


class UsuarioUpdate(BaseModel):
    rol_id: int

    nombre_usuario: str = Field(
        min_length=3,
        max_length=50
    )

    correo: EmailStr

    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=128
    )

    estado: str = Field(
        pattern="^(ACTIVO|INACTIVO|BLOQUEADO)$"
    )


class RolCreate(BaseModel):
    nombre_rol: str = Field(
        min_length=1,
        max_length=50
    )

    descripcion: Optional[str] = None

    estado: str = Field(
        pattern="^(ACTIVO|INACTIVO)$"
    )


class PermisoCreate(BaseModel):
    codigo_permiso: str = Field(
        min_length=1,
        max_length=80
    )

    descripcion: Optional[str] = None

    modulo: Optional[str] = None


class RolPermisoCreate(BaseModel):
    rol_id: int
    permiso_id: int


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def rows_to_dicts(cursor):
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
        for row in cursor.fetchall()
    ]


def raise_security_database_error(
    error: Exception
):
    error_message = str(error)

    if "ORA-00001" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo guardar la información "
                "porque existe un valor único repetido."
            )
        )

    if "ORA-02291" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo guardar la información "
                "porque uno de los registros relacionados "
                "no existe."
            )
        )

    if "ORA-02292" in error_message:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se puede eliminar el registro porque "
                "tiene información relacionada."
            )
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=(
            "Error de base de datos: "
            f"{error_message}"
        )
    )


# ---------------------------------------------------------
# USUARIOS
# ---------------------------------------------------------

@router.get("/usuarios")
def get_usuarios(
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT
                u.usuario_id,
                u.rol_id,
                r.nombre_rol,
                u.nombre_usuario,
                u.correo,
                u.estado
            FROM usuarios u
            INNER JOIN roles r
                ON r.rol_id = u.rol_id
            ORDER BY u.usuario_id
            """
        )

        return rows_to_dicts(
            cursor
        )

    except Exception as error:
        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.post(
    "/usuarios",
    status_code=status.HTTP_201_CREATED
)
def create_usuario(
    usuario: UsuarioCreate,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        hashed_password = hash_password(
            usuario.password
        )

        cursor.execute(
            """
            INSERT INTO usuarios (
                rol_id,
                nombre_usuario,
                correo,
                password_hash,
                estado
            )
            VALUES (
                :rol_id,
                :nombre_usuario,
                :correo,
                :password_hash,
                :estado
            )
            """,
            {
                "rol_id":
                    usuario.rol_id,

                "nombre_usuario":
                    usuario.nombre_usuario.strip(),

                "correo":
                    str(usuario.correo).strip().lower(),

                "password_hash":
                    hashed_password,

                "estado":
                    usuario.estado
            }
        )

        db.commit()

        return {
            "message":
                "Usuario creado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.put("/usuarios/{usuario_id}")
def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        update_data = {
            "usuario_id":
                usuario_id,

            "rol_id":
                usuario.rol_id,

            "nombre_usuario":
                usuario.nombre_usuario.strip(),

            "correo":
                str(usuario.correo).strip().lower(),

            "estado":
                usuario.estado
        }

        set_parts = [
            "rol_id = :rol_id",
            "nombre_usuario = :nombre_usuario",
            "correo = :correo",
            "estado = :estado"
        ]

        if usuario.password is not None:
            update_data[
                "password_hash"
            ] = hash_password(
                usuario.password
            )

            set_parts.append(
                "password_hash = :password_hash"
            )

        sql = f"""
        UPDATE usuarios
        SET {", ".join(set_parts)}
        WHERE usuario_id = :usuario_id
        """

        cursor.execute(
            sql,
            update_data
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Usuario no encontrado."
                )
            )

        db.commit()

        return {
            "message":
                "Usuario actualizado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.delete("/usuarios/{usuario_id}")
def delete_usuario(
    usuario_id: int,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM usuarios
            WHERE usuario_id = :usuario_id
            """,
            {
                "usuario_id":
                    usuario_id
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Usuario no encontrado."
                )
            )

        db.commit()

        return {
            "message":
                "Usuario eliminado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


# ---------------------------------------------------------
# ROLES
# ---------------------------------------------------------

@router.get("/roles")
def get_roles(
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT
                rol_id,
                nombre_rol,
                descripcion,
                estado
            FROM roles
            ORDER BY rol_id
            """
        )

        return rows_to_dicts(
            cursor
        )

    except Exception as error:
        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.post(
    "/roles",
    status_code=status.HTTP_201_CREATED
)
def create_rol(
    rol: RolCreate,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO roles (
                nombre_rol,
                descripcion,
                estado
            )
            VALUES (
                :nombre_rol,
                :descripcion,
                :estado
            )
            """,
            {
                "nombre_rol":
                    rol.nombre_rol.strip(),

                "descripcion":
                    rol.descripcion,

                "estado":
                    rol.estado
            }
        )

        db.commit()

        return {
            "message":
                "Rol creado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.put("/roles/{rol_id}")
def update_rol(
    rol_id: int,
    rol: RolCreate,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            UPDATE roles
            SET
                nombre_rol = :nombre_rol,
                descripcion = :descripcion,
                estado = :estado
            WHERE rol_id = :rol_id
            """,
            {
                "rol_id":
                    rol_id,

                "nombre_rol":
                    rol.nombre_rol.strip(),

                "descripcion":
                    rol.descripcion,

                "estado":
                    rol.estado
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Rol no encontrado."
                )
            )

        db.commit()

        return {
            "message":
                "Rol actualizado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.delete("/roles/{rol_id}")
def delete_rol(
    rol_id: int,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM roles
            WHERE rol_id = :rol_id
            """,
            {
                "rol_id":
                    rol_id
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Rol no encontrado."
                )
            )

        db.commit()

        return {
            "message":
                "Rol eliminado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


# ---------------------------------------------------------
# PERMISOS
# ---------------------------------------------------------

@router.get("/permisos")
def get_permisos(
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT
                permiso_id,
                codigo_permiso,
                descripcion,
                modulo
            FROM permisos
            ORDER BY permiso_id
            """
        )

        return rows_to_dicts(
            cursor
        )

    except Exception as error:
        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.post(
    "/permisos",
    status_code=status.HTTP_201_CREATED
)
def create_permiso(
    permiso: PermisoCreate,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO permisos (
                codigo_permiso,
                descripcion,
                modulo
            )
            VALUES (
                :codigo_permiso,
                :descripcion,
                :modulo
            )
            """,
            {
                "codigo_permiso":
                    permiso.codigo_permiso.strip(),

                "descripcion":
                    permiso.descripcion,

                "modulo":
                    permiso.modulo
            }
        )

        db.commit()

        return {
            "message":
                "Permiso creado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.put("/permisos/{permiso_id}")
def update_permiso(
    permiso_id: int,
    permiso: PermisoCreate,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            UPDATE permisos
            SET
                codigo_permiso = :codigo_permiso,
                descripcion = :descripcion,
                modulo = :modulo
            WHERE permiso_id = :permiso_id
            """,
            {
                "permiso_id":
                    permiso_id,

                "codigo_permiso":
                    permiso.codigo_permiso.strip(),

                "descripcion":
                    permiso.descripcion,

                "modulo":
                    permiso.modulo
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Permiso no encontrado."
                )
            )

        db.commit()

        return {
            "message":
                "Permiso actualizado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.delete("/permisos/{permiso_id}")
def delete_permiso(
    permiso_id: int,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM permisos
            WHERE permiso_id = :permiso_id
            """,
            {
                "permiso_id":
                    permiso_id
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Permiso no encontrado."
                )
            )

        db.commit()

        return {
            "message":
                "Permiso eliminado correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


# ---------------------------------------------------------
# ROL_PERMISOS
# ---------------------------------------------------------

@router.get("/rol-permisos")
def get_rol_permisos(
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT
                rp.rol_id,
                r.nombre_rol,
                rp.permiso_id,
                p.codigo_permiso,
                p.modulo,
                p.descripcion
            FROM rol_permisos rp
            INNER JOIN roles r
                ON r.rol_id = rp.rol_id
            INNER JOIN permisos p
                ON p.permiso_id = rp.permiso_id
            ORDER BY
                r.nombre_rol,
                p.modulo,
                p.codigo_permiso
            """
        )

        return rows_to_dicts(
            cursor
        )

    except Exception as error:
        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.post(
    "/rol-permisos",
    status_code=status.HTTP_201_CREATED
)
def create_rol_permiso(
    rol_permiso: RolPermisoCreate,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT 1
            FROM rol_permisos
            WHERE rol_id = :rol_id
            AND permiso_id = :permiso_id
            """,
            {
                "rol_id":
                    rol_permiso.rol_id,

                "permiso_id":
                    rol_permiso.permiso_id
            }
        )

        existing_relation = cursor.fetchone()

        if existing_relation is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Este permiso ya está asignado "
                    "al rol seleccionado."
                )
            )

        cursor.execute(
            """
            INSERT INTO rol_permisos (
                rol_id,
                permiso_id
            )
            VALUES (
                :rol_id,
                :permiso_id
            )
            """,
            {
                "rol_id":
                    rol_permiso.rol_id,

                "permiso_id":
                    rol_permiso.permiso_id
            }
        )

        db.commit()

        return {
            "message":
                "Permiso asignado al rol correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.delete(
    "/rol-permisos/{rol_id}/{permiso_id}"
)
def delete_rol_permiso_path(
    rol_id: int,
    permiso_id: int,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM rol_permisos
            WHERE rol_id = :rol_id
            AND permiso_id = :permiso_id
            """,
            {
                "rol_id":
                    rol_id,

                "permiso_id":
                    permiso_id
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Relación rol-permiso "
                    "no encontrada."
                )
            )

        db.commit()

        return {
            "message":
                "Permiso removido del rol correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()


@router.delete("/rol-permisos")
def delete_rol_permiso_query(
    rol_id: int,
    permiso_id: int,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM rol_permisos
            WHERE rol_id = :rol_id
            AND permiso_id = :permiso_id
            """,
            {
                "rol_id":
                    rol_id,

                "permiso_id":
                    permiso_id
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Relación rol-permiso "
                    "no encontrada."
                )
            )

        db.commit()

        return {
            "message":
                "Permiso removido del rol correctamente."
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()

        raise_security_database_error(
            error
        )

    finally:
        cursor.close()