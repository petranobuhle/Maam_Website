from django.db import migrations


TOPIC_CONTENT = {
    "understanding-mental-health": (
        "Understanding mental health",
        "What mental health means, what can shape it, and why it is part of everyday wellbeing.",
    ),
    "stress": (
        "Stress",
        "Learn how pressure can affect wellbeing and when it may help to seek support.",
    ),
    "anxiety": (
        "Anxiety",
        "Understand anxious feelings and when ongoing worry may need professional support.",
    ),
    "depression": (
        "Depression",
        "Learn how persistent low mood can affect daily life and where support may help.",
    ),
    "mental-health-stigma": (
        "Mental health stigma",
        "Explore how stereotypes and discrimination can affect conversations and help-seeking.",
    ),
    "supporting-a-friend": (
        "Supporting a friend",
        "Practical, respectful ways to listen, check in and connect a friend with support.",
    ),
    "seeking-professional-help": (
        "Seeking professional help",
        "Ways to begin looking for qualified support and questions you can ask.",
    ),
}

ORIGINAL_ARTICLES = {
    "understanding-mental-health": {
        "title": "Understanding mental health",
        "summary": "A basic guide to what mental health is, why it matters and how support can help.",
        "content": "Mental health includes how you think, feel and cope with daily life and stress. It changes over time and can be supported through safe relationships, education and trusted care.",
    },
    "stress-and-everyday-pressure": {
        "title": "Stress and everyday pressure",
        "summary": "A practical explanation of stress, common triggers and healthy ways to respond.",
        "content": "Stress is a normal human response to pressure, but constant stress can affect sleep, mood and concentration. Recognising signs early can help people seek support earlier.",
    },
    "supporting-a-friend-who-is-struggling": {
        "title": "Supporting a friend who is struggling",
        "summary": "Simple and respectful ways to listen, encourage help and avoid judgment.",
        "content": "Support works best when it is calm, patient and practical. Listening without pressure, checking on someone and encouraging trusted support can make a real difference.",
    },
}

