"""Correct clear errors in the Shona (sn) education translations (Batch 4 review, 18 November 2026).

Only Shona fields change. English articles are untouched. Each correction applies only if the
exact old wording is present, so the migration is safe to re-run and fully reversible.
All translations remain marked "draft" until a native Shona speaker confirms them.
"""
from django.db import migrations

# (article slug, field, old wording, corrected wording, reason)
TRANSLATION_FIXES = [
    (
        "understanding-anxiety",
        "content",
        "zviratidzo izvi hazvigoni kukupa kana mumwe munhu chirwere.",
        "zviratidzo izvi hazvigoni kushandiswa kuona kuti iwe kana mumwe munhu ane chirwere chipi.",
        "Said the signs cannot 'give' an illness; English means they cannot diagnose (agreed wording).",
    ),
    (
        "understanding-anxiety",
        "content",
        "kushaya hope kana kutadza kutarisa",
        "kushaya hope kana kutadza kuisa pfungwa pachinhu",
        "'kutarisa' means 'to look'; English says difficulty concentrating.",
    ),
    (
        "understanding-anxiety",
        "summary",
        "Kuzvidya mwoyo dzimwe nguva chinhu chinowanzoitika.",
        "Kunzwa kuzvidya mwoyo chinhu chinowanzoitika.",
        "'sometimes ... commonly' was contradictory; English: anxious feelings are common.",
    ),
    (
        "understanding-depression",
        "content",
        "hope, kudya kana kugona kutarisa.",
        "hope, kudya kana kugona kuisa pfungwa pachinhu.",
        "'kutarisa' means 'to look'; English says concentration.",
    ),
    (
        "mental-health-stigma",
        "content",
        "kuti atenderwe kana kubatwa neruremekedzo.",
        "kuti atendwe kana kubatwa neruremekedzo.",
        "'atenderwe' means 'be permitted'; English says 'be believed' (atendwe).",
    ),
    (
        "supporting-a-friend-who-is-struggling",
        "content",
        "kuchinja kwaunoona kuchikushungurudza, tsvaga nguva yakavanzika",
        "kuchinja kwaunoona kuchikunetsa, tsvaga nguva yamuri moga",
        "'kushungurudza' can mean abuse/torment and 'nguva yakavanzika' means secret time; "
        "English: a change that worries you, a private moment.",
    ),
    (
        "understanding-mental-health",
        "summary",
        "Dzidza zvinogona kuuhwandisa kana kuuhutadzisa uye",
        "Dzidza zvinogona kuhupesvedzera uye",
        "'kuuhwandisa' is not a word and the object concord was wrong; English: what can shape it.",
    ),
    (
        "understanding-mental-health",
        "content",
        "Hachisi kungoreva kusava nechirwere chepfungwa.",
        "Hahusi kungoreva kusava nechirwere chepfungwa.",
        "Concord must agree with 'utano' (hu-), not 'chikamu'.",
    ),
    (
        "understanding-mental-health",
        "content",
        "Kunzwa kutya, kusuruvara kana kushushikana dzimwe nguva hakurevi wega kuti",
        "Kunzwa kunetseka, kusuruvara kana kushushikana dzimwe nguva hakurevi kwega kuti",
        "English says 'worried' (kunetseka, not fear); 'wega' must agree with 'kunzwa' (kwega).",
    ),
]

# (topic slug, old wording, corrected wording, reason)
TOPIC_FIXES = [
    (
        "mental-health-stigma",
        "kuseka kana kusarudzwa zvingakanganisa",
        "kuseka kana kusarurwa zvingakanganisa",
        "'kusarudzwa' means 'being chosen'; the meaning is exclusion (kusarurwa).",
    ),
]


def _apply(apps, forward):
    ArticleTranslation = apps.get_model("education", "ArticleTranslation")
    Topic = apps.get_model("education", "Topic")

    for slug, field, old, new, _reason in TRANSLATION_FIXES:
        find, replace = (old, new) if forward else (new, old)
        for translation in ArticleTranslation.objects.filter(article__slug=slug, language__code="sn"):
            text = getattr(translation, field)
            if find in text:
                setattr(translation, field, text.replace(find, replace, 1))
                translation.save(update_fields=[field, "updated_at"])

    for slug, old, new, _reason in TOPIC_FIXES:
        find, replace = (old, new) if forward else (new, old)
        for topic in Topic.objects.filter(slug=slug):
            if find in topic.shona_description:
                topic.shona_description = topic.shona_description.replace(find, replace, 1)
                topic.save(update_fields=["shona_description", "updated_at"])


def correct(apps, schema_editor):
    _apply(apps, forward=True)


def revert(apps, schema_editor):
    _apply(apps, forward=False)


class Migration(migrations.Migration):
    dependencies = [
        ("education", "0014_set_resource_photo_countries"),
    ]

    operations = [
        migrations.RunPython(correct, revert),
    ]
