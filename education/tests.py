from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from core.models import Country
from .models import Article, ArticleTranslation, CommunityStory, LibraryResource, MediaItem, Topic


class EducationPageTests(TestCase):
    def test_library_pages_render_with_empty_states(self):
        for name in ("learn", "listen", "watch-listen", "stories", "resources"):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_resources_require_a_source_and_real_published_material(self):
        country = Country.objects.get(code="ZW")
        LibraryResource.objects.create(
            title="Verified resource",
            slug="verified-resource-test",
            category=LibraryResource.Category.GUIDE,
            summary="A real resource with a publisher and source link.",
            external_url="https://example.org/verified-resource",
            source_name="Example publisher",
            source_url="https://example.org/verified-resource",
            country=country,
            is_published=True,
        )
        LibraryResource.objects.create(
            title="Demo resource",
            slug="demo-resource-test",
            external_url="https://example.org/demo-resource",
            source_name="Example publisher",
            source_url="https://example.org/demo-resource",
            country=country,
            is_published=True,
            is_demo=True,
        )
        LibraryResource.objects.create(
            title="Unsourced resource",
            slug="unsourced-resource-test",
            external_url="https://example.org/unsourced-resource",
            country=country,
            is_published=True,
        )

        response = self.client.get(reverse("resources"))

        self.assertContains(response, "Verified resource")
        self.assertNotContains(response, "Demo resource")
        self.assertNotContains(response, "Unsourced resource")
        self.assertContains(response, "Friendship Bench publications")

    def test_watch_page_embeds_only_published_sourced_media(self):
        country = Country.objects.get(code="ZW")
        MediaItem.objects.create(
            title="Demo video",
            slug="demo-video-test",
            media_url="https://www.youtube.com/watch?v=HMRaun9yRWk",
            source_name="World Health Organization",
            source_url="https://www.who.int/",
            country=country,
            is_published=True,
            is_demo=True,
        )
        MediaItem.objects.create(
            title="Unsourced video",
            slug="unsourced-video-test",
            media_url="https://www.youtube.com/watch?v=HMRaun9yRWk",
            country=country,
            is_published=True,
        )

        response = self.client.get(reverse("watch-listen"))

        self.assertContains(response, "Mental health in adolescence")
        self.assertContains(response, "How to support young people")
        self.assertContains(response, "https://www.youtube-nocookie.com/embed/HMRaun9yRWk")
        self.assertContains(response, "A caption track was not listed")
        self.assertNotContains(response, "Demo video")
        self.assertNotContains(response, "Unsourced video")
        self.assertNotContains(response, "autoplay")

    def test_youtube_embed_rejects_untrusted_hosts_and_malformed_ids(self):
        untrusted_host = MediaItem(media_url="https://youtube.com.example.org/watch?v=HMRaun9yRWk")
        malformed_id = MediaItem(media_url="https://www.youtube.com/watch?v=short")

        self.assertEqual(untrusted_host.youtube_embed_url, "")
        self.assertEqual(malformed_id.youtube_embed_url, "")

    def test_public_stories_require_consent_and_manual_publication(self):
        country = Country.objects.get(code="ZW")
        CommunityStory.objects.create(
            title="Approved story",
            slug="approved-story-test",
            excerpt="Published with consent.",
            body="The approved story.",
            country=country,
            is_published=True,
            consent_confirmed=True,
        )
        CommunityStory.objects.create(
            title="Unconsented story",
            slug="unconsented-story-test",
            excerpt="Not approved.",
            body="Not approved.",
            country=country,
            is_published=True,
        )
        CommunityStory.objects.create(
            title="Demo story",
            slug="demo-story-test",
            excerpt="A demonstration.",
            body="A demonstration.",
            country=country,
            is_published=True,
            is_demo=True,
            consent_confirmed=True,
        )

        response = self.client.get(reverse("stories"))

        self.assertContains(response, "Approved story")
        self.assertNotContains(response, "Unconsented story")
        self.assertNotContains(response, "Demo story")
        self.assertContains(response, "manual approval for publication")
        self.assertNotContains(response, "<form")

    def test_admin_requires_authentication(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)

    def test_demo_articles_are_explicitly_labelled(self):
        country = Country.objects.get(code="ZW")
        Article.objects.create(
            title="Demo article",
            slug="demo-article-test",
            country=country,
            is_published=True,
            is_demo=True,
        )
        response = self.client.get(reverse("learn"))
        self.assertContains(response, "Demonstration")
        self.assertContains(response, "review needed")

    def test_every_learning_topic_links_to_a_sourced_article(self):
        response = self.client.get(reverse("learn"))
        topic_slugs = (
            "understanding-mental-health",
            "stress",
            "anxiety",
            "depression",
            "mental-health-stigma",
            "supporting-a-friend",
            "seeking-professional-help",
        )
        self.assertEqual(response.content.count(b"topic-card--link"), len(topic_slugs))

        for topic_slug in topic_slugs:
            with self.subTest(topic=topic_slug):
                topic = Topic.objects.get(slug=topic_slug, is_active=True)
                article = topic.articles.filter(
                    is_published=True,
                    is_demo=False,
                    source_url__gt="",
                ).first()
                self.assertIsNotNone(article)
                self.assertContains(response, topic.name)
                article_url = reverse("article-detail", args=[article.slug])
                self.assertContains(
                    response,
                    f'class="topic-card topic-card--link" href="{article_url}?lang=en"',
                )
                self.assertContains(response, article_url)

                detail = self.client.get(article_url)
                self.assertEqual(detail.status_code, 200)
                self.assertContains(detail, article.source_name)
                self.assertContains(detail, f'href="{article.source_url}"')
                self.assertContains(detail, reverse("support"))

    def test_education_defaults_to_english_and_offers_only_english_and_shona(self):
        response = self.client.get(reverse("learn"))
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, 'href="?lang=en"')
        self.assertContains(response, 'href="?lang=sn"')
        self.assertContains(response, "Understand mental health.")

        shona_response = self.client.get(f"{reverse('learn')}?lang=sn")
        self.assertContains(shona_response, '<html lang="sn">')
        self.assertContains(shona_response, "Nzwisisa utano hwepfungwa.")
        self.assertContains(shona_response, "Kunzwisisa utano hwepfungwa")
        self.assertContains(shona_response, "Kuzvidya mwoyo")
        self.assertContains(shona_response, "Dhairekitori reRubatsiro")
        self.assertContains(shona_response, "Shanduro dzeShona hadzisati dzapera")
        self.assertNotContains(shona_response, 'href="?lang=rw"')
        self.assertContains(shona_response, "/learn/understanding-anxiety/?lang=sn")
        for topic in Topic.objects.filter(is_active=True):
            with self.subTest(topic=topic.slug):
                self.assertContains(shona_response, topic.shona_name)

        for translation in ArticleTranslation.objects.filter(
            article__is_published=True,
            article__is_demo=False,
            language__code="sn",
        ).select_related("article"):
            with self.subTest(article=translation.article.slug):
                article_response = self.client.get(
                    f"{reverse('article-detail', args=[translation.article.slug])}?lang=sn"
                )
                self.assertEqual(article_response.status_code, 200)
                self.assertContains(article_response, translation.title)
                self.assertContains(article_response, translation.content.split("\n\n")[0])

        unsupported_language = self.client.get(f"{reverse('learn')}?lang=rw")
        self.assertContains(unsupported_language, '<html lang="en">')
        self.assertContains(unsupported_language, "Understand mental health.")

    def test_shona_article_translations_are_editable_drafts_and_keep_language(self):
        articles = Article.objects.filter(is_published=True, is_demo=False)
        translations = ArticleTranslation.objects.filter(
            article__in=articles,
            language__code="sn",
        )
        self.assertEqual(translations.count(), 7)
        self.assertEqual(translations.filter(review_status="draft", reviewed_at__isnull=True).count(), 7)
        self.assertEqual(Topic.objects.filter(is_active=True).exclude(shona_name="").count(), 7)

        article = Article.objects.get(slug="understanding-anxiety")
        translation = translations.get(article=article)
        detail = self.client.get(f"{reverse('article-detail', args=[article.slug])}?lang=sn")
        self.assertContains(detail, '<html lang="sn">')
        self.assertContains(detail, translation.title)
        self.assertContains(detail, "Kuzvidya mwoyo usati wanyora bvunzo")
        self.assertContains(detail, "Shanduro yeShona iyi idrafti")
        self.assertContains(detail, 'href="?lang=en"')
        self.assertContains(detail, 'href="?lang=sn"')
        self.assertContains(detail, "?lang=sn")

        english_detail = self.client.get(reverse("article-detail", args=[article.slug]))
        self.assertContains(english_detail, '<html lang="en">')
        self.assertContains(english_detail, article.title)
        self.assertNotContains(english_detail, translation.title)

    def test_story_cannot_be_published_without_consent(self):
        country = Country.objects.get(code="ZW")
        story = CommunityStory(
            title="Unpublished draft",
            slug="unpublished-draft-test",
            excerpt="Draft excerpt",
            body="Draft story",
            country=country,
            is_published=True,
            consent_confirmed=False,
        )
        with self.assertRaises(ValidationError):
            story.full_clean()


