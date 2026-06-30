from fastapi import APIRouter, Depends, status

from backend.database import get_db
from backend.schemas import DoctorCreate, DoctorUpdate
from backend.services.doctor_service import DoctorService


router = APIRouter(
    prefix="/doctores",
    tags=["Doctores"]
)


@router.get("")
def get_doctores(connection=Depends(get_db)):
    doctor_service = DoctorService(connection)

    return doctor_service.get_all_doctores()


@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, connection=Depends(get_db)):
    doctor_service = DoctorService(connection)

    return doctor_service.get_doctor_by_id(doctor_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor: DoctorCreate,
    connection=Depends(get_db)
):
    doctor_service = DoctorService(connection)

    doctor_data = doctor.model_dump()

    return doctor_service.create_doctor(doctor_data)


@router.put("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    connection=Depends(get_db)
):
    doctor_service = DoctorService(connection)

    doctor_data = doctor.model_dump(exclude_unset=True)

    return doctor_service.update_doctor(
        doctor_id,
        doctor_data
    )


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, connection=Depends(get_db)):
    doctor_service = DoctorService(connection)

    return doctor_service.delete_doctor(doctor_id)