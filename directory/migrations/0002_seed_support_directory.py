from django.db import migrations


def seed_support_directory(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    Organisation = apps.get_model("directory", "Organisation")
    SupportService = apps.get_model("directory", "SupportService")

    country = Country.objects.filter(code="ZW", is_active=True).first()
    if not country:
        return

    organisation, _ = Organisation.objects.get_or_create(
        slug="harare-youth-wellbeing-network",
        defaults={
            "name": "Harare Youth Wellbeing Network",
            "country": country,
            "city": "Harare",
            "website": "https://example.org",
            "phone": "+263 123 4567",
            "email": "hello@example.org",
            "description": "Sample demonstration support organisation for the MAAM project. Replace with verified information before launch.",
            "is_verified": True,
            "verification_status": "verified",
            "last_verified_at": "2026-11-12T00:00:00Z",
        },
    )

    SupportService.objects.get_or_create(
        organisation=organisation,
        country=country,
        name="Youth wellbeing information line",
        defaults={
            "service_type": "helpline",
            "description": "Sample service for education and referral guidance.",
            "city": "Harare",
            "phone": "+263 123 4567",
            "email": "hello@example.org",
            "website": "https://example.org",
            "is_verified": True,
            "verification_status": "verified",
            "last_verified_at": "2026-11-12T00:00:00Z",
            "is_active": True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("directory", "0001_initial"),
        ("core", "0002_seed_country_language_data"),
    ]

    operations = [
        migrations.RunPython(seed_support_directory, migrations.RunPython.noop),
    ]
