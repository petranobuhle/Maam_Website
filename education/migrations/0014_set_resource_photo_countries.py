"""Show the Zimbabwe flag on the Friendship Bench photograph (taken in Harare).

The WHO cover is a global publication, so it is deliberately given no country flag.
"""
from django.db import migrations

PHOTO_COUNTRIES = {"friendship-bench-publications": "ZW"}


def set_countries(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    LibraryResource = apps.get_model("education", "LibraryResource")
    for slug, code in PHOTO_COUNTRIES.items():
        country = Country.objects.filter(code=code).first()
        if country:
            LibraryResource.objects.filter(slug=slug, cover_image_country__isnull=True).update(
                cover_image_country=country
            )


def clear_countries(apps, schema_editor):
    LibraryResource = apps.get_model("education", "LibraryResource")
    LibraryResource.objects.filter(slug__in=PHOTO_COUNTRIES).update(cover_image_country=None)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_seed_country_language_data"),
        ("education", "0013_libraryresource_cover_image_country"),
    ]

    operations = [
        migrations.RunPython(set_countries, clear_countries),
    ]
