from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Query
)

from backend.database import get_db
from backend.services.audit_admin_service import (
    AuditAdminService
)


router = APIRouter(
    prefix="/admin/auditoria",
    tags=["Administración - Auditoría"]
)


@router.get("/dashboard")
def get_audit_dashboard(
    fecha_desde: Optional[str] = Query(
        default=None
    ),
    fecha_hasta: Optional[str] = Query(
        default=None
    ),
    usuario: Optional[str] = Query(
        default=None
    ),
    modulo: Optional[str] = Query(
        default=None
    ),
    accion: Optional[str] = Query(
        default=None
    ),
    resultado: Optional[str] = Query(
        default=None
    ),
    limite: int = Query(
        default=500,
        ge=1,
        le=1000
    ),
    connection=Depends(get_db)
):
    audit_service = AuditAdminService(
        connection
    )

    return audit_service.get_dashboard(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        usuario=usuario,
        modulo=modulo,
        accion=accion,
        resultado=resultado,
        limite=limite
    )