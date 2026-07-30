"""Request and response models with input normalization."""

import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

ROLL_NUMBER_PATTERN = re.compile(r"^\d{2}/[A-Z]{2,10}/\d{1,4}$")
PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")
ALLOWED_BRANCHES = {"CSE", "EEE", "ME", "CE", "ECE", "OTHER"}
ALLOWED_YEARS = {"1st Year", "2nd Year", "3rd Year", "4th Year"}


def clean_text(value: str) -> str:
    """Trim and collapse whitespace so stored values remain consistent."""
    return " ".join(value.strip().split())


class RegistrationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str
    roll_number: str
    branch: str
    year: str
    reason: str = Field(min_length=12, max_length=1000)

    @field_validator("name", "reason", mode="before")
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
        return re.sub(r"[\s-]", "", value)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not PHONE_PATTERN.fullmatch(value):
            raise ValueError("Phone number must be a valid 10-digit Indian mobile number.")
        return value

    @field_validator("roll_number", mode="before")
    @classmethod
    def normalize_roll_number(cls, value: str) -> str:
        return clean_text(value).upper().replace(" ", "")

    @field_validator("roll_number")
    @classmethod
    def validate_roll_number(cls, value: str) -> str:
        if not ROLL_NUMBER_PATTERN.fullmatch(value):
            raise ValueError("Roll number must use YY/BRANCH/ROLL, for example 25/CSE/68.")
        return value

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
