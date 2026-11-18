import datetime

from django.db import migrations


VERIFIED_AT = datetime.datetime(2026, 11, 17, tzinfo=datetime.timezone.utc)


def seed_verified_zimbabwe_listings(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    Organisation = apps.get_model("directory", "Organisation")
    SupportService = apps.get_model("directory", "SupportService")
    country = Country.objects.filter(code="ZW", is_active=True).first()
    if country is None:
        return

    friendship_bench, _ = Organisation.objects.update_or_create(
        slug="friendship-bench-zimbabwe",
        defaults={
            "name": "Friendship Bench Zimbabwe",
            "country": country,
            "city": "",
            "address": "",
            "website": "https://www.friendshipbenchzimbabwe.org/",
            "phone": "",
            "email": "",
            "description": (
                "Friendship Bench describes its approach as community-based, "
                "evidence-informed psychological support delivered through trained "
                "community mental health supporters."
            ),
            "verification_source": "https://www.friendshipbenchzimbabwe.org/",
            "is_verified": True,
            "is_demo": False,
            "verification_status": "verified",
            "last_verified_at": VERIFIED_AT,
        },
    )
    SupportService.objects.update_or_create(
        organisation=friendship_bench,
        name="Online mental health and psychosocial support",
        defaults={
            "country": country,
            "service_type": "Direct mental health and psychosocial support",
            "delivery_mode": "online",
            "description": (
                "The official service page describes one-to-one support by WhatsApp "
                "call or chat from trained Friendship Bench mental health supporters. "
                "The organisation describes sessions as free; mobile or call charges "
                "may apply."
            ),
            "intended_for": (
                "The official page describes support for people experiencing "
                "mild-to-moderate depression, anxiety, substance misuse, emotional "
                "distress and related concerns. Contact Friendship Bench to confirm "
                "whether the service is suitable for you."
            ),
            "languages": "English, Shona and Ndebele",
            "operating_hours": "Monday–Friday, 9am–4pm; Saturday, 9am–12pm",
            "whatsapp_url": "https://wa.me/263784845294",
            "phone": "+263 784 845 294",
            "email": "",
            "website": "https://www.friendshipbenchzimbabwe.org/online",
            "verification_source": "https://www.friendshipbenchzimbabwe.org/online",
            "is_verified": True,
            "verification_status": "verified",
            "last_verified_at": VERIFIED_AT,
            "is_demo": False,
            "is_active": True,
        },
    )

    zimnamh, _ = Organisation.objects.update_or_create(
        slug="zimbabwe-national-association-for-mental-health",
        defaults={
            "name": "Zimbabwe National Association for Mental Health (ZIMNAMH)",
            "country": country,
            "city": "Harare",
            "address": (
                "Psychiatry Unit, Sally Mugabe Hospital (formerly Harare Hospital), "
                "Sotherton, Harare, Zimbabwe"
            ),
            "website": "https://zimnamh.org.zw/",
            "phone": "+263 772 571 075",
            "email": "info@zimnamh.org.zw",
            "description": (
                "ZIMNAMH describes itself as a Zimbabwean membership-based organisation "
                "working to advance the rights and wellbeing of people with mental "
                "disabilities. Its website describes mental health awareness, advocacy, "
                "rehabilitation and disability support."
            ),
            "verification_source": "https://zimnamh.org.zw/contact.html",
            "is_verified": True,
            "is_demo": False,
            "verification_status": "verified",
            "last_verified_at": VERIFIED_AT,
        },
    )
    SupportService.objects.update_or_create(
        organisation=zimnamh,
        name="Mental health awareness and advocacy",
        defaults={
            "country": country,
            "service_type": "Mental health advocacy and education",
            "delivery_mode": "community",
            "description": (
                "ZIMNAMH's official website describes mental health awareness "
                "campaigns, education, community outreach and advocacy. Contact the "
                "organisation to confirm current programmes and availability."
            ),
            "intended_for": "",
            "languages": "",
            "operating_hours": "",
            "whatsapp_url": "",
            "phone": "",
            "email": "",
            "website": "https://zimnamh.org.zw/",
            "verification_source": "https://zimnamh.org.zw/",
            "is_verified": True,
            "verification_status": "verified",
            "last_verified_at": VERIFIED_AT,
            "is_demo": False,
            "is_active": True,
        },
    )
    SupportService.objects.update_or_create(
        organisation=zimnamh,
        name="Mental rehabilitation and disability support",
        defaults={
            "country": country,
            "service_type": "Rehabilitation and disability support",
            "delivery_mode": "not_stated",
            "description": (
                "ZIMNAMH's official website describes mental rehabilitation and "
                "disability support. Specific services, access arrangements, eligibility "
                "and current availability are not detailed on the cited pages; contact "
                "the organisation to confirm."
            ),
            "intended_for": (
                "The organisation describes work with people with mental and psychosocial "
                "disabilities; programme-level eligibility is not stated."
            ),
            "languages": "",
            "operating_hours": "",
            "whatsapp_url": "",
            "phone": "",
            "email": "",
            "website": "https://zimnamh.org.zw/",
            "verification_source": "https://zimnamh.org.zw/",
            "is_verified": True,
            "verification_status": "verified",
            "last_verified_at": VERIFIED_AT,
            "is_demo": False,
            "is_active": True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("directory", "0005_organisation_address_supportservice_delivery_mode_and_more"),
        ("core", "0002_seed_country_language_data"),
    ]

    operations = [
        migrations.RunPython(
            seed_verified_zimbabwe_listings,
            migrations.RunPython.noop,
        ),
    ]