class ShonaCorrectionTests(TestCase):
    """Batch 4 Shona corrections (migration 0015). English text must stay unchanged."""

    def test_agreed_anxiety_correction_is_shown(self):
        response = self.client.get(reverse("article-detail", args=["understanding-anxiety"]), {"lang": "sn"})
        # The sentence follows a semicolon in the article, so it starts with a lowercase "z".
        self.assertContains(
            response, "zviratidzo izvi hazvigoni kushandiswa kuona kuti iwe kana mumwe munhu ane chirwere chipi."
        )
        self.assertNotContains(response, "hazvigoni kukupa kana mumwe munhu chirwere")
        self.assertContains(response, "kutadza kuisa pfungwa pachinhu")
        # The draft notice is still shown to readers.
        self.assertContains(response, 'class="education-translation-notice"')

    def test_other_meaning_errors_are_corrected(self):
        expectations = {
            "mental-health-stigma": ("kuti atendwe kana kubatwa", "kuti atenderwe"),
            "supporting-a-friend-who-is-struggling": ("tsvaga nguva yamuri moga", "nguva yakavanzika"),
            "understanding-depression": ("kugona kuisa pfungwa pachinhu", "kugona kutarisa"),
            "understanding-mental-health": ("kuhupesvedzera", "kuuhwandisa"),
        }
        for slug, (fixed, old) in expectations.items():
            with self.subTest(article=slug):
                response = self.client.get(reverse("article-detail", args=[slug]), {"lang": "sn"})
                self.assertContains(response, fixed)
                self.assertNotContains(response, old)

    def test_all_seven_shona_translations_stay_visible_and_marked_draft(self):
        translations = ArticleTranslation.objects.filter(language__code="sn")
        self.assertEqual(translations.count(), 7)
        self.assertFalse(translations.exclude(review_status=ArticleTranslation.ReviewStatus.DRAFT).exists())

    def test_english_articles_are_unchanged(self):
        response = self.client.get(reverse("article-detail", args=["understanding-anxiety"]))
        self.assertContains(response, "a list of signs cannot diagnose you or someone else.")
        self.assertNotContains(response, "zviratidzo izvi")

    def test_stigma_topic_description_corrected(self):
        topic = Topic.objects.get(slug="mental-health-stigma")
        self.assertIn("kusarurwa", topic.shona_description)
        self.assertNotIn("kusarudzwa", topic.shona_description)


