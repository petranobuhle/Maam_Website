from django.contrib import admin

from .models import Campaign, CampaignResource


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "country", "is_active", "is_demo", "start_date", "end_date")
    list_filter = ("is_active", "is_demo", "country")
    search_fields = ("title", "summary")


@admin.register(CampaignResource)
class CampaignResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "campaign", "resource_type")
    list_filter = ("resource_type",)
    search_fields = ("title", "description")
