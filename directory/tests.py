from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import Country
from .models import Organisation, SupportService


class SupportDirectoryTests(TestCase):
    def setUp(self):
        self.country, _ = Country.objects.get_or_create(
            code="ZW",
            defaults={"name": "Zimbabwe", "is_active": True},
        )
        self.country.is_active = True
        self.country.save(update_fields=["is_active"])

    def create_listing(self, *, verified):
        organisation = Organisation.objects.create(
            name="Community Health Centre",
            slug=f"community-health-centre-{verified}",
            country=self.country,
            is_verified=verified,
            verification_status="verified" if verified else "pending",
            verification_source="https://health.example.test/organisation" if verified else "",
            last_verified_at=timezone.now() if verified else None,
        )
        service = SupportService.objects.create(
            organisation=organisation,
            country=self.country,
            name=f"Wellbeing information {verified}",
            service_type="Information",
            is_verified=verified,
            verification_status="verified" if verified else "pending",
            verification_source="https://health.example.test/service" if verified else "",
            last_verified_at=timezone.now() if verified else None,
            is_active=True,
        )
        return organisation, service

    def test_directory_shows_only_fully_verified_non_demo_services(self):
        _, verified = self.create_listing(verified=True)
        _, pending = self.create_listing(verified=False)
        response = self.client.get(reverse("support"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, verified.name)
        self.assertNotContains(response, pending.name)

    def test_search_filters_verified_services(self):
        _, listing = self.create_listing(verified=True)
        response = self.client.get(reverse("support"), {"q": "Wellbeing"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, listing.name)
        self.assertContains(self.client.get(reverse("support"), {"q": "not-a-service"}), "No verified listings")

    def test_existing_sample_listing_is_not_marked_verified(self):
        organisation = Organisation.objects.get(slug="harare-youth-wellbeing-network")
        service = organisation.services.get(name="Youth wellbeing information line")
        self.assertTrue(organisation.is_demo)
        self.assertFalse(organisation.is_verified)
        self.assertEqual(organisation.verification_status, "pending")
        self.assertTrue(service.is_demo)
        self.assertFalse(service.is_verified)
        self.assertFalse(service.is_active)
        self.assertEqual(service.verification_status, "pending")
        response = self.client.get(reverse("support"))
        self.assertNotContains(response, organisation.name)

    def test_verified_directory_listings_show_sources_and_access_modes(self):
        response = self.client.get(reverse("support"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Friendship Bench Zimbabwe")
        self.assertContains(response, "Zimbabwe National Association for Mental Health (ZIMNAMH)")
        self.assertContains(response, "Online")
        self.assertContains(response, "Community-based")
        self.assertContains(response, "MAAM Project Lead")
        self.assertContains(response, "Official website reviewed")
        self.assertContains(response, 'href="https://www.friendshipbenchzimbabwe.org/online"')
        self.assertContains(response, 'href="https://zimnamh.org.zw/"')

    def test_directory_groups_services_under_one_card_per_organisation(self):
        response = self.client.get(reverse("support"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["organisations"]), 10)
        self.assertEqual(
            response.content.decode().count('class="feature-card directory-card"'),
            10,
        )
        self.assertEqual(
            response.content.decode().count(
                "Zimbabwe National Association for Mental Health (ZIMNAMH)"
            ),
            1,
        )
        self.assertContains(response, "Rehabilitation and disability support")
        self.assertContains(response, "FreshStart Mental Health Support Organisation")

    def test_directory_search_covers_country_organisations_services_and_locations(self):
        expected_slugs = {
            "Zimbabwe": "friendship-bench-zimbabwe",
            "ZIMNAMH": "zimbabwe-national-association-for-mental-health",
            "Friendship Bench": "friendship-bench-zimbabwe",
            "Harare": "connect-zimbabwe-institute-of-systemic-therapy",
            "Rehabilitation": "zimbabwe-national-association-for-mental-health",
            "Advocacy": "zimbabwe-national-association-for-mental-health",
            "FreshStart": "freshstart-mental-health-support-organisation",
            "CONNECT-ZIST": "connect-zimbabwe-institute-of-systemic-therapy",
        }
        for query, expected_slug in expected_slugs.items():
            with self.subTest(query=query):
                response = self.client.get(reverse("support"), {"q": query})
                self.assertEqual(response.status_code, 200)
                self.assertIn(
                    expected_slug,
                    {organisation.slug for organisation in response.context["organisations"]},
                )
                self.assertNotContains(response, "Harare Youth Wellbeing Network")

    def test_added_organisation_details_include_source_and_available_contact_links(self):
        listings = {
            "freshstart-mental-health-support-organisation": {
                "source": "https://freshstartngo.org/contact.html",
                "phones": ("+263788995400", "+263713403415"),
                "email": None,
            },
            "happy-nest-counselling-chambers": {
                "source": "https://www.hncc.org.zw/contact/",
                "phones": ("+263777757958",),
                "email": "admin@hncc.org.zw",
            },
            "anxiety-support-and-awareness-centre": {
                "source": "https://asactrust.co.zw/get-help/",
                "phones": ("+263719555772",),
                "email": "asactrust.org@gmail.com",
            },
            "connect-zimbabwe-institute-of-systemic-therapy": {
                "source": "https://connect.org.zw/contact/",
                "phones": (
                    "+263242741719",
                    "+263242741779",
                    "+263242741726",
                    "+263242741794",
                ),
                "email": "admin@connect.org.zw",
            },
            "phoebe-centre-zimbabwe": {
                "source": "https://phoebecentre.org/contact-us/",
                "phones": ("+263242448060", "+263716586831", "+263779651691"),
                "email": "adminzim@phoebecentre.org.uk",
            },
            "ndinewe-foundation": {
                "source": "https://ndinewe.org/about-us",
                "phones": ("+263781293888",),
                "email": "info@ndinewe.org",
            },
            "tree-of-life-trust-zimbabwe": {
                "source": "https://www.treeoflifezimbabwe.org/node/59",
                "phones": (),
                "email": None,
            },
            "contact-family-counselling-centre": {
                "source": "https://contactfcc.co.zw/",
                "phones": ("+263292272400", "+263292881842"),
                "email": "contact@contactfcc.co.zw",
            },
        }
        for slug, details in listings.items():
            with self.subTest(organisation=slug):
                organisation = Organisation.objects.get(slug=slug)
                response = self.client.get(
                    reverse("support-detail", args=[organisation.id])
                )
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, organisation.name)
                self.assertContains(response, f'href="{details["source"]}"')
                self.assertContains(response, 'href="https://')
                for phone in details["phones"]:
                    self.assertContains(response, f'href="tel:{phone}"')
                if details["email"]:
                    self.assertContains(
                        response,
                        f'href="mailto:{details["email"]}"',
                    )

    def test_friendship_bench_details_include_verified_contact_and_service_information(self):
        organisation = Organisation.objects.get(slug="friendship-bench-zimbabwe")
        response = self.client.get(reverse("support-detail", args=[organisation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="tel:+263784845294"')
        self.assertContains(response, 'href="https://wa.me/263784845294"')
        self.assertContains(response, 'href="https://www.friendshipbenchzimbabwe.org/online"')
        self.assertContains(response, "English, Shona and Ndebele")
        self.assertContains(response, "Monday–Friday, 9am–4pm; Saturday, 9am–12pm")
        self.assertContains(response, "17 November 2026")
        self.assertContains(response, "Official website reviewed")
        self.assertContains(response, "does not imply that MAAM and this organisation have partnered")

    def test_zimnamh_details_include_official_contact_and_distinct_service_types(self):
        organisation = Organisation.objects.get(slug="zimbabwe-national-association-for-mental-health")
        response = self.client.get(reverse("support-detail", args=[organisation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="tel:+263772571075"')
        self.assertContains(response, 'href="mailto:info@zimnamh.org.zw"')
        self.assertContains(response, 'href="https://zimnamh.org.zw/"')
        self.assertContains(response, "Sotherton, Harare, Zimbabwe")
        self.assertContains(response, "Mental health advocacy and education")
        self.assertContains(response, "Rehabilitation and disability support")
        self.assertContains(response, "Not stated by organisation")
        self.assertContains(response, 'href="https://zimnamh.org.zw/contact.html"')

    def test_listing_cannot_be_verified_without_an_official_source_and_date(self):
        organisation, _ = self.create_listing(verified=False)
        organisation.is_verified = True
        organisation.verification_status = "verified"
        with self.assertRaises(ValidationError):
            organisation.full_clean()
