from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import (
    DisponibilidadDoctorCreate,
    DisponibilidadDoctorUpdate
)
from backend.services.disponibilidad_doctor_service import (
    DisponibilidadDoctorService
)


router = APIRouter(
    prefix="/disponibilidad-doctores",
    tags=["Disponibilidad Doctores"]
)


@router.get("")
def get_all_disponibilidad_doctores(connection=Depends(get_db)):
    service = DisponibilidadDoctorService(connection)

    return service.get_all()


@router.get("/doctor/{doctor_id}")
def get_disponibilidad_by_doctor_id(
    doctor_id: int,
    connection=Depends(get_db)
):
    service = DisponibilidadDoctorService(connection)

    return service.get_by_doctor_id(doctor_id)


@router.get("/{disponibilidad_id}")
def get_disponibilidad_doctor_by_id(
    disponibilidad_id: int,
    connection=Depends(get_db)
):
    service = DisponibilidadDoctorService(connection)

    return service.get_by_id(disponibilidad_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_disponibilidad_doctor(
    data: DisponibilidadDoctorCreate,
    connection=Depends(get_db)
):
    service = DisponibilidadDoctorService(connection)

    return service.create(data)


@router.put("/{disponibilidad_id}")
def update_disponibilidad_doctor(
    disponibilidad_id: int,
    data: DisponibilidadDoctorUpdate,
    connection=Depends(get_db)
):
    service = DisponibilidadDoctorService(connection)

    return service.update(disponibilidad_id, data)


@router.delete("/{disponibilidad_id}")
def delete_disponibilidad_doctor(
    disponibilidad_id: int,
    connection=Depends(get_db)
):
    service = DisponibilidadDoctorService(connection)

    return service.delete(disponibilidad_id)