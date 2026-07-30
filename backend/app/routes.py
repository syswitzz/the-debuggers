"""HTTP routes for club registrations."""

import logging

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import crud
from .config import get_settings
from .database import get_db
from .email import send_registration_emails
from .schemas import ApiResponse, RegistrationCreate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["registrations"])
limiter = Limiter(key_func=lambda request: request.client.host if request.client else "unknown")


@router.post(
    "/register",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
def register(
    request: Request,
    payload: RegistrationCreate,
    db: Session = Depends(get_db),
) -> ApiResponse | JSONResponse:
    """Store one registration, reject duplicates, then send two emails."""
    if crud.get_by_email(db, payload.email):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"success": False, "message": "Email already registered."},
        )
    if crud.get_by_roll_number(db, payload.roll_number):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"success": False, "message": "Roll number already registered."},
        )

    try:
        registration = crud.create_registration(db, payload)
    except IntegrityError:
        # Unique database constraints also protect against simultaneous requests.
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"success": False, "message": "Email or roll number already registered."},
        )

    try:
        send_registration_emails(get_settings(), registration)
    except Exception:
        # The registration is valid and safely saved even if Resend is temporarily unavailable.
        logger.exception("Could not send registration emails for registration %s", registration.id)

    return ApiResponse(success=True, message="Registration successful.")
