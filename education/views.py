from django.db.models import Case, F, IntegerField, Prefetch, Q, Value, When
from django.shortcuts import render

from core.models import Country
from .models import (
    Article,
    ArticleTranslation,
    AudioResource,
    CommunityStory,
    LibraryResource,
    MediaItem,
    Topic,
)
from .ui_translations import get_education_ui


def _get_active_country():
    return Country.objects.filter(is_active=True).order_by("name").first()


def _education_language_code(request):
    return "sn" if request.GET.get("lang") == "sn" else "en"


def _shona_translation_prefetch():
    return Prefetch(
        "translations",
        queryset=ArticleTranslation.objects.filter(language__code="sn")
        .exclude(review_status=ArticleTranslation.ReviewStatus.ARCHIVED)
        .select_related("language"),
        to_attr="education_translations",
    )


def _attach_education_translation(objects, language_code):
    for item in objects:
        translations = getattr(item, "education_translations", [])
        item.display_translation = translations[0] if language_code == "sn" and translations else None


def learn(request):
    language_code = _education_language_code(request)
    country = _get_active_country()
    articles = (
        Article.objects.filter(is_published=True)
        .filter(Q(country=country) | Q(country__isnull=True))
        .order_by("-is_featured", "title")
        .prefetch_related("topics", _shona_translation_prefetch())
    )
    topics = list(
        Topic.objects.filter(is_active=True)
        .filter(Q(country=country) | Q(country__isnull=True))
        .prefetch_related(Prefetch("articles", queryset=articles, to_attr="published_articles"))
        .order_by("name")
    )
    articles = list(articles)
    _attach_education_translation(articles, language_code)
    for topic in topics:
        topic.display_name = topic.shona_name if language_code == "sn" and topic.shona_name else topic.name
        topic.display_description = (
            topic.shona_description
            if language_code == "sn" and topic.shona_description
            else topic.description
        )
        _attach_education_translation(topic.published_articles, language_code)
    has_draft_translations = language_code == "sn" and any(
        article.display_translation
        and article.display_translation.review_status == ArticleTranslation.ReviewStatus.DRAFT
        for article in articles
    )
    return render(
        request,
        "education/learn.html",
        {
            "articles": articles,
            "topics": topics,
            "country": country,
            "language_code": language_code,
            "ui": get_education_ui(language_code),
            "has_draft_translations": has_draft_translations,
        },
    )


def article_detail(request, slug):
    language_code = _education_language_code(request)
    country = _get_active_country()
    article = Article.objects.filter(
        Q(country=country) | Q(country__isnull=True),
        slug=slug,
        is_published=True,
    ).prefetch_related("topics", _shona_translation_prefetch()).first()
    if article is None:
        return render(
            request,
            "education/article_not_found.html",
            {
                "slug": slug,
                "language_code": language_code,
                "ui": get_education_ui(language_code),
            },
            status=404,
        )

    article.display_translation = None
    translations = getattr(article, "education_translations", [])
    translation = translations[0] if language_code == "sn" and translations else None
    article.display_translation = translation

    related_articles = (
        Article.objects.filter(
            Q(country=country) | Q(country__isnull=True),
            is_published=True,
        )
        .exclude(id=article.id)
        .order_by("-is_featured", "title")[:3]
        .prefetch_related(_shona_translation_prefetch())
    )
    related_articles = list(related_articles)
    _attach_education_translation(related_articles, language_code)
    return render(
        request,
        "education/article_detail.html",
        {
            "article": article,
            "translation": translation,
            "related_articles": related_articles,
            "language_code": language_code,
            "ui": get_education_ui(language_code),
        },
    )


def listen(request):
    country = _get_active_country()
    audio_resources = (
        AudioResource.objects.filter(
            article__country=country,
            article__is_published=True,
            article__is_demo=False,
            is_approved=True,
            is_demo=False,
        )
        .exclude(audio_url="")
        .select_related("article", "language")
        .order_by("title")
    )
    return render(
        request,
        "education/listen.html",
        {"audio_resources": audio_resources, "country": country},
    )


def watch_listen(request):
    country = _get_active_country()
    media_items = MediaItem.objects.filter(
        country=country,
        is_published=True,
        is_demo=False,
        media_url__gt="",
        source_name__gt="",
        source_url__gt="",
    )
    audio_resources = (
        AudioResource.objects.filter(
            article__country=country,
            article__is_published=True,
            article__is_demo=False,
            is_approved=True,
            is_demo=False,
        )
        .exclude(audio_url="")
        .select_related("article", "language")
    )
    return render(
        request,
        "education/watch_listen.html",
        {
            "media_items": media_items,
            "audio_resources": audio_resources,
            "country": country,
        },
    )


PRIORITY_COUNTRY_CODE = "ZW"


def _public_stories():
    """Published stories that meet the consent, licence or link-only rules for their type."""
    Story = CommunityStory
    community = Q(story_type=Story.StoryType.COMMUNITY, consent_confirmed=True) & ~Q(body="")
    republished = (
        Q(story_type=Story.StoryType.REPUBLISHED)
        & ~Q(body="")
        & ~Q(author_display="")
        & ~Q(source_url="")
        & ~Q(licence_name="")
        & ~Q(licence_url="")
        & ~Q(attribution_text="")
    )
    external = Q(story_type=Story.StoryType.EXTERNAL, body="") & ~Q(source_url="") & ~Q(source_name="")
    return (
        Story.objects.filter(is_published=True, is_demo=False)
        .filter(community | republished | external)
        .select_related("country")
        .annotate(
            country_priority=Case(
                When(country__code=PRIORITY_COUNTRY_CODE, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("country_priority", "-is_featured", "display_order", F("published_on").desc(nulls_last=True))
    )


def stories(request):
    story_list = list(_public_stories())
    hosted = [story for story in story_list if story.is_hosted]
    zimbabwe_stories = [story for story in story_list if story.country.code == PRIORITY_COUNTRY_CODE]
    africa_features = [story for story in hosted if story.country.code != PRIORITY_COUNTRY_CODE]
    africa_links = [
        story
        for story in story_list
        if not story.is_hosted and story.country.code != PRIORITY_COUNTRY_CODE
    ]
    return render(
        request,
        "education/stories.html",
        {
            "stories": story_list,
            "zimbabwe_stories": zimbabwe_stories,
            "africa_features": africa_features,
            "africa_links": africa_links,
            "country_labels": sorted({story.country.name for story in story_list}),
        },
    )


def story_detail(request, slug):
    story = _public_stories().exclude(story_type=CommunityStory.StoryType.EXTERNAL).filter(slug=slug).first()
    if story is None:
        return render(request, "education/story_not_found.html", {"slug": slug}, status=404)
    more_stories = [item for item in _public_stories().exclude(id=story.id) if item.is_hosted][:2]
    return render(
        request,
        "education/story_detail.html",
        {"story": story, "more_stories": more_stories},
    )


def resources(request):
    country = _get_active_country()
    category = request.GET.get("category", "")
    resource_list = (
        LibraryResource.objects.filter(
            country=country,
            is_published=True,
            is_demo=False,
            source_name__gt="",
            source_url__gt="",
        )
        .filter(Q(file__gt="") | Q(external_url__gt=""))
    )
    if category in LibraryResource.Category.values:
        resource_list = resource_list.filter(category=category)
    return render(
        request,
        "education/resources.html",
        {
            "resources": resource_list,
            "categories": LibraryResource.Category.choices,
            "selected_category": category,
        },
    )
