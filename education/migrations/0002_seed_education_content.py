from django.db import migrations
from django.utils import timezone


def seed_education_content(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    Language = apps.get_model("core", "Language")
    Topic = apps.get_model("education", "Topic")
    Article = apps.get_model("education", "Article")
    ArticleTranslation = apps.get_model("education", "ArticleTranslation")
    AudioResource = apps.get_model("education", "AudioResource")

    country = Country.objects.filter(code="ZW", is_active=True).first()
    language_en = Language.objects.filter(code="en", is_active=True).first()
    language_sn = Language.objects.filter(code="sn", is_active=True).first()
    if not country or not language_en or not language_sn:
        return

    topic_names = [
        "Understanding mental health",
        "Stress",
        "Anxiety",
        "Depression",
        "Mental health stigma",
        "Supporting a friend",
        "Seeking professional help",
    ]
    for name in topic_names:
        Topic.objects.get_or_create(
            name=name,
            defaults={
                "slug": name.lower().replace(" & ", "-").replace(" ", "-").replace("/", "-")[:120],
                "description": f"Educational content exploring {name.lower()}.",
                "country": country,
                "is_active": True,
            },
        )

    article_data = [
        {
            "title": "Understanding mental health",
            "slug": "understanding-mental-health",
            "summary": "A basic guide to what mental health is, why it matters and how support can help.",
            "content": "Mental health includes how you think, feel and cope with daily life and stress. It changes over time and can be supported through safe relationships, education and trusted care.",
            "shona_title": "Kunzwisisa utano hwepfungwa",
            "shona_summary": "Mushumo wepasi rose unotsanangura utano hwepfungwa, kukosha kwawo uye kuti rubatsiro runogona kubatsira sei.",
            "shona_content": "Utenzi hwepfungwa hunosanganisira maitiro aunofunga, kunzwa uye kubata zvinetso pazuva nezuva. Hunochinja nguva dzose uye hunogona kubatsirwa nerudo rwakachengeteka, dzidzo uye rubatsiro rwakavimbika.",
        },
        {
            "title": "Stress and everyday pressure",
            "slug": "stress-and-everyday-pressure",
            "summary": "A practical explanation of stress, common triggers and healthy ways to respond.",
            "content": "Stress is a normal human response to pressure, but constant stress can affect sleep, mood and concentration. Recognising signs early can help people seek support earlier.",
            "shona_title": "Kushushikana uye kudzvinyirirwa kwemazuva ese",
            "shona_summary": "Mushumo unotsanangura kushushikana, zvinokonzeresa uye nzira dzinobatsira dzekuzvidzivirira.",
            "shona_content": "Kushushikana ibasa rakajairika remunhu pakudzvinyirirwa, asi kushushikana nguva dzose kunogona kukanganisa hope, mweya uye kutarisa. Kuziva zviratidzo nguva isati yapfuura kunogona kubatsira vanhu kutsvaga rubatsiro pakutanga.",
        },
        {
            "title": "Supporting a friend who is struggling",
            "slug": "supporting-a-friend-who-is-struggling",
            "summary": "Simple and respectful ways to listen, encourage help and avoid judgment.",
            "content": "Support works best when it is calm, patient and practical. Listening without pressure, checking on someone and encouraging trusted support can make a real difference.",
            "shona_title": "Kutsigira shamwari iri kushushikana",
            "shona_summary": "Zvinhu zvakareruka uye zvine mutsindo zvekuteerera, kukurudzira rubatsiro uye kudzivirira kutonga.",
            "shona_content": "Rubatsiro runoshanda zvakanyanya kana rwuri rwakanyarara, rwunogamuchira, uye rwunoshanda. Kuteerera pasina kumanikidza, kubvunza nemwoyo murefu uye kukurudzira rubatsiro rwakavimbika kunogona kuita mutsauko.",
        },
    ]

    for item in article_data:
        article, _ = Article.objects.get_or_create(
            slug=item["slug"],
            defaults={
                "title": item["title"],
                "summary": item["summary"],
                "content": item["content"],
                "country": country,
                "is_featured": item["slug"] == "understanding-mental-health",
                "is_published": True,
            },
        )
        ArticleTranslation.objects.get_or_create(
            article=article,
            language=language_en,
            defaults={
                "title": item["title"],
                "summary": item["summary"],
                "content": item["content"],
                "review_status": "reviewed",
                "reviewed_at": timezone.now(),
            },
        )
        ArticleTranslation.objects.get_or_create(
            article=article,
            language=language_sn,
            defaults={
                "title": item["shona_title"],
                "summary": item["shona_summary"],
                "content": item["shona_content"],
                "review_status": "reviewed",
                "reviewed_at": timezone.now(),
            },
        )

        AudioResource.objects.get_or_create(
            slug=f"{item['slug']}-audio",
            defaults={
                "article": article,
                "language": language_en,
                "title": f"{item['title']} audio",
                "audio_url": "",
                "download_url": "",
                "transcript": "Sample educational audio transcript for demonstration purposes only. This content is not a diagnosis or emergency guidance.",
                "duration_seconds": 180,
                "is_approved": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("education", "0001_initial"),
        ("core", "0002_seed_country_language_data"),
    ]

    operations = [
        migrations.RunPython(seed_education_content, migrations.RunPython.noop),
    ]
