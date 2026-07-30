"""Small database operations for registrations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Registration
from .schemas import RegistrationCreate


def get_by_email(db: Session, email: str) -> Registration | None:
    return db.scalar(select(Registration).where(Registration.email == email))


def get_by_student_id(db: Session, student_id: str) -> Registration | None:
    return db.scalar(select(Registration).where(Registration.student_id == student_id))


def create_registration(db: Session, registration: RegistrationCreate) -> Registration:
    data = registration.model_dump()
    # Map API camelCase studentId to DB snake_case student_id
    if 'studentId' in data:
        data['student_id'] = data.pop('studentId')
    record = Registration(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
