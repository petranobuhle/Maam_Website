from django.db import migrations


def seed_country_language_data(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    Language = apps.get_model("core", "Language")

    Country.objects.get_or_create(
        code="ZW",
        defaults={
            "name": "Zimbabwe",
            "official_name": "Republic of Zimbabwe",
            "region": "Southern Africa",
            "is_active": True,
        },
    )
    Country.objects.get_or_create(
        code="RW",
        defaults={
            "name": "Rwanda",
            "official_name": "Republic of Rwanda",
            "region": "East Africa",
            "is_active": False,
        },
    )

    Language.objects.get_or_create(
        code="en",
        defaults={
            "name": "English",
            "native_name": "English",
            "is_active": True,
        },
    )
    Language.objects.get_or_create(
        code="sn",
        defaults={
            "name": "Shona",
            "native_name": "Chishona",
            "is_active": True,
        },
    )
    Language.objects.get_or_create(
        code="rw",
        defaults={
            "name": "Kinyarwanda",
            "native_name": "Ikinyarwanda",
            "is_active": False,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_country_language_data, migrations.RunPython.noop),
    ]
