import re
import uuid
from urllib.parse import parse_qs, urlparse

from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from core.models import Country, Language


def build_youtube_embed_url(media_url, load_captions=False):
    """Return a privacy-enhanced YouTube embed URL, or "" for anything else."""
    parsed_url = urlparse(media_url or "")
    if parsed_url.scheme != "https":
        return ""

    hostname = (parsed_url.hostname or "").lower()
    path_parts = parsed_url.path.strip("/").split("/")
    if hostname == "youtu.be":
        video_id = path_parts[0] if path_parts else ""
    elif hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed_url.path == "/watch":
            video_id = parse_qs(parsed_url.query).get("v", [""])[0]
        elif len(path_parts) > 1 and path_parts[0] in {"embed", "shorts", "live"}:
            video_id = path_parts[1]
        else:
            video_id = ""
    else:
        video_id = ""

    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        return ""

    embed_url = f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&playsinline=1"
    if load_captions:
        embed_url += "&cc_load_policy=1"
    return embed_url


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=130, unique=True)
    description = models.TextField(blank=True)
    shona_name = models.CharField(max_length=120, blank=True)
    shona_description = models.TextField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True, related_name="topics")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True, related_name="articles")
    topics = models.ManyToManyField(Topic, related_name="articles", blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    is_demo = models.BooleanField(default=False)
    source_name = models.CharField(max_length=180, blank=True)
    source_url = models.URLField(blank=True)
    cover_image = models.FileField(
        upload_to="article_covers/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])],
    )
    cover_image_url = models.URLField(blank=True)
    cover_image_alt = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["slug"])]

    def clean(self):
        if self.is_published and not self.is_demo and not self.source_url:
            raise ValidationError({"source_url": "Add a credible source before publishing this article."})
        if (self.cover_image or self.cover_image_url) and not self.cover_image_alt:
            raise ValidationError({"cover_image_alt": "Describe the image for readers using assistive technology."})

    def __str__(self):
        return self.title


class ArticleTranslation(models.Model):
    class ReviewStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        REVIEWED = "reviewed", "Reviewed"
        ARCHIVED = "archived", "Archived"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="translations")
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="article_translations")
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    review_status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.DRAFT)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["article", "language"], name="unique_article_language_translation")
        ]
        ordering = ["title"]

    def __str__(self):
        return f"{self.article.title} ({self.language.code})"


class AudioResource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, on_delete=models.PROTECT, related_name="audio_resources")
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="audio_resources")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    audio_url = models.URLField(blank=True)
    download_url = models.URLField(blank=True)
    transcript = models.TextField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class MediaItem(models.Model):
    class MediaType(models.TextChoices):
        VIDEO = "video", "Video"
        DOCUMENTARY = "documentary", "Documentary"
        AUDIO = "audio", "Audio discussion"
        PODCAST = "podcast", "Podcast"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    media_type = models.CharField(max_length=20, choices=MediaType.choices, default=MediaType.VIDEO)
    summary = models.TextField(blank=True)
    media_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=180, blank=True)
    source_url = models.URLField(blank=True)
    thumbnail = models.FileField(
        upload_to="media_thumbnails/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])],
    )
    thumbnail_url = models.URLField(blank=True)
    thumbnail_alt = models.CharField(max_length=240, blank=True)
    captions_url = models.URLField(blank=True)
    transcript = models.TextField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="media_items")
    is_published = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "title"]

    @property
    def youtube_embed_url(self):
        return build_youtube_embed_url(self.media_url, load_captions=bool(self.captions_url))

    def clean(self):
        if self.is_published and not self.media_url:
            raise ValidationError({"media_url": "Add a media link before publishing this item."})
        if self.is_published and (not self.source_name or not self.source_url):
            raise ValidationError("Add the publisher name and source page before publishing this item.")
        if (self.thumbnail or self.thumbnail_url) and not self.thumbnail_alt:
            raise ValidationError({"thumbnail_alt": "Describe the thumbnail for readers using assistive technology."})

    def __str__(self):
        return self.title