ARTICLES = {
    "understanding-mental-health": {
        "title": "Understanding mental health",
        "summary": (
            "Mental health is part of everyday wellbeing. Learn what can shape it and when it may help "
            "to talk with someone."
        ),
        "content": (
            "The World Health Organization describes mental health as wellbeing that helps a person "
            "cope with life's stresses, learn, work and contribute to their community. It is part of "
            "overall health, not simply the absence of a mental health condition.\n\n"
            "Mental health can change over time. Personal circumstances, relationships, safety, "
            "living conditions and community support can all matter. Feeling worried, grieving or "
            "stressed at times does not by itself establish a diagnosis.\n\n"
            "If a concern persists, feels overwhelming or makes everyday activities difficult, "
            "consider speaking with someone you trust or a qualified health professional. MAAM "
            "shares general education; it does not assess or treat individuals."
        ),
        "source_name": "World Health Organization: Mental health",
        "source_url": "https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response",
        "topics": ["understanding-mental-health"],
        "featured": True,
    },
    "stress-and-everyday-pressure": {
        "title": "Stress and everyday pressure",
        "summary": (
            "Pressure from school, relationships, change or difficult circumstances can affect "
            "wellbeing. Stress is not a personal failing."
        ),
        "content": (
            "Stress is a common feeling when someone is under pressure, overwhelmed or finding it "
            "hard to cope. Exams, changes at home or school, friendship difficulties, illness, "
            "financial problems and unsafe environments can all add pressure. People respond "
            "differently, and stress is not a sign of weakness.\n\n"
            "Notice what is weighing on you and, if it feels safe, tell someone you trust. Small "
            "steps such as taking a pause, keeping a routine where possible, or asking for practical "
            "help may support wellbeing. These steps do not replace professional care when stress "
            "persists or disrupts daily life.\n\n"
            "If pressure involves danger, violence or serious hardship, you deserve support from "
            "trusted people and appropriate local services. Responsibility does not rest on one "
            "person to cope alone."
        ),
        "source_name": "UNICEF Parenting: What is stress?",
        "source_url": "https://www.unicef.org/parenting/mental-health/what-is-stress",
        "topics": ["stress"],
        "featured": False,
    },
    "supporting-a-friend-who-is-struggling": {
        "title": "Supporting a friend who is struggling",
        "summary": (
            "Listen without judgment, ask what would help and encourage appropriate support without "
            "trying to diagnose or fix everything."
        ),
        "content": (
            "Start with care, not a label. If you notice a change that worries you, choose a private "
            "moment and ask an open question such as, “How have things been for you?” Listen calmly "
            "and without judgment. Do not minimize what they say, make assumptions or pressure them "
            "to share more than they want.\n\n"
            "Ask what kind of support would feel helpful. You might check in later or offer to help "
            "them speak with a trusted adult or qualified service. Be honest about what you can do; "
            "you cannot promise to solve everything or keep a serious safety concern secret.\n\n"
            "If you are worried that someone may be in immediate danger, involve a trusted adult or "
            "appropriate local professional rather than carrying the concern alone. You can care "
            "about a friend without becoming their counsellor."
        ),
        "source_name": "Friendship Bench Zimbabwe: Online support and advice",
        "source_url": "https://www.friendshipbenchzimbabwe.org/online",
        "topics": ["supporting-a-friend"],
        "featured": False,
    },
    "understanding-anxiety": {
        "title": "Understanding anxiety",
        "summary": (
            "Anxious feelings are common. Persistent, excessive worry that interferes with daily life "
            "is a reason to consider asking for support."
        ),
        "content": (
            "Feeling anxious before an exam, presentation or uncertain event is common. Anxiety "
            "disorders involve fear or worry that is excessive, difficult to control, can last over "
            "time and may interfere with school, relationships or everyday activities.\n\n"
            "People can experience anxiety differently. Tension, restlessness, trouble sleeping or "
            "difficulty concentrating can have many causes; a list of signs cannot diagnose you or "
            "someone else.\n\n"
            "If worry feels overwhelming, continues for a long time or makes daily activities hard, "
            "consider speaking with a qualified health professional. Seeking support is not a "
            "personal failure."
        ),
        "source_name": "World Health Organization: Anxiety disorders",
        "source_url": "https://www.who.int/news-room/fact-sheets/detail/anxiety-disorders",
        "topics": ["anxiety"],
        "featured": False,
    },
    "understanding-depression": {
        "title": "Understanding depression",
        "summary": (
            "Depression is more than a difficult day. Learn how persistent low mood can affect "
            "everyday life and why assessment belongs to a qualified professional."
        ),
        "content": (
            "The World Health Organization describes depression as depressed mood or a loss of "
            "interest or pleasure that lasts for long periods. It can affect relationships, school, "
            "work and other parts of daily life.\n\n"
            "Some people also experience changes in energy, sleep, appetite or concentration. "
            "Experiences differ, and one feeling or sign does not prove that someone has depression. "
            "Only a qualified professional can assess an individual.\n\n"
            "If low mood or loss of interest persists or affects daily life, consider speaking with "
            "a qualified health professional or someone you trust. You do not need to decide what "
            "to call the experience before asking for support."
        ),
        "source_name": "World Health Organization: Depression",
        "source_url": "https://www.who.int/news-room/fact-sheets/detail/depression",
        "topics": ["depression"],
        "featured": False,
    },
    "mental-health-stigma": {
        "title": "Mental health stigma: replacing assumptions with understanding",
        "summary": (
            "Stereotypes and discrimination can make it harder to speak openly or seek help. "
            "Respectful listening is one way communities can respond."
        ),
        "content": (
            "Stigma can appear as stereotypes, teasing, blame, exclusion or discrimination related "
            "to mental health. It can also show up in assumptions that distress is weakness or that "
            "someone should simply “get over it.” These ideas do not explain a person's experience.\n\n"
            "The World Health Organization notes that stigma can affect young people's readiness "
            "to seek help. No one should be pressured to disclose personal experiences in order to "
            "be believed or treated with dignity.\n\n"
            "We can help challenge stigma by listening without judgment, using respectful language, "
            "asking rather than assuming, protecting privacy and sharing credible information."
        ),
        "source_name": "World Health Organization: Mental health of adolescents",
        "source_url": "https://www.who.int/news-room/fact-sheets/detail/adolescent-mental-health",
        "topics": ["mental-health-stigma"],
        "featured": False,
    },
    "seeking-professional-help": {
        "title": "Seeking professional help",
        "summary": (
            "You can ask for support without diagnosing yourself first. Learn how to start a "
            "conversation and check which local options are available."
        ),
        "content": (
            "A qualified health professional can listen, assess what is affecting you and discuss "
            "possible support. Care can be provided in different settings; what is available depends "
            "on the service and location.\n\n"
            "You could begin by speaking with a trusted healthcare provider or contacting an "
            "organisation in the MAAM Support Directory. Ask the organisation directly about its "
            "services, who provides them, cost, languages, opening hours, privacy and how to make "
            "an appointment. These details can vary and should not be assumed from a listing.\n\n"
            "You do not need to have a diagnosis or know the right words before asking a question. "
            "MAAM provides education and a directory; it does not provide clinical care or emergency "
            "response."
        ),
        "source_name": "World Health Organization: Mental health",
        "source_url": "https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response",
        "topics": ["seeking-professional-help"],
        "featured": False,
    },
}


