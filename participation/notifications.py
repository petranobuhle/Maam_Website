"""Staff email notifications for new Get Involved submissions, sent through Resend's HTTPS API.

Privacy and safety rules:
- The email says only that a form was submitted, when, a reference ID and an admin link.
  Names, email addresses and messages are NOT included; staff read them in the admin.
- Log lines contain only the form type, reference ID and an HTTP status. Never personal
  details, request bodies or the API key.
- "Accepted" means Resend accepted the email for sending. It does not prove delivery.
- This function never raises, so a notification problem can never lose a submission.
"""
import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from .models import NotificationStatus

logger = logging.getLogger("participation.notifications")

FORM_LABELS = {
    "volunteerinterest": "volunteer interest",
    "partnershipinquiry": "partnership inquiry",
}


def _claim(submission):
    """Atomically move PENDING -> SENDING. Only one caller can ever win, preventing duplicates."""
    model = type(submission)
    claimed = model.objects.filter(pk=submission.pk, notification_status=NotificationStatus.PENDING).update(
        notification_status=NotificationStatus.SENDING
    )
    return claimed == 1


def _record(submission, status, reference="", count_attempt=True):
    model = type(submission)
    attempts = submission.notification_attempts + (1 if count_attempt else 0)
    fields = {
        "notification_status": status,
        "notification_reference": reference[:100],
        "notification_attempts": attempts,
        "notification_attempted_at": timezone.now() if count_attempt else submission.notification_attempted_at,
    }
    model.objects.filter(pk=submission.pk).update(**fields)
    for name, value in fields.items():
        setattr(submission, name, value)


def _email_text(form_label, submission, admin_link):
    submitted = timezone.localtime(submission.created_at).strftime("%d %B %Y at %H:%M")
    return (
        f"A new {form_label} form was submitted on the MAAM website.\n\n"
        f"Submitted: {submitted} ({settings.TIME_ZONE})\n"
        f"Reference: {submission.pk}\n\n"
        "For privacy, this email does not include the person's details or message.\n"
        "Sign in to the MAAM admin to read the submission:\n"
        f"{admin_link}\n\n"
        "This is an automatic notification. MAAM is an awareness and education initiative, not a "
        "counselling or emergency service. If a submission raises a safeguarding concern, follow "
        "MAAM's safeguarding guidance.\n"
    )


def notify_new_submission(submission, request, *, retry=False):
    """Send at most one notification for a saved submission. Returns the final status."""
    model_name = submission._meta.model_name
    form_label = FORM_LABELS.get(model_name, "form")

    if retry:
        # Only failed (or switched-off) notifications may be retried; accepted ones are never sent twice.
        model = type(submission)
        retryable = [NotificationStatus.FAILED, NotificationStatus.DISABLED]
        if model.objects.filter(pk=submission.pk, notification_status__in=retryable).update(
            notification_status=NotificationStatus.PENDING
        ) != 1:
            return submission.notification_status
        submission.notification_status = NotificationStatus.PENDING

    if not _claim(submission):
        return submission.notification_status

    if not settings.RESEND_API_KEY:
        _record(submission, NotificationStatus.DISABLED, count_attempt=False)
        return NotificationStatus.DISABLED

    admin_link = request.build_absolute_uri(
        reverse(f"admin:participation_{model_name}_change", args=[submission.pk])
    )
    payload = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [settings.NOTIFICATION_EMAIL],
        "subject": f"New MAAM {form_label} submission",
        "text": _email_text(form_label, submission, admin_link),
    }
    attempt_number = submission.notification_attempts + 1
    api_request = urllib.request.Request(
        settings.RESEND_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "maam-website/1.0",
            # Resend ignores a repeated key for 24 hours, a second guard against duplicates.
            "Idempotency-Key": f"maam-{model_name}/{submission.pk}/attempt-{attempt_number}",
        },
    )

    try:
        with urllib.request.urlopen(api_request, timeout=settings.RESEND_TIMEOUT_SECONDS) as response:
            body = json.loads(response.read().decode("utf-8") or "{}")
        email_id = str(body.get("id", "")) if isinstance(body, dict) else ""
        if not email_id:
            raise ValueError("Resend response had no email ID")
    except urllib.error.HTTPError as error:
        _record(submission, NotificationStatus.FAILED)
        logger.warning(
            "Notification for %s %s was rejected by Resend (HTTP %s).", model_name, submission.pk, error.code
        )
        return NotificationStatus.FAILED
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        _record(submission, NotificationStatus.FAILED)
        logger.warning(
            "Notification for %s %s could not be sent (%s).", model_name, submission.pk, type(error).__name__
        )
        return NotificationStatus.FAILED

    _record(submission, NotificationStatus.ACCEPTED, reference=email_id)
    logger.info("Notification for %s %s accepted by Resend.", model_name, submission.pk)
    return NotificationStatus.ACCEPTED
