import uuid

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from core.models import Country


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    target_audience = models.TextField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="campaigns")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_demo = models.BooleanField(default=False)
    cover_image = models.FileField(
        upload_to="campaign_covers/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])],
    )
    cover_image_url = models.URLField(blank=True)
    cover_image_alt = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if (self.cover_image or self.cover_image_url) and not self.cover_image_alt:
            raise ValidationError({"cover_image_alt": "Describe the campaign image for readers using assistive technology."})

    def __str__(self):
        return self.title


class CampaignResource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=50, default="document")
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="campaign_resources/", blank=True)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
