from django.contrib import admin, messages

from .models import NotificationStatus, PartnershipInquiry, VolunteerInterest
from .notifications import notify_new_submission

NOTIFICATION_FIELDS = (
    "notification_status",
    "notification_reference",
    "notification_attempts",
    "notification_attempted_at",
)


@admin.action(description="Retry staff email notification (failed or switched-off only)")
def retry_notification(modeladmin, request, queryset):
    results = {}
    for submission in queryset:
        status = notify_new_submission(submission, request, retry=True)
        results[status] = results.get(status, 0) + 1
    accepted = results.get(NotificationStatus.ACCEPTED, 0)
    failed = results.get(NotificationStatus.FAILED, 0)
    disabled = results.get(NotificationStatus.DISABLED, 0)
    skipped = sum(results.values()) - accepted - failed - disabled
    if accepted:
        modeladmin.message_user(
            request, f"{accepted} notification(s) accepted by Resend. Delivery is not confirmed.", messages.SUCCESS
        )
    if failed:
        modeladmin.message_user(request, f"{failed} notification(s) failed again. Check the logs.", messages.ERROR)
    if disabled:
        modeladmin.message_user(
            request, f"{disabled} not sent: RESEND_API_KEY is not set.", messages.WARNING
        )
    if skipped:
        modeladmin.message_user(
            request, f"{skipped} skipped: already accepted or in progress, so not sent again.", messages.INFO
        )


class SubmissionAdmin(admin.ModelAdmin):
    actions = [retry_notification]
    list_filter = ("notification_status",)
    readonly_fields = NOTIFICATION_FIELDS


@admin.register(VolunteerInterest)
class VolunteerInterestAdmin(SubmissionAdmin):
    list_display = ("full_name", "email", "role_interest", "country", "created_at", "notification_status")
    search_fields = ("full_name", "email", "role_interest")


@admin.register(PartnershipInquiry)
class PartnershipInquiryAdmin(SubmissionAdmin):
    list_display = (
        "organisation_name",
        "contact_name",
        "email",
        "partnership_type",
        "created_at",
        "notification_status",
    )
    search_fields = ("organisation_name", "contact_name", "email")
