from django.db import migrations


RESOURCES = [
    {
        "title": "Mental health of adolescents",
        "slug": "who-adolescent-mental-health",
        "category": "other",
        "summary": (
            "World Health Organization fact sheet on adolescent mental health, including common "
            "challenges, risk and protective factors, and ways to support young people. Updated "
            "1 September 2025."
        ),
        "external_url": "https://www.who.int/news-room/fact-sheets/detail/adolescent-mental-health",
        "source_name": "World Health Organization",
        "source_url": "https://www.who.int/news-room/fact-sheets/detail/adolescent-mental-health",
    },
    {
        "title": "Doing What Matters in Times of Stress: An Illustrated Guide",
        "slug": "who-doing-what-matters-times-stress",
        "category": "guide",
        "summary": (
            "A World Health Organization guide with practical skills for coping with stress. "
            "Published 29 April 2020."
        ),
        "external_url": (
            "https://iris.who.int/server/api/core/bitstreams/"
            "65bb7c04-5180-4773-a0d8-0d5be2cc35a0/content"
        ),
        "source_name": "World Health Organization",
        "source_url": "https://www.who.int/publications/i/item/9789240003927",
    },
    {
        "title": "The State of the World's Children 2021: On My Mind",
        "slug": "unicef-state-world-children-2021",
        "category": "research",
        "summary": (
            "UNICEF's flagship report on children’s and caregivers’ mental health, including "
            "risk and protective factors and social influences. Published October 2021."
        ),
        "external_url": "https://www.unicef.org/reports/state-worlds-children-2021",
        "source_name": "UNICEF",
        "source_url": "https://www.unicef.org/reports/state-worlds-children-2021",
    },
    {
        "title": "Mental health and well-being",
        "slug": "unicef-mental-health-wellbeing",
        "category": "other",
        "summary": (
            "UNICEF's online collection of guidance and resources on supporting children’s "
            "and caregivers’ mental health. No publication date is listed on the page."
        ),
        "external_url": "https://www.unicef.org/parenting/mental-health-and-well-being",
        "source_name": "UNICEF",
        "source_url": "https://www.unicef.org/parenting/mental-health-and-well-being",
    },
    {
        "title": "Friendship Bench publications",
        "slug": "friendship-bench-publications",
        "category": "other",
        "summary": (
            "The Friendship Bench's publications page, including research on mental health "
            "and help-seeking among young people in Zimbabwe. Publication dates are listed "
            "with individual entries."
        ),
        "external_url": "https://www.friendshipbench.org/publications",
        "source_name": "Friendship Bench",
        "source_url": "https://www.friendshipbench.org/publications",
    },
]

VIDEOS = [
    {
        "title": "Mental health in adolescence",
        "slug": "who-mental-health-in-adolescence",
        "media_type": "video",
        "summary": (
            "A short World Health Organization video about mental health during adolescence. "
            "Read the linked WHO fact sheet for further information."
        ),
        "media_url": "https://www.youtube.com/watch?v=HMRaun9yRWk",
        "source_name": "World Health Organization",
        "source_url": "https://www.who.int/news-room/fact-sheets/detail/adolescent-mental-health",
        "captions_url": "https://www.youtube.com/watch?v=HMRaun9yRWk&cc_load_policy=1",
    },
    {
        "title": "How to support young people's mental health",
        "slug": "unicef-support-young-peoples-mental-health",
        "media_type": "video",
        "summary": (
            "A short UNICEF video about supporting young people's mental health. The linked "
            "UNICEF page provides related written guidance."
        ),
        "media_url": "https://www.youtube.com/watch?v=Fk_UuIx_-O8",
        "source_name": "UNICEF",
        "source_url": "https://www.unicef.org/parenting/mental-health-and-well-being",
    },
]


def seed_resources_and_videos(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    LibraryResource = apps.get_model("education", "LibraryResource")
    MediaItem = apps.get_model("education", "MediaItem")
    country = Country.objects.get(code="ZW")

    for fields in RESOURCES:
        LibraryResource.objects.get_or_create(
            slug=fields["slug"],
            defaults={**fields, "country_id": country.pk, "is_published": True},
        )

    for fields in VIDEOS:
        MediaItem.objects.get_or_create(
            slug=fields["slug"],
            defaults={**fields, "country_id": country.pk, "is_published": True},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("education", "0007_mediaitem_source_name_mediaitem_source_url"),
    ]

    operations = [
        migrations.RunPython(seed_resources_and_videos, migrations.RunPython.noop),
    ]
