from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.database import get_db


router = APIRouter()


class UsuarioCreate(BaseModel):
    rol_id: int
    nombre_usuario: str
    password_hash: str
    estado: str


class RolCreate(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None
    estado: str


class PermisoCreate(BaseModel):
    codigo_permiso: str
    descripcion: Optional[str] = None
    modulo: Optional[str] = None


class RolPermisoCreate(BaseModel):
    rol_id: int
    permiso_id: int


def rows_to_dicts(cursor):
    columns = [column[0].lower() for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# ---------------------------------------------------------
# USUARIOS
# ---------------------------------------------------------

@router.get("/usuarios")
def get_usuarios(db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT
            u.usuario_id,
            u.rol_id,
            r.nombre_rol,
            u.nombre_usuario,
            u.password_hash,
            u.estado
        FROM usuarios u
        JOIN roles r
            ON r.rol_id = u.rol_id
        ORDER BY u.usuario_id
        """
    )

    return rows_to_dicts(cursor)


@router.post("/usuarios")
def create_usuario(usuario: UsuarioCreate, db=Depends(get_db)):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (
                rol_id,
                nombre_usuario,
                password_hash,
                estado
            )
            VALUES (
                :rol_id,
                :nombre_usuario,
                :password_hash,
                :estado
            )
            """,
            {
                "rol_id": usuario.rol_id,
                "nombre_usuario": usuario.nombre_usuario,
                "password_hash": usuario.password_hash,
                "estado": usuario.estado
            }
        )

        db.commit()

        return {"message": "Usuario creado correctamente."}

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.put("/usuarios/{usuario_id}")
def update_usuario(usuario_id: int, usuario: UsuarioCreate, db=Depends(get_db)):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            UPDATE usuarios
            SET
                rol_id = :rol_id,
                nombre_usuario = :nombre_usuario,
                password_hash = :password_hash,
                estado = :estado
            WHERE usuario_id = :usuario_id
            """,
            {
                "usuario_id": usuario_id,
                "rol_id": usuario.rol_id,
                "nombre_usuario": usuario.nombre_usuario,
                "password_hash": usuario.password_hash,
                "estado": usuario.estado
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado."
            )

        db.commit()

        return {"message": "Usuario actualizado correctamente."}

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db=Depends(get_db)):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM usuarios
            WHERE usuario_id = :usuario_id
            """,
            {"usuario_id": usuario_id}
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado."
            )

        db.commit()

        return {"message": "Usuario eliminado correctamente."}

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


# ---------------------------------------------------------
# ROLES
# ---------------------------------------------------------

@router.get("/roles")
def get_roles(db=Depends(get_db)):
    cursor = db.cursor()

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

    return rows_to_dicts(cursor)


@router.post("/roles")
def create_rol(rol: RolCreate, db=Depends(get_db)):
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
                "nombre_rol": rol.nombre_rol,
                "descripcion": rol.descripcion,
                "estado": rol.estado
            }
        )

        db.commit()

        return {"message": "Rol creado correctamente."}

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.put("/roles/{rol_id}")
def update_rol(rol_id: int, rol: RolCreate, db=Depends(get_db)):
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
                "rol_id": rol_id,
                "nombre_rol": rol.nombre_rol,
                "descripcion": rol.descripcion,
                "estado": rol.estado
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado."
            )

        db.commit()

        return {"message": "Rol actualizado correctamente."}

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/roles/{rol_id}")
def delete_rol(rol_id: int, db=Depends(get_db)):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM roles
            WHERE rol_id = :rol_id
            """,
            {"rol_id": rol_id}
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado."
            )

        db.commit()

        return {"message": "Rol eliminado correctamente."}

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


# ---------------------------------------------------------
# PERMISOS
# ---------------------------------------------------------

@router.get("/permisos")
def get_permisos(db=Depends(get_db)):
    cursor = db.cursor()

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

    return rows_to_dicts(cursor)


@router.post("/permisos")
def create_permiso(permiso: PermisoCreate, db=Depends(get_db)):
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
                "codigo_permiso": permiso.codigo_permiso,
                "descripcion": permiso.descripcion,
                "modulo": permiso.modulo
            }
        )

        db.commit()

        return {"message": "Permiso creado correctamente."}

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


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
                "permiso_id": permiso_id,
                "codigo_permiso": permiso.codigo_permiso,
                "descripcion": permiso.descripcion,
                "modulo": permiso.modulo
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Permiso no encontrado."
            )

        db.commit()

        return {"message": "Permiso actualizado correctamente."}

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/permisos/{permiso_id}")
def delete_permiso(permiso_id: int, db=Depends(get_db)):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM permisos
            WHERE permiso_id = :permiso_id
            """,
            {"permiso_id": permiso_id}
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Permiso no encontrado."
            )

        db.commit()

        return {"message": "Permiso eliminado correctamente."}

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


# ---------------------------------------------------------
# ROL_PERMISOS
# ---------------------------------------------------------

@router.get("/rol-permisos")
def get_rol_permisos(db=Depends(get_db)):
    cursor = db.cursor()

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
        JOIN roles r
            ON r.rol_id = rp.rol_id
        JOIN permisos p
            ON p.permiso_id = rp.permiso_id
        ORDER BY
            r.nombre_rol,
            p.modulo,
            p.codigo_permiso
        """
    )

    return rows_to_dicts(cursor)


@router.post("/rol-permisos")
def create_rol_permiso(
    rol_permiso: RolPermisoCreate,
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO rol_permisos (
                rol_id,
                permiso_id
            )
            SELECT
                :rol_id,
                :permiso_id
            FROM dual
            WHERE NOT EXISTS (
                SELECT 1
                FROM rol_permisos
                WHERE rol_id = :rol_id
                AND permiso_id = :permiso_id
            )
            """,
            {
                "rol_id": rol_permiso.rol_id,
                "permiso_id": rol_permiso.permiso_id
            }
        )

        db.commit()

        return {"message": "Permiso asignado al rol correctamente."}

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/rol-permisos/{rol_id}/{permiso_id}")
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
                "rol_id": rol_id,
                "permiso_id": permiso_id
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Relación rol-permiso no encontrada."
            )

        db.commit()

        return {"message": "Permiso removido del rol correctamente."}

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))


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
                "rol_id": rol_id,
                "permiso_id": permiso_id
            }
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Relación rol-permiso no encontrada."
            )

        db.commit()

        return {"message": "Permiso removido del rol correctamente."}

    except HTTPException:
        db.rollback()
        raise

    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))