class ResourceImageTests(TestCase):
    def test_licensed_photos_show_with_alt_text_and_credit(self):
        response = self.client.get(reverse("resources"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/static/images/resources/friendship-bench-harare-costa-juta.jpg")
        self.assertContains(response, 'alt="A Friendship Bench grandmother holding a clipboard')
        self.assertContains(response, "Photo: Costa Juta")
        self.assertContains(response, 'href="https://creativecommons.org/licenses/by-sa/4.0/"')
        self.assertContains(response, "/static/images/resources/who-doing-what-matters-cover.jpg")
        self.assertContains(response, "resource-card__photo--top")
        self.assertContains(response, "CC BY-NC-SA 3.0 IGO")

    def test_no_placeholder_icons_or_unlicensed_images(self):
        response = self.client.get(reverse("resources"))
        for leftover in ("photo-placeholder", "resource-art", "<svg"):
            self.assertNotContains(response, leftover)
        # Exactly the two resources with confirmed image rights have a photograph.
        self.assertContains(response, 'class="resource-card__media"', count=2)

    def test_resource_image_requires_alt_credit_and_licence(self):
        resource = LibraryResource.objects.get(slug="unicef-state-world-children-2021")
        resource.cover_image_static = "images/resources/example.jpg"
        with self.assertRaises(ValidationError) as caught:
            resource.full_clean()
        for field in ("cover_image_alt", "cover_image_credit", "cover_image_licence_name"):
            self.assertIn(field, caught.exception.message_dict)

    def test_zimbabwe_flag_shows_only_on_photo_taken_in_zimbabwe(self):
        response = self.client.get(reverse("resources"))
        self.assertContains(response, "/static/images/flags/zw.svg", count=1)
        self.assertContains(response, '<span class="visually-hidden">Photo taken in </span>Zimbabwe')
        who = LibraryResource.objects.get(slug="who-doing-what-matters-times-stress")
        self.assertEqual(who.cover_image_flag, "")

    def test_photo_country_needs_a_flag_file(self):
        resource = LibraryResource.objects.get(slug="friendship-bench-publications")
        resource.cover_image_country = Country.objects.get(code="UG")
        with self.assertRaises(ValidationError) as caught:
            resource.full_clean()
        self.assertIn("cover_image_country", caught.exception.message_dict)

    def test_filtered_resources_still_show_photos(self):
        response = self.client.get(reverse("resources"), {"category": "guide"})
        self.assertContains(response, "who-doing-what-matters-cover.jpg")
        self.assertNotContains(response, "friendship-bench-harare-costa-juta.jpg")


class DocumentaryStoriesTests(TestCase):
    """Seeded open-licence stories, credit rules and Zimbabwe-first ordering."""

    def test_stories_page_title_and_seeded_stories(self):
        response = self.client.get(reverse("stories"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beyond the Silence: <span>Real Voices. Real Experiences.</span>")
        self.assertContains(response, "My bipolar odyssey")
        self.assertContains(response, "Samukelisiwe J. Ngcobo")
        self.assertContains(response, "Life beyond diagnosis: My journey of hope")
        self.assertContains(response, "Edward Nkurunungi")
        self.assertContains(response, "Republished with credit · CC BY 4.0")
        self.assertContains(response, "MAAM did not interview these writers")
        self.assertContains(response, "South Africa")
        self.assertContains(response, "Uganda")

    def test_zimbabwe_section_comes_first_and_external_stories_link_out(self):
        response = self.client.get(reverse("stories"))
        content = response.content.decode()
        self.assertLess(content.index("Voices from Zimbabwe"), content.index("Selected stories from the continent"))
        self.assertLess(content.index("Mental health is everyone"), content.index("My bipolar odyssey"))
        self.assertContains(response, 'href="https://www.unicef.org/zimbabwe/stories/mental-health-everyones-business"')
        self.assertContains(response, "On the original website")
        external = CommunityStory.objects.get(slug="unicef-zimbabwe-mental-health-everyones-business")
        self.assertEqual(external.body, "")
        self.assertEqual(
            self.client.get(reverse("story-detail", args=[external.slug])).status_code,
            404,
        )

    def test_republished_story_shows_full_text_credit_licence_and_content_note(self):
        response = self.client.get(reverse("story-detail", args=["my-bipolar-odyssey"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I am a doctor. I am also a patient")
        self.assertContains(response, "I am thriving despite it.")
        self.assertContains(response, "https://doi.org/10.4102/sajpsychiatry.v30i0.2339")
        self.assertContains(response, 'href="https://creativecommons.org/licenses/by/4.0/"')
        self.assertContains(response, "© 2024. The Author. Licensee: AOSIS.")
        self.assertContains(response, "Content note:")
        self.assertContains(response, "<strong>Changes:</strong>")
        self.assertContains(response, "MAAM did not interview the author")
        self.assertNotContains(response, "permission_notes")
        self.assertNotContains(response, "Licence checked on the publisher")

        uganda = self.client.get(reverse("story-detail", args=["life-beyond-diagnosis"]))
        self.assertContains(uganda, "There is more to a human being than a diagnosis.")
        self.assertContains(uganda, "Department of Administration, Peer Nation, Kampala, Uganda")

    def test_new_countries_do_not_become_the_active_country(self):
        self.assertFalse(Country.objects.get(code="ZA").is_active)
        self.assertFalse(Country.objects.get(code="UG").is_active)
        self.assertEqual(list(Country.objects.filter(is_active=True).values_list("code", flat=True)), ["ZW"])

    def test_republished_story_requires_licence_and_credit(self):
        story = CommunityStory(
            story_type=CommunityStory.StoryType.REPUBLISHED,
            title="Missing credit",
            slug="missing-credit-test",
            excerpt="Summary",
            body="Story text",
            country=Country.objects.get(code="ZW"),
            is_published=True,
        )
        with self.assertRaises(ValidationError) as caught:
            story.full_clean()
        for field in ("licence_name", "licence_url", "attribution_text", "source_url", "author_display"):
            self.assertIn(field, caught.exception.message_dict)

    def test_external_story_cannot_store_copied_text(self):
        story = CommunityStory(
            story_type=CommunityStory.StoryType.EXTERNAL,
            title="Copied",
            slug="copied-test",
            excerpt="Summary",
            body="Copied text from another website",
            source_name="Publisher",
            source_url="https://example.org/story",
            country=Country.objects.get(code="ZW"),
            is_published=True,
        )
        with self.assertRaises(ValidationError) as caught:
            story.full_clean()
        self.assertIn("body", caught.exception.message_dict)

    def test_pull_quote_must_be_word_for_word_and_media_needs_credit(self):
        story = CommunityStory.objects.get(slug="life-beyond-diagnosis")
        story.pull_quote = "A quote the author never wrote."
        story.video_url = "https://www.youtube.com/watch?v=HMRaun9yRWk"
        with self.assertRaises(ValidationError) as caught:
            story.full_clean()
        self.assertIn("pull_quote", caught.exception.message_dict)
        self.assertIn("video_credit", caught.exception.message_dict)

    def test_unpublished_or_demo_stories_are_hidden(self):
        CommunityStory.objects.filter(slug="my-bipolar-odyssey").update(is_published=False)
        CommunityStory.objects.filter(slug="life-beyond-diagnosis").update(is_demo=True)
        response = self.client.get(reverse("stories"))
        self.assertNotContains(response, "My bipolar odyssey")
        self.assertNotContains(response, "Life beyond diagnosis")
        self.assertEqual(self.client.get(reverse("story-detail", args=["my-bipolar-odyssey"])).status_code, 404)
