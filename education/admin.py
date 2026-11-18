from django.contrib import admin

from .models import (
    Article,
    ArticleTranslation,
    AudioResource,
    CommunityStory,
    LibraryResource,
    MediaItem,
    Topic,
)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "shona_name", "slug", "is_active")
    search_fields = ("name", "shona_name", "slug")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "country", "is_published", "is_demo", "is_featured")
    list_filter = ("is_published", "is_demo", "is_featured", "country")
    search_fields = ("title", "summary")


@admin.register(ArticleTranslation)
class ArticleTranslationAdmin(admin.ModelAdmin):
    list_display = ("article", "language", "review_status", "reviewed_at")
    list_filter = ("review_status", "language")
    search_fields = ("title", "summary", "content", "article__title")


@admin.register(AudioResource)
class AudioResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "is_approved", "is_demo")
    list_filter = ("is_approved", "is_demo", "language")
    search_fields = ("title", "slug")


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "country", "is_published", "is_demo")
    list_filter = ("media_type", "country", "is_published", "is_demo")
    search_fields = ("title", "summary")


@admin.register(LibraryResource)
class LibraryResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "country", "is_published", "is_demo")
    list_filter = ("category", "country", "is_published", "is_demo")
    search_fields = ("title", "summary", "source_name")


@admin.register(CommunityStory)
class CommunityStoryAdmin(admin.ModelAdmin):
    list_display = ("title", "story_type", "country", "licence_name", "consent_confirmed", "is_published", "is_demo")
    list_filter = ("story_type", "country", "consent_confirmed", "is_published", "is_demo")
    search_fields = ("title", "excerpt", "author_display", "source_name")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Story", {"fields": ("story_type", "title", "slug", "country", "excerpt", "body", "pull_quote", "content_note")}),
        (
            "Author",
            {"fields": ("author_display", "is_anonymous", "author_affiliation", "author_note", "consent_confirmed")},
        ),
        (
            "Source, licence and credit",
            {
                "description": (
                    "Republish text only under an open licence or with written permission. "
                    "For external links, leave the story text empty."
                ),
                "fields": (
                    "original_title",
                    "source_name",
                    "source_url",
                    "doi_url",
                    "published_on",
                    "licence_name",
                    "licence_url",
                    "copyright_notice",
                    "attribution_text",
                    "changes_note",
                    "permission_notes",
                ),
            },
        ),
        (
            "Photograph and video (only where rights allow)",
            {"fields": ("image", "image_alt", "image_credit", "video_url", "video_credit")},
        ),
        ("Publishing", {"fields": ("is_featured", "display_order", "is_published", "is_demo")}),
    )
