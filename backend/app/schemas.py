"""Request and response models with input normalization."""

import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

ROLL_NUMBER_PATTERN = re.compile(r"^\d{2}/[A-Z]{2,10}/\d{1,4}$")
PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")
ALLOWED_BRANCHES = {"CSE", "EEE", "ME", "CE", "B.ARCH", "MNC"}
ALLOWED_YEARS = {"1st Year", "2nd Year", "3rd Year", "4th Year"}


def clean_text(value: str) -> str:
    """Trim and collapse whitespace so stored values remain consistent."""
    return " ".join(value.strip().split())


class RegistrationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str
    studentId: str
    branch: str
    year: str
    interest: str = Field(default="")

    @field_validator("name", "interest", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return clean_text(value)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return clean_text(value).lower()

    @field_validator("phone", mode="before")
    @classmethod
    def normalize_phone(cls, value: str) -> str:
        # Keep digits only, accept +91 or leading 0 and normalize to last 10 digits
        digits = re.sub(r"\D", "", value)
        if len(digits) > 10:
            digits = digits[-10:]
        return digits

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not PHONE_PATTERN.fullmatch(value):
            raise ValueError("Phone number must be a valid 10-digit Indian mobile number.")
        return value

    @field_validator("studentId", mode="before")
    @classmethod
    def normalize_student_id(cls, value: str) -> str:
        return clean_text(value).upper().replace(" ", "")

    @field_validator("studentId")
    @classmethod
    def validate_student_id(cls, value: str) -> str:
        # Accept either an 11-digit registration ID or YY/BRANCH/ROLL
        if value.isdigit() and len(value) == 11:
            return value
        if ROLL_NUMBER_PATTERN.fullmatch(value):
            return value
        raise ValueError("Student ID must be 11 digits or use YY/BRANCH/ROLL (e.g. 25/CSE/68).")

    @field_validator("branch", mode="before")
    @classmethod
    def normalize_branch(cls, value: str) -> str:
        return clean_text(value).upper()

    @field_validator("branch")
    @classmethod
    def validate_branch(cls, value: str) -> str:
        if value not in ALLOWED_BRANCHES:
            raise ValueError("Select a valid branch.")
        return value

    @field_validator("year", mode="before")
    @classmethod
    def validate_year(cls, value: str) -> str:
        value = clean_text(value)
        if value not in ALLOWED_YEARS:
            raise ValueError("Select a valid year.")
        return value


class ApiResponse(BaseModel):
    success: bool
    message: str
