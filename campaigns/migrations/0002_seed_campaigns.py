from django.db import migrations
from django.utils import timezone


def seed_campaigns(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    Campaign = apps.get_model("campaigns", "Campaign")
    CampaignResource = apps.get_model("campaigns", "CampaignResource")

    country = Country.objects.filter(code="ZW", is_active=True).first()
    if not country:
        return

    campaign, _ = Campaign.objects.get_or_create(
        slug="listening-is-support-changing-how-we-respond-to-young-peoples-mental-health",
        defaults={
            "title": "Listening Is Support — Changing How We Respond to Young People's Mental Health.",
            "summary": "A youth-led campaign centred on empathy, trauma-informed listening and prevention through community trust.",
            "objective": "Encourage adults and peers to listen with empathy and connect young people to trusted support sooner.",
            "target_audience": "Young people, parents, teachers, youth leaders, and community support networks.",
            "country": country,
            "start_date": timezone.now().date(),
            "is_active": True,
        },
    )

    CampaignResource.objects.get_or_create(
        campaign=campaign,
        title="Campaign discussion guide",
        defaults={
            "resource_type": "document",
            "description": "Sample campaign discussion guide for community conversations.",
            "url": "",
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("campaigns", "0001_initial"),
        ("core", "0002_seed_country_language_data"),
    ]

    operations = [
        migrations.RunPython(seed_campaigns, migrations.RunPython.noop),
    ]
