from django.contrib import admin

from .models import Organisation, SupportService


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "city",
        "is_verified",
        "verification_status",
        "last_verified_at",
        "is_demo",
    )
    list_filter = ("is_verified", "verification_status", "is_demo", "country")
    search_fields = ("name", "city", "email")


@admin.register(SupportService)
class SupportServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organisation",
        "service_type",
        "delivery_mode",
        "is_verified",
        "verification_status",
        "last_verified_at",
        "is_demo",
    )
    list_filter = ("is_verified", "verification_status", "is_demo", "service_type", "delivery_mode", "country")
    search_fields = ("name", "description", "email")