def update_learning_content(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    Topic = apps.get_model("education", "Topic")
    Article = apps.get_model("education", "Article")

    country = Country.objects.get(code="ZW", is_active=True)
    topics = {}
    for slug, (name, description) in TOPIC_CONTENT.items():
        topic = Topic.objects.filter(slug=slug, is_active=True).first()
        if topic is None or topic.name != name:
            raise RuntimeError(f"Expected active education topic {name!r} ({slug}).")
        topic.description = description
        topic.save()
        topics[slug] = topic

    for slug, content in ARTICLES.items():
        if slug in ORIGINAL_ARTICLES:
            article = Article.objects.get(slug=slug)
        else:
            if Article.objects.filter(slug=slug).exists():
                raise RuntimeError(f"Refusing to overwrite an existing article with slug {slug!r}.")
            article = Article(slug=slug)

        article.title = content["title"]
        article.summary = content["summary"]
        article.content = content["content"]
        article.country = country
        article.is_published = True
        article.is_demo = False
        article.is_featured = content["featured"]
        article.source_name = content["source_name"]
        article.source_url = content["source_url"]
        article.save()
        article.topics.set([topics[topic_slug] for topic_slug in content["topics"]])


def restore_learning_content(apps, schema_editor):
    Topic = apps.get_model("education", "Topic")
    Article = apps.get_model("education", "Article")

    new_slugs = [slug for slug in ARTICLES if slug not in ORIGINAL_ARTICLES]
    Article.objects.filter(slug__in=new_slugs).delete()

    for slug, content in ORIGINAL_ARTICLES.items():
        article = Article.objects.get(slug=slug)
        article.title = content["title"]
        article.summary = content["summary"]
        article.content = content["content"]
        article.is_published = True
        article.is_demo = True
        article.is_featured = slug == "understanding-mental-health"
        article.source_name = ""
        article.source_url = ""
        article.save()
        article.topics.clear()

    for slug, (name, _description) in TOPIC_CONTENT.items():
        topic = Topic.objects.get(slug=slug)
        topic.description = f"Educational content exploring {name.lower()}."
        topic.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_seed_country_language_data"),
        ("education", "0004_article_cover_image_libraryresource_cover_image_and_more"),
    ]

    operations = [
        migrations.RunPython(update_learning_content, restore_learning_content),
    ]
