"""SQLAlchemy database models."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Registration(Base):
    __tablename__ = "registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    student_id: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    branch: Mapped[str] = mapped_column(String(20), nullable=False)
    year: Mapped[str] = mapped_column(String(20), nullable=False)
    interest: Mapped[str] = mapped_column(Text, nullable=True)
