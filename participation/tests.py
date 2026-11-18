import io
import json
import urllib.error
from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from participation.admin import retry_notification
from participation.models import NotificationStatus, PartnershipInquiry, VolunteerInterest
from participation.notifications import notify_new_submission

FAKE_KEY = "re_test_not_a_real_key"
URLOPEN = "participation.notifications.urllib.request.urlopen"

VOLUNTEER_DATA = {
    "volunteer_submit": "1",
    "full_name": "Anna Chikono",
    "email": "anna@example.org",
    "country": "Zimbabwe",
    "role_interest": "Community outreach",
    "availability": "Weekends",
    "motivation": "I want to support young people and improve awareness in my community.",
    "consent_to_contact": "on",
}
PARTNERSHIP_DATA = {
    "partnership_submit": "1",
    "organisation_name": "Muzinda Youth Network",
    "contact_name": "Tapiwa Ndlovu",
    "email": "tapiwa@example.org",
    "country": "Zimbabwe",
    "partnership_type": "Education",
    "message": "We would like to host a youth mental health awareness session for students.",
    "consent_to_contact": "on",
}


def resend_ok(email_id="email_123"):
    response = mock.MagicMock()
    response.read.return_value = json.dumps({"id": email_id}).encode()
    response.__enter__.return_value = response
    return response


def resend_http_error(code=403):
    return urllib.error.HTTPError(
        "https://api.resend.com/emails", code, "Forbidden", hdrs=None, fp=io.BytesIO(b'{"message":"denied"}')
    )


