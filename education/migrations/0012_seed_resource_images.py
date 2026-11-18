"""Attach licensed images to library resources.

Only images with a confirmed open licence are added. Resources whose images are
copyright-reserved (WHO fact sheet, UNICEF pages and report) are left without a photograph.
"""
from django.db import migrations

IMAGES = {
    "friendship-bench-publications": {
        "cover_image_static": "images/resources/friendship-bench-harare-costa-juta.jpg",
        "cover_image_alt": (
            "A Friendship Bench grandmother holding a clipboard talks with a client on a wooden bench "
            "outdoors in Harare, Zimbabwe."
        ),
        "cover_image_credit": "Photo: Costa Juta",
        "cover_image_source_name": "Wikimedia Commons",
        "cover_image_source_url": "https://commons.wikimedia.org/wiki/File:Friendship-Bench-Zimbabwe.jpg",
        "cover_image_licence_name": "CC BY-SA 4.0",
        "cover_image_licence_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "cover_image_focus": "center",
        "cover_image_rights_notes": (
            "Checked 18 November 2026. Wikimedia Commons file 'Friendship-Bench-Zimbabwe.jpg' by Costa Juta, "
            "dated 21 October 2022. Licence: CC BY-SA 4.0. Author permission confirmed by Wikimedia VRT, "
            "ticket 2022102110144325. Description: 'Friendship Bench Grandmother and client having a problem "
            "solving therapy session on the Friendship Bench in Harare, Zimbabwe'. Stored as the 1280px "
            "Wikimedia thumbnail; not otherwise edited. If MAAM edits the image, the edited version must also "
            "be shared under CC BY-SA 4.0."
        ),
    },
    "who-doing-what-matters-times-stress": {
        "cover_image_static": "images/resources/who-doing-what-matters-cover.jpg",
        "cover_image_alt": (
            "Front cover of the WHO guide Doing What Matters in Times of Stress: An Illustrated Guide, "
            "with a drawing of people of different ages sharing a meal at a long table."
        ),
        "cover_image_credit": "Cover: World Health Organization (2020)",
        "cover_image_source_name": "WHO",
        "cover_image_source_url": "https://www.who.int/publications/i/item/9789240003927",
        "cover_image_licence_name": "CC BY-NC-SA 3.0 IGO",
        "cover_image_licence_url": "https://creativecommons.org/licenses/by-nc-sa/3.0/igo/",
        "cover_image_focus": "top",
        "cover_image_rights_notes": (
            "Checked 18 November 2026. Publication front cover (from the WHO publication page). The guide is "
            "licensed CC BY-NC-SA 3.0 IGO (non-commercial use with credit). WHO's licence terms say the WHO "
            "logo may not be used, so the card crops to the top of the cover and the logo is not shown. "
            "MAAM must remain non-commercial for this licence to apply."
        ),
    },
}


def add_images(apps, schema_editor):
    LibraryResource = apps.get_model("education", "LibraryResource")
    for slug, fields in IMAGES.items():
        LibraryResource.objects.filter(slug=slug, cover_image_static="").update(**fields)


def remove_images(apps, schema_editor):
    LibraryResource = apps.get_model("education", "LibraryResource")
    blank = {field: "" for field in next(iter(IMAGES.values())) if field != "cover_image_focus"}
    for slug, fields in IMAGES.items():
        LibraryResource.objects.filter(slug=slug, cover_image_static=fields["cover_image_static"]).update(
            **blank, cover_image_focus="center"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("education", "0011_libraryresource_image_rights"),
    ]

    operations = [
        migrations.RunPython(add_images, remove_images),
    ]
