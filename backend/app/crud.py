"""Small database operations for registrations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Registration
from .schemas import RegistrationCreate


def get_by_email(db: Session, email: str) -> Registration | None:
    return db.scalar(select(Registration).where(Registration.email == email))


def get_by_roll_number(db: Session, roll_number: str) -> Registration | None:
    return db.scalar(select(Registration).where(Registration.roll_number == roll_number))


def create_registration(db: Session, registration: RegistrationCreate) -> Registration:
    record = Registration(**registration.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
