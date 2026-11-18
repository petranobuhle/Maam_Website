from django.test import TestCase
from django.urls import resolve, reverse


class PublicPageTests(TestCase):
    def test_primary_pages_render(self):
        names = [
            "home",
            "about",
            "learn",
            "listen",
            "watch-listen",
            "stories",
            "resources",
            "support",
            "insights",
            "privacy",
            "safeguarding",
            "contact",
            "get-involved",
        ]
        for name in names:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_about_page_explains_identity_and_shared_responsibility(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        for content in (
            "Mwana Asingachemi Anofira Mumbereko",
            "The baby that does not cry will die in the cradle.",
            "MAAM is a youth-led mental health awareness and advocacy initiative",
            "the responsibility is not on a person to find perfect words",
            "listen, respond with compassion",
            "MAAM Project Lead",
            "MAAM is still being developed",
            "not a counselling centre, mental health clinic or healthcare provider",
        ):
            with self.subTest(content=content):
                self.assertContains(response, content)

    def test_about_page_includes_mission_values_workstreams_and_internal_links(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        for content in (
            "Promote mental health awareness, challenge stigma",
            "Communities where mental health is understood",
            "Compassion",
            "Dignity",
            "Inclusion",
            "Awareness",
            "Empowerment",
            "Accountability",
            "Increase mental health literacy and awareness.",
            "Promote responsible storytelling, consent and privacy.",
            "Education and awareness",
            "Community voices",
            "Campaigns and advocacy",
            "Credible resources",
            "Support directory",
            "Participation and partnerships",
        ):
            with self.subTest(content=content):
                self.assertContains(response, content)
        for name in ("learn", "support", "get-involved"):
            with self.subTest(link=name):
                self.assertContains(response, f'href="{reverse(name)}"')

    def test_about_page_uses_supplied_highfield_photo(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="/static/images/about-highfield-harare-dawn.jpg"')
        self.assertContains(response, 'alt="A view of Highfield, Harare, Zimbabwe, at dawn."')
        self.assertContains(response, "Highfield, Harare, Zimbabwe.")
        # CC BY-SA 4.0 credit for the Wikimedia Commons photo by Achitate.
        self.assertContains(response, "Photo: Achitate")
        self.assertContains(response, 'href="https://creativecommons.org/licenses/by-sa/4.0/"')
        self.assertContains(response, "https://commons.wikimedia.org/wiki/File:Dawn_in_Highfield_Harare_2.jpg")
        self.assertNotContains(response, "about-photo-placeholder")
        self.assertNotContains(response, "about-youth-workshop.jpg")
        self.assertNotContains(response, "Beletweyne")
        self.assertNotContains(response, "Presentation image placeholder")
        self.assertNotContains(response, 'class="visual-note"')

    def test_support_and_stories_routes_use_their_content_views(self):
        self.assertEqual(resolve("/support/").func.__module__, "directory.views")
        self.assertEqual(resolve("/stories/").func.__module__, "education.views")

    def test_privacy_page_explains_current_collection_and_contact_options(self):
        response = self.client.get(reverse("privacy"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Volunteer form")
        self.assertContains(response, "Partnership form")
        self.assertContains(response, "There is no active public survey")
        self.assertContains(response, "No automatic deletion process is configured")
        self.assertContains(response, 'href="mailto:mahwadupetra@gmail.com')
        self.assertContains(response, reverse("safeguarding"))
        self.assertContains(response, reverse("get-involved"))

    def test_safeguarding_page_explains_boundaries_and_contact_options(self):
        response = self.client.get(reverse("safeguarding"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "listening without judgement")
        self.assertContains(response, "You are not required to disclose")
        self.assertContains(response, "not monitored for urgent requests")
        self.assertContains(response, "named safeguarding lead")
        self.assertContains(response, 'href="mailto:mahwadupetra@gmail.com')
        self.assertContains(response, reverse("privacy"))
        self.assertContains(response, reverse("get-involved"))

    def test_contact_page_uses_current_email_address(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "mahwadupetra@gmail.com")
        self.assertContains(response, 'href="mailto:mahwadupetra@gmail.com"')

    def test_homepage_uses_original_art_and_clear_paths_without_placeholders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="/static/images/homepage-maam-hero.jpg"')
        self.assertContains(
            response,
            'alt="A caregiver listens closely as a child in a cradle reaches toward her, showing the child being heard and supported."',
        )
        self.assertContains(response, "Listening is a shared responsibility.")
        self.assertContains(response, "not a reason to blame anyone who finds speaking difficult")
        for name in ("learn", "support", "get-involved"):
            with self.subTest(link=name):
                self.assertContains(response, f'href="{reverse(name)}"')
        self.assertNotContains(response, "replace with consented, licensed community photography")
        self.assertNotContains(response, "No verified MAAM figures published yet")
        self.assertNotContains(response, "Presentation image placeholder")