@override_settings(RESEND_API_KEY=FAKE_KEY, NOTIFICATION_EMAIL="staff@example.org")
class SubmissionNotificationTests(TestCase):
    """Resend is always mocked here: no real email is sent and no real key is used."""

    def test_volunteer_submission_sends_one_minimal_notification(self):
        with mock.patch(URLOPEN, return_value=resend_ok("email_abc")) as urlopen:
            response = self.client.post(reverse("get-involved"), VOLUNTEER_DATA)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlopen.call_count, 1)
        api_request = urlopen.call_args.args[0]
        payload = json.loads(api_request.data)
        self.assertEqual(api_request.full_url, "https://api.resend.com/emails")
        self.assertEqual(api_request.get_header("Authorization"), f"Bearer {FAKE_KEY}")
        submission = VolunteerInterest.objects.get()
        self.assertEqual(
            api_request.get_header("Idempotency-key"),
            f"maam-volunteerinterest/{submission.pk}/attempt-1",
        )
        self.assertEqual(payload["to"], ["staff@example.org"])
        self.assertIn("volunteer interest", payload["subject"])
        self.assertIn(str(submission.pk), payload["text"])
        self.assertIn(f"/admin/participation/volunteerinterest/{submission.pk}/change/", payload["text"])
        # Privacy: no personal details or message content in the email.
        for private in ("Anna", "Chikono", "anna@example.org", "support young people", "Weekends"):
            self.assertNotIn(private, json.dumps(payload))

        self.assertEqual(submission.notification_status, NotificationStatus.ACCEPTED)
        self.assertEqual(submission.notification_reference, "email_abc")
        self.assertEqual(submission.notification_attempts, 1)
        follow_up = self.client.get(response.url)
        # The visitor sees the unchanged message, which makes no claim about any email.
        self.assertContains(follow_up, '<div class="success-box">Your volunteer interest has been received.</div>')

    def test_partnership_submission_sends_notification(self):
        with mock.patch(URLOPEN, return_value=resend_ok()) as urlopen:
            self.client.post(reverse("get-involved"), PARTNERSHIP_DATA)
        self.assertEqual(urlopen.call_count, 1)
        payload = json.loads(urlopen.call_args.args[0].data)
        self.assertIn("partnership inquiry", payload["subject"])
        for private in ("Muzinda", "Tapiwa", "tapiwa@example.org", "awareness session"):
            self.assertNotIn(private, json.dumps(payload))
        self.assertEqual(PartnershipInquiry.objects.get().notification_status, NotificationStatus.ACCEPTED)

    def test_rejected_notification_keeps_submission_and_logs_nothing_private(self):
        with mock.patch(URLOPEN, side_effect=resend_http_error(403)), self.assertLogs(
            "participation.notifications", level="WARNING"
        ) as logs:
            response = self.client.post(reverse("get-involved"), VOLUNTEER_DATA, follow=True)

        self.assertContains(response, "Your volunteer interest has been received.")
        submission = VolunteerInterest.objects.get()
        self.assertEqual(submission.notification_status, NotificationStatus.FAILED)
        log_text = "\n".join(logs.output)
        self.assertIn("HTTP 403", log_text)
        self.assertIn(str(submission.pk), log_text)
        for secret in (FAKE_KEY, "Anna", "anna@example.org", "support young people", "denied"):
            self.assertNotIn(secret, log_text)

    def test_network_failure_is_recorded_without_breaking_the_form(self):
        with mock.patch(URLOPEN, side_effect=urllib.error.URLError("offline")), self.assertLogs(
            "participation.notifications", level="WARNING"
        ):
            response = self.client.post(reverse("get-involved"), PARTNERSHIP_DATA, follow=True)
        self.assertContains(response, "Your partnership inquiry has been received.")
        self.assertEqual(PartnershipInquiry.objects.get().notification_status, NotificationStatus.FAILED)

    def test_no_duplicate_notification_for_the_same_submission(self):
        request = RequestFactory().get("/")
        with mock.patch(URLOPEN, return_value=resend_ok()) as urlopen:
            self.client.post(reverse("get-involved"), VOLUNTEER_DATA)
            submission = VolunteerInterest.objects.get()
            self.assertEqual(notify_new_submission(submission, request), NotificationStatus.ACCEPTED)
            fresh = VolunteerInterest.objects.get()
            notify_new_submission(fresh, request)
            notify_new_submission(fresh, request, retry=True)  # retry never resends an accepted one
        self.assertEqual(urlopen.call_count, 1)

    def test_admin_retry_resends_only_failed_notifications(self):
        with mock.patch(URLOPEN, side_effect=resend_http_error(500)), self.assertLogs(
            "participation.notifications", level="WARNING"
        ):
            self.client.post(reverse("get-involved"), VOLUNTEER_DATA)
        failed = VolunteerInterest.objects.get()
        self.assertEqual(failed.notification_status, NotificationStatus.FAILED)

        request = RequestFactory().post("/")
        modeladmin = mock.MagicMock()
        with mock.patch(URLOPEN, return_value=resend_ok("email_retry")) as urlopen:
            retry_notification(modeladmin, request, VolunteerInterest.objects.all())
            retry_notification(modeladmin, request, VolunteerInterest.objects.all())  # second click: no resend
        self.assertEqual(urlopen.call_count, 1)
        self.assertEqual(
            urlopen.call_args.args[0].get_header("Idempotency-key"),
            f"maam-volunteerinterest/{failed.pk}/attempt-2",
        )
        retried = VolunteerInterest.objects.get()
        self.assertEqual(retried.notification_status, NotificationStatus.ACCEPTED)
        self.assertEqual(retried.notification_attempts, 2)


class NotificationsSwitchedOffTests(TestCase):
    @override_settings(RESEND_API_KEY="")
    def test_without_api_key_nothing_is_sent_and_status_says_so(self):
        with mock.patch(URLOPEN) as urlopen:
            response = self.client.post(reverse("get-involved"), VOLUNTEER_DATA, follow=True)
        urlopen.assert_not_called()
        self.assertContains(response, "Your volunteer interest has been received.")
        self.assertEqual(VolunteerInterest.objects.get().notification_status, NotificationStatus.DISABLED)


