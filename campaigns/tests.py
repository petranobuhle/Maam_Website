from django.contrib import admin
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from core.models import Country
from .models import Campaign


class CampaignRemovalTests(TestCase):
    """The public Campaigns page is retired; campaign records stay in the admin."""

    def setUp(self):
        self.country = Country.objects.get(code="ZW")
        self.campaign = Campaign.objects.create(
            title="Community listening workshop",
            slug="community-listening-workshop-test",
            summary="A test campaign.",
            country=self.country,
            is_active=True,
        )

    def test_public_campaign_routes_are_removed(self):
        self.assertEqual(self.client.get("/campaigns/").status_code, 404)
        self.assertEqual(self.client.get(f"/campaigns/{self.campaign.slug}/").status_code, 404)
        with self.assertRaises(NoReverseMatch):
            reverse("campaigns")

    def test_navigation_no_longer_links_to_campaigns(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, 'href="/campaigns/"')
        self.assertNotContains(response, ">Campaigns</a>")

    def test_campaign_data_is_kept_and_manageable_in_admin(self):
        self.assertTrue(Campaign.objects.filter(slug=self.campaign.slug).exists())
        self.assertIn(Campaign, admin.site._registry)
