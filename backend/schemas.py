from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class PacienteCreate(BaseModel):
    usuario_id: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    correo: Optional[str] = Field(default=None, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=200)
    fecha_nacimiento: Optional[date] = None


class PacienteUpdate(BaseModel):
    usuario_id: Optional[int] = None
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(default=None, min_length=1, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    correo: Optional[str] = Field(default=None, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=200)
    fecha_nacimiento: Optional[date] = None


class EspecialidadCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=200)


class EspecialidadUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=200)


class DoctorCreate(BaseModel):
    usuario_id: Optional[int] = None
    especialidad_id: int
    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    correo: Optional[str] = Field(default=None, max_length=150)


class DoctorUpdate(BaseModel):
    usuario_id: Optional[int] = None
    especialidad_id: Optional[int] = None
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(default=None, min_length=1, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    correo: Optional[str] = Field(default=None, max_length=150)


class CitaCreate(BaseModel):
    paciente_id: int
    doctor_id: int
    fecha_hora_inicio: datetime
    duracion_minutos: int = Field(gt=0, le=999)
    estado: str = Field(min_length=1, max_length=20)
    motivo: Optional[str] = Field(default=None, max_length=250)


class CitaUpdate(BaseModel):
    paciente_id: Optional[int] = None
    doctor_id: Optional[int] = None
    fecha_hora_inicio: Optional[datetime] = None
    duracion_minutos: Optional[int] = Field(default=None, gt=0, le=999)
    estado: Optional[str] = Field(default=None, min_length=1, max_length=20)
    motivo: Optional[str] = Field(default=None, max_length=250)


class ConsultaCreate(BaseModel):
    cita_id: int
    diagnostico: Optional[str] = Field(default=None, max_length=500)
    observaciones: Optional[str] = Field(default=None, max_length=500)
    fecha_atencion: Optional[datetime] = None


class ConsultaUpdate(BaseModel):
    cita_id: Optional[int] = None
    diagnostico: Optional[str] = Field(default=None, max_length=500)
    observaciones: Optional[str] = Field(default=None, max_length=500)
    fecha_atencion: Optional[datetime] = None


class TratamientoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=300)
    costo_base: float = Field(ge=0)
    estado: str = Field(min_length=1, max_length=20)


class TratamientoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=300)
    costo_base: Optional[float] = Field(default=None, ge=0)
    estado: Optional[str] = Field(default=None, min_length=1, max_length=20)


class TratamientoConsultaCreate(BaseModel):
    consulta_id: int
    tratamiento_id: int
    cantidad: int = Field(gt=0, le=99999)
    precio_unitario: Optional[float] = Field(default=None, ge=0)


class TratamientoConsultaUpdate(BaseModel):
    consulta_id: Optional[int] = None
    tratamiento_id: Optional[int] = None
    cantidad: Optional[int] = Field(default=None, gt=0, le=99999)
    precio_unitario: Optional[float] = Field(default=None, ge=0)


class FacturaCreate(BaseModel):
    paciente_id: int
    consulta_id: Optional[int] = None
    numero_factura: str = Field(min_length=1, max_length=30)
    fecha_emision: Optional[date] = None
    subtotal: Optional[float] = Field(default=None, ge=0)
    impuesto: Optional[float] = Field(default=0, ge=0)
    estado: str = Field(min_length=1, max_length=20)


class FacturaUpdate(BaseModel):
    paciente_id: Optional[int] = None
    consulta_id: Optional[int] = None
    numero_factura: Optional[str] = Field(default=None, min_length=1, max_length=30)
    fecha_emision: Optional[date] = None
    subtotal: Optional[float] = Field(default=None, ge=0)
    impuesto: Optional[float] = Field(default=None, ge=0)
    estado: Optional[str] = Field(default=None, min_length=1, max_length=20)


class DetalleFacturaCreate(BaseModel):
    factura_id: int
    tratamiento_consulta_id: Optional[int] = None
    descripcion: Optional[str] = Field(default=None, max_length=300)
    cantidad: int = Field(gt=0, le=99999)
    precio_unitario: Optional[float] = Field(default=None, ge=0)


class DetalleFacturaUpdate(BaseModel):
    factura_id: Optional[int] = None
    tratamiento_consulta_id: Optional[int] = None
    descripcion: Optional[str] = Field(default=None, max_length=300)
    cantidad: Optional[int] = Field(default=None, gt=0, le=99999)
    precio_unitario: Optional[float] = Field(default=None, ge=0)


class MetodoPagoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=200)
    estado: str = Field(min_length=1, max_length=20)


class MetodoPagoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=200)
    estado: Optional[str] = Field(default=None, min_length=1, max_length=20)


class PagoCreate(BaseModel):
    factura_id: int
    metodo_pago_id: int
    monto: float = Field(gt=0)
    fecha_pago: Optional[date] = None
    numero_referencia: Optional[str] = Field(default=None, max_length=100)
    estado: str = Field(min_length=1, max_length=20)


class PagoUpdate(BaseModel):
    factura_id: Optional[int] = None
    metodo_pago_id: Optional[int] = None
    monto: Optional[float] = Field(default=None, gt=0)
    fecha_pago: Optional[date] = None
    numero_referencia: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[str] = Field(default=None, min_length=1, max_length=20)