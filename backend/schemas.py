from datetime import date
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