class LibraryResource(models.Model):
    class Category(models.TextChoices):
        GUIDE = "guide", "Guide"
        POSTER = "poster", "Poster"
        INFOGRAPHIC = "infographic", "Infographic"
        RESEARCH = "research", "Research summary"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GUIDE)
    summary = models.TextField(blank=True)
    file = models.FileField(
        upload_to="library_resources/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "png", "jpg", "jpeg", "webp"])],
    )
    external_url = models.URLField(blank=True)
    cover_image = models.FileField(
        upload_to="resource_covers/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])],
    )
    cover_image_url = models.URLField(blank=True)
    cover_image_static = models.CharField(
        max_length=200,
        blank=True,
        help_text="Path of an approved image stored in the project's static folder, e.g. images/resources/name.jpg",
    )
    cover_image_alt = models.CharField(max_length=240, blank=True)
    cover_image_credit = models.CharField(
        max_length=240,
        blank=True,
        help_text="Who made or owns the image, e.g. 'Photo: Costa Juta'.",
    )
    cover_image_source_name = models.CharField(max_length=120, blank=True)
    cover_image_source_url = models.URLField(blank=True)
    cover_image_licence_name = models.CharField(max_length=80, blank=True, help_text="For example: CC BY-SA 4.0")
    cover_image_licence_url = models.URLField(blank=True)
    cover_image_country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        help_text=(
            "Country where the photograph was taken. Its flag is shown on the image. "
            "Leave empty for global publications such as WHO or UNICEF covers."
        ),
    )
    cover_image_focus = models.CharField(
        max_length=10,
        choices=[("center", "Centre"), ("top", "Top")],
        default="center",
        help_text="Which part of the image to keep when it is cropped to fit the card.",
    )
    cover_image_rights_notes = models.TextField(
        blank=True,
        help_text="Internal record of the licence or permission check. Not shown publicly.",
    )
    source_name = models.CharField(max_length=180, blank=True)
    source_url = models.URLField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="library_resources")
    is_published = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "title"]

    def clean(self):
        if self.is_published and not (self.file or self.external_url):
            raise ValidationError("Add a file or external link before publishing this resource.")
        if self.is_published and (not self.source_name or not self.source_url):
            raise ValidationError("Add the publisher name and source page before publishing this resource.")
        if self.has_cover_image:
            missing = {
                "cover_image_alt": "Describe the cover image for readers using assistive technology.",
                "cover_image_credit": "Credit the photographer or image owner.",
                "cover_image_licence_name": "Record the licence or permission that allows reuse.",
            }
            errors = {field: message for field, message in missing.items() if not getattr(self, field)}
            if errors:
                raise ValidationError(errors)
        if self.cover_image_country_id and not finders.find(self.cover_image_flag or "-"):
            raise ValidationError(
                {"cover_image_country": "No flag file for this country yet. Add it to static/images/flags/ first."}
            )

    @property
    def has_cover_image(self):
        return bool(self.cover_image or self.cover_image_static or self.cover_image_url)

    @property
    def cover_image_flag(self):
        """Static path of the photo country's flag, e.g. images/flags/zw.svg, or ""."""
        country = self.cover_image_country
        if not (country and self.has_cover_image):
            return ""
        return f"images/flags/{country.code.lower()}.svg"

    def __str__(self):
        return self.title


class CommunityStory(models.Model):
    class StoryType(models.TextChoices):
        COMMUNITY = "community", "Community story shared with MAAM (informed consent required)"
        REPUBLISHED = "republished", "Republished under an open licence (credit required)"
        EXTERNAL = "external", "External link only (no permission to republish)"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    story_type = models.CharField(max_length=20, choices=StoryType.choices, default=StoryType.COMMUNITY)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    excerpt = models.TextField(help_text="A short, factual summary written by MAAM. Do not invent details.")
    body = models.TextField(
        blank=True,
        help_text="Full story text. Leave empty for external links: their text must not be copied.",
    )
    pull_quote = models.CharField(
        max_length=300,
        blank=True,
        help_text="Optional. Must be copied word-for-word from the story text above.",
    )
    content_note = models.TextField(blank=True, help_text="Tell readers about distressing topics before they read.")
    author_display = models.CharField(max_length=120, blank=True)
    author_affiliation = models.CharField(max_length=200, blank=True)
    author_note = models.TextField(blank=True, help_text="Author biography, only as published by the original source.")
    is_anonymous = models.BooleanField(default=True)
    consent_confirmed = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="community_stories")

    original_title = models.CharField(max_length=250, blank=True)
    source_name = models.CharField(max_length=180, blank=True, help_text="Original publisher or publication.")
    source_url = models.URLField(blank=True)
    doi_url = models.URLField(blank=True)
    published_on = models.DateField(null=True, blank=True, help_text="Original publication date.")
    licence_name = models.CharField(max_length=80, blank=True, help_text="For example: CC BY 4.0")
    licence_url = models.URLField(blank=True)
    copyright_notice = models.CharField(max_length=200, blank=True)
    attribution_text = models.TextField(blank=True, help_text="Credit line shown to readers, as the licence requires.")
    changes_note = models.TextField(blank=True, help_text="State whether MAAM changed the original work.")
    permission_notes = models.TextField(
        blank=True,
        help_text="Internal record of licence checks or permission requests. Not shown publicly.",
    )

    image = models.FileField(
        upload_to="story_images/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])],
        help_text="Only upload a photograph you have permission or an open licence to use.",
    )
    image_alt = models.CharField(max_length=240, blank=True)
    image_credit = models.CharField(max_length=240, blank=True, help_text="Photographer, owner and licence.")
    video_url = models.URLField(blank=True, help_text="YouTube link, only where the rights allow embedding.")
    video_credit = models.CharField(max_length=240, blank=True)

    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=100, help_text="Lower numbers appear first.")
    is_demo = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Community stories"

    @property
    def is_hosted(self):
        return self.story_type != self.StoryType.EXTERNAL

    @property
    def video_embed_url(self):
        return build_youtube_embed_url(self.video_url)

    def clean(self):
        errors = {}
        if self.is_published and self.is_demo:
            raise ValidationError("Demonstration stories cannot be published.")

        if self.story_type == self.StoryType.COMMUNITY:
            if self.is_published and not self.consent_confirmed:
                raise ValidationError("A story can only be published after informed consent is confirmed.")
        elif self.story_type == self.StoryType.REPUBLISHED and self.is_published:
            required = {
                "body": "Add the full story text.",
                "author_display": "Credit the author by name.",
                "source_name": "Name the original publisher.",
                "source_url": "Link to the original publication.",
                "licence_name": "Record the open licence.",
                "licence_url": "Link to the licence.",
                "attribution_text": "Add the credit line the licence requires.",
                "changes_note": "State whether MAAM changed the original work.",
            }
            for field, message in required.items():
                if not getattr(self, field):
                    errors[field] = message
        elif self.story_type == self.StoryType.EXTERNAL:
            if self.body:
                errors["body"] = "Do not copy the text of an external story. Link to it instead."
            if self.image:
                errors["image"] = "Do not upload photographs for an external story without permission."
            if self.is_published and not (self.source_name and self.source_url):
                errors["source_url"] = "Add the original publisher and link."

        if self.pull_quote and self.pull_quote not in self.body:
            errors["pull_quote"] = "The pull quote must appear word-for-word in the story text."
        if self.image and not (self.image_alt and self.image_credit):
            errors["image_credit"] = "Add alt text and a credit for the photograph."
        if self.video_url and not self.video_credit:
            errors["video_credit"] = "Credit the video owner."
        if self.video_url and not self.video_embed_url:
            errors["video_url"] = "Use a YouTube link that can be embedded."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title