class AdminSecurityTests(TestCase):
    def test_submissions_are_not_public(self):
        VolunteerInterest.objects.create(
            full_name="Private Person", email="private@example.org", role_interest="x", motivation="y"
        )
        for name in ("admin:participation_volunteerinterest_changelist", "admin:participation_partnershipinquiry_changelist"):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("admin:login"), response["Location"])
        self.assertNotContains(self.client.get(reverse("get-involved")), "Private Person")

    def test_staff_can_review_submissions_and_notification_status(self):
        user = get_user_model().objects.create_superuser("reviewer", "reviewer@example.org", "a-long-test-passphrase-91")
        self.client.force_login(user)
        VolunteerInterest.objects.create(
            full_name="Review Me", email="r@example.org", role_interest="x", motivation="y",
            notification_status=NotificationStatus.FAILED,
        )
        response = self.client.get(reverse("admin:participation_volunteerinterest_changelist"))
        self.assertContains(response, "Review Me")
        self.assertContains(response, "Failed")
        self.assertContains(response, "Retry staff email notification")

    def test_short_passwords_are_rejected(self):
        with self.assertRaises(ValidationError):
            validate_password("Short-pass1")  # 11 characters
        validate_password("a-much-longer-passphrase-2026")


class ParticipationPageTests(TestCase):
    def test_get_involved_page_is_public(self):
        response = self.client.get(reverse("get-involved"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Volunteer")
        self.assertContains(response, "Partnership")

    def test_volunteer_interest_form_saves_data(self):
        response = self.client.post(
            reverse("get-involved"),
            {
                "volunteer_submit": "1",
                "full_name": "Anna Chikono",
                "email": "anna@example.org",
                "country": "Zimbabwe",
                "role_interest": "Community outreach",
                "availability": "Weekends",
                "motivation": "I want to support young people and improve awareness in my community.",
                "consent_to_contact": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(VolunteerInterest.objects.count(), 1)
        self.assertTrue(VolunteerInterest.objects.get().consent_to_contact)
        follow_up = self.client.get(response.url)
        self.assertContains(follow_up, "Your volunteer interest has been received.")

    def test_partnership_inquiry_form_saves_data(self):
        response = self.client.post(
            reverse("get-involved"),
            {
                "partnership_submit": "1",
                "organisation_name": "Muzinda Youth Network",
                "contact_name": "Tapiwa Ndlovu",
                "email": "tapiwa@example.org",
                "country": "Zimbabwe",
                "partnership_type": "Education",
                "message": "We would like to host a youth mental health awareness session for students.",
                "consent_to_contact": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PartnershipInquiry.objects.count(), 1)
        self.assertTrue(PartnershipInquiry.objects.get().consent_to_contact)
        follow_up = self.client.get(response.url)
        self.assertContains(follow_up, "Your partnership inquiry has been received.")

    def test_volunteer_interest_requires_consent(self):
        response = self.client.post(
            reverse("get-involved"),
            {
                "volunteer_submit": "1",
                "full_name": "Anna Chikono",
                "email": "anna@example.org",
                "country": "Zimbabwe",
                "role_interest": "Community outreach",
                "availability": "Weekends",
                "motivation": "I want to support young people and improve awareness in my community.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(VolunteerInterest.objects.count(), 0)
        self.assertContains(response, "Consent is required before you submit this inquiry.")

    def test_partnership_inquiry_requires_consent(self):
        response = self.client.post(
            reverse("get-involved"),
            {
                "partnership_submit": "1",
                "organisation_name": "Muzinda Youth Network",
                "contact_name": "Tapiwa Ndlovu",
                "email": "tapiwa@example.org",
                "country": "Zimbabwe",
                "partnership_type": "Education",
                "message": "We would like to host a youth mental health awareness session for students.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PartnershipInquiry.objects.count(), 0)
        self.assertContains(response, "Consent is required before you submit this inquiry.")

    def test_privacy_and_safeguarding_pages_are_public(self):
        self.assertEqual(self.client.get(reverse("privacy")).status_code, 200)
        self.assertEqual(self.client.get(reverse("safeguarding")).status_code, 200)
