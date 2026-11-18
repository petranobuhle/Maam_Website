import re
import uuid

from django.core.exceptions import ValidationError
from django.db import models

from core.models import Country


class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="organisations")
    city = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    verification_source = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("verified", "Verified"), ("rejected", "Rejected")],
        default="pending",
    )
    last_verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def clean(self):
        marked_verified = self.is_verified or self.verification_status == "verified"
        if marked_verified and self.is_demo:
            raise ValidationError("Demonstration organisations cannot be marked verified.")
        if marked_verified and (not self.verification_source or not self.last_verified_at):
            raise ValidationError("Provide an official verification source and date before verification.")

    def __str__(self):
        return self.name

    @property
    def phone_numbers(self):
        return tuple(
            number.strip()
            for number in re.split(r"[/,;|]", self.phone)
            if number.strip()
        )

    @property
    def phone_number_links(self):
        links = []
        for number in self.phone_numbers:
            uri = re.sub(r"[^\d+]", "", number)
            if uri.startswith("0"):
                uri = f"+263{uri[1:]}"
            links.append((number, uri))
        return tuple(links)


class SupportService(models.Model):
    class DeliveryMode(models.TextChoices):
        ONLINE = "online", "Online"
        IN_PERSON = "in_person", "In person"
        PHONE = "phone", "Phone"
        COMMUNITY = "community", "Community-based"
        HYBRID = "hybrid", "Online and in person"
        NOT_STATED = "not_stated", "Not stated by organisation"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="services")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="support_services")
    name = models.CharField(max_length=180)
    service_type = models.CharField(max_length=80)
    delivery_mode = models.CharField(
        max_length=20,
        choices=DeliveryMode.choices,
        default=DeliveryMode.NOT_STATED,
    )
    description = models.TextField(blank=True)
    intended_for = models.TextField(blank=True)
    languages = models.CharField(max_length=255, blank=True)
    operating_hours = models.CharField(max_length=255, blank=True)
    whatsapp_url = models.URLField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    verification_source = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("verified", "Verified"), ("rejected", "Rejected")],
        default="pending",
    )
    last_verified_at = models.DateTimeField(null=True, blank=True)
    is_demo = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def clean(self):
        marked_verified = self.is_verified or self.verification_status == "verified"
        organisation_is_demo = bool(
            self.organisation_id and self.organisation.is_demo
        )
        if marked_verified and (self.is_demo or organisation_is_demo):
            raise ValidationError("Demonstration services cannot be marked verified.")
        if marked_verified and (not self.verification_source or not self.last_verified_at):
            raise ValidationError("Provide an official verification source and date before verification.")

    def __str__(self):
        return f"{self.name} ({self.organisation.name})"
