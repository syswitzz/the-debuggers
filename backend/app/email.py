"""Minimal Resend email delivery for successful registrations."""

from html import escape
import logging

import resend

from .config import Settings
from .models import Registration

logger = logging.getLogger(__name__)


def _send(settings: Settings, recipient: str, subject: str, html: str) -> None:
    if not settings.resend_api_key or not settings.resend_from_email:
        logger.error("Resend is not configured; registration emails were not sent.")
        return

    resend.api_key = settings.resend_api_key
    resend.Emails.send(
        {
            "from": settings.resend_from_email,
            "to": [recipient],
            "subject": subject,
            "html": html,
        }
    )


def send_registration_emails(settings: Settings, registration: Registration) -> None:
    """Send a confirmation to the student and a concise club notification."""
    name = escape(registration.name)
    email = escape(registration.email)
    roll_number = escape(registration.roll_number)
    branch = escape(registration.branch)
    year = escape(registration.year)
    reason = escape(registration.reason)

    _send(
        settings,
        registration.email,
        "Welcome to The Debuggers",
        f"""
        <main style="font-family:Arial,sans-serif;color:#1f2937;line-height:1.6;max-width:560px;margin:auto">
          <h2>Thanks for registering, {name}.</h2>
          <p>Your registration for <strong>The Debuggers</strong>, the coding club of Gaya College of Engineering, Gaya, has been received.</p>
          <p>We will contact you about upcoming seminars and workshops.</p>
          <p>Regards,<br>The Debuggers</p>
        </main>
        """,
    )
    _send(
        settings,
        settings.notification_email,
        f"New The Debuggers registration: {name}",
        f"""
        <main style="font-family:Arial,sans-serif;color:#1f2937;line-height:1.6;max-width:560px;margin:auto">
          <h2>New registration</h2>
          <p><strong>Name:</strong> {name}<br>
          <strong>Email:</strong> {email}<br>
          <strong>Phone:</strong> {registration.phone}<br>
          <strong>Roll number:</strong> {roll_number}<br>
          <strong>Branch:</strong> {branch}<br>
          <strong>Year:</strong> {year}</p>
          <p><strong>Reason:</strong><br>{reason}</p>
        </main>
        """,
    )
