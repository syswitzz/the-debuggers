"""Minimal Resend email delivery for successful registrations."""

import logging
from html import escape

from .config import Settings
from .models import Registration

logger = logging.getLogger(__name__)

try:
    import resend
except ImportError:  # pragma: no cover - environment dependent
    resend = None


def _send(settings: Settings, to_email: str, subject: str, html: str) -> None:
    """Send an email through Resend when configuration is present."""
    if not settings.resend_api_key:
        logger.info("Resend API key not configured; skipping registration email to %s", to_email)
        return

    if resend is None:
        logger.warning("resend package is not available; skipping registration email to %s", to_email)
        return

    try:
        resend.api_key = settings.resend_api_key
        resend.Emails.send(
            {
                "from": settings.resend_from_email or "onboarding@resend.dev",
                "to": [to_email],
                "subject": subject,
                "html": html,
            }
        )
    except Exception:
        logger.exception("Failed to send registration email to %s", to_email)


def send_registration_emails(settings: Settings, registration: Registration) -> None:
    """Send a single confirmation email to the applicant."""
    name = escape(registration.name)
    email = escape(registration.email)
    student_id = escape(registration.student_id)
    branch = escape(registration.branch)
    year = escape(registration.year)
    interest = escape(registration.interest or "")

    interest_html = (
        f'<p style="margin:6px 0"><strong>Interest:</strong> {interest}</p>' if interest else ""
    )

    html = f"""
<main style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; color:#111827; line-height:1.5; max-width:600px; margin:0 auto; padding:16px">
  <header style="text-align:left; margin-bottom:12px">
    <h2 style="margin:0 0 6px 0; font-size:20px;">Thanks for joining The Debuggers, {name}!</h2>
    <p style="margin:0; color:#6b7280; font-size:14px">Your registration has been received — here are the details we saved:</p>
  </header>
  <section style="background:#fff; border-radius:8px; padding:12px; box-shadow:0 1px 0 rgba(0,0,0,0.04)">
    <p style="margin:6px 0"><strong>Email:</strong> {email}</p>
    <p style="margin:6px 0"><strong>Phone:</strong> {escape(registration.phone)}</p>
    <p style="margin:6px 0"><strong>Student ID:</strong> {student_id}</p>
    <p style="margin:6px 0"><strong>Branch:</strong> {branch} · <strong>Year:</strong> {year}</p>
    {interest_html}
  </section>
  <section style="margin-top:12px">
    <h3 style="margin:0 0 8px 0; font-size:16px">Welcome to the community</h3>
    <p style="margin:0 0 8px 0; color:#4b5563; font-size:14px">The Debuggers is a student-run coding club at Gaya College of Engineering. We organise hands-on workshops, project nights, and study groups across topics like web development, algorithms, and systems.</p>
    <p style="margin:0 0 8px 0; color:#4b5563; font-size:14px">Join our communities:</p>
    <p style="margin:0 0 6px 0"><a href="https://chat.whatsapp.com/IKu6rbcxIpGBe5hwo1gCRX?s=cl&p=a&ilr=1" style="color:#0ea5a4; text-decoration:none">WhatsApp group</a> · <a href="https://github.com/The-Debuggers-GCE" style="color:#0ea5a4; text-decoration:none">GitHub community</a></p>
  </section>
  <footer style="margin-top:18px; color:#6b7280; font-size:13px">
    <p style="margin:0">We will be in touch with upcoming sessions — keep an eye on your inbox and the WhatsApp group.</p>
    <p style="margin:8px 0 0 0">Cheers,<br><strong>The Debuggers</strong></p>
  </footer>
</main>
"""

    _send(settings, registration.email, "Your registration — The Debuggers", html)
