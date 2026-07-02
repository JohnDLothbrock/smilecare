from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import HorarioDoctorCreate, HorarioDoctorUpdate
from backend.services.horario_doctor_service import HorarioDoctorService


router = APIRouter(
    prefix="/horarios-doctores",
    tags=["Horarios Doctores"]
)


@router.get("")
def get_all_horarios_doctores(connection=Depends(get_db)):
    service = HorarioDoctorService(connection)

    return service.get_all()


@router.get("/doctor/{doctor_id}")
def get_horarios_by_doctor_id(
    doctor_id: int,
    connection=Depends(get_db)
):
    service = HorarioDoctorService(connection)

    return service.get_by_doctor_id(doctor_id)


@router.get("/{horario_id}")
def get_horario_doctor_by_id(
    horario_id: int,
    connection=Depends(get_db)
):
    service = HorarioDoctorService(connection)

    return service.get_by_id(horario_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_horario_doctor(
    data: HorarioDoctorCreate,
    connection=Depends(get_db)
):
    service = HorarioDoctorService(connection)

    return service.create(data)


@router.put("/{horario_id}")
def update_horario_doctor(
    horario_id: int,
    data: HorarioDoctorUpdate,
    connection=Depends(get_db)
):
    service = HorarioDoctorService(connection)

    return service.update(horario_id, data)


@router.delete("/{horario_id}")
def delete_horario_doctor(
    horario_id: int,
    connection=Depends(get_db)
):
    service = HorarioDoctorService(connection)

    return service.delete(horario_id)