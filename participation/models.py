import uuid

from django.db import models


class NotificationStatus(models.TextChoices):
    PENDING = "pending", "Not sent yet"
    SENDING = "sending", "Sending"
    ACCEPTED = "accepted", "Accepted by Resend (delivery not confirmed)"
    FAILED = "failed", "Failed – check the logs and retry"
    DISABLED = "disabled", "Not sent – email notifications are switched off"


class NotificationTracking(models.Model):
    """Records whether MAAM staff were notified about a submission. Never shown publicly."""

    notification_status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
        editable=False,
    )
    notification_reference = models.CharField(
        max_length=100,
        blank=True,
        editable=False,
        help_text="Email ID returned by Resend when it accepted the notification.",
    )
    notification_attempts = models.PositiveSmallIntegerField(default=0, editable=False)
    notification_attempted_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True


class VolunteerInterest(NotificationTracking):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    country = models.CharField(max_length=80, blank=True)
    role_interest = models.CharField(max_length=80)
    availability = models.CharField(max_length=80, blank=True)
    motivation = models.TextField()
    consent_to_contact = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name


class PartnershipInquiry(NotificationTracking):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=120)
    email = models.EmailField()
    country = models.CharField(max_length=80, blank=True)
    partnership_type = models.CharField(max_length=80)
    message = models.TextField()
    consent_to_contact = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.organisation_name
