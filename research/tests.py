from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Country, Language
from research.models import Survey, SurveyAnswer, SurveyQuestion, SurveyResponse


class SurveyWorkflowTests(TestCase):
    def setUp(self):
        self.country, _ = Country.objects.get_or_create(
            code="ZW",
            defaults={"name": "Zimbabwe", "official_name": "Republic of Zimbabwe", "is_active": True},
        )
        self.country.is_active = True
        self.country.save(update_fields=["is_active"])
        self.language, _ = Language.objects.get_or_create(
            code="en",
            defaults={"name": "English", "native_name": "English", "is_active": True},
        )
        self.survey = Survey.objects.create(
            title="Youth awareness survey",
            slug="youth-awareness-survey",
            description="A voluntary anonymous survey for understanding community awareness and support-seeking.",
            country=self.country,
            language=self.language,
            is_active=True,
        )
        self.text_question = SurveyQuestion.objects.create(
            survey=self.survey,
            question_text="What helps you feel supported in your community?",
            question_type="text",
            is_required=True,
            order=1,
        )
        self.choice_question = SurveyQuestion.objects.create(
            survey=self.survey,
            question_text="Which response best describes your current situation?",
            question_type="choice",
            choices=["I feel okay", "I feel stressed", "I need support"],
            is_required=True,
            order=2,
        )

    def test_insights_page_is_public(self):
        response = self.client.get(reverse("insights"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Insights, shared responsibly")
        self.assertContains(response, "not enough responses")

    def test_survey_requires_consent_and_age_group(self):
        response = self.client.post(
            reverse("survey-detail", args=[self.survey.id]),
            {
                f"question_{self.text_question.id}": "I feel supported by my friends.",
                f"question_{self.choice_question.id}": "I feel stressed",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "consent")
        self.assertEqual(SurveyResponse.objects.count(), 0)

    def test_survey_submission_creates_anonymous_response(self):
        response = self.client.post(
            reverse("survey-detail", args=[self.survey.id]),
            {
                "age_group": "18-21",
                "consent": "on",
                f"question_{self.text_question.id}": "Listening and trusted information helps.",
                f"question_{self.choice_question.id}": "I feel stressed",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SurveyResponse.objects.count(), 1)
        self.assertEqual(SurveyAnswer.objects.count(), 2)
        submitted = SurveyResponse.objects.get()
        self.assertTrue(submitted.consent_given)
        self.assertEqual(submitted.age_group, "18-21")
        self.assertEqual(submitted.anonymous_token, "")
        self.assertEqual(
            SurveyAnswer.objects.get(question=self.text_question).answer_value,
            "",
        )

    def test_survey_rejects_choices_not_defined_by_the_question(self):
        response = self.client.post(
            reverse("survey-detail", args=[self.survey.id]),
            {
                "age_group": "18-21",
                "consent": "on",
                f"question_{self.text_question.id}": "A suitable response.",
                f"question_{self.choice_question.id}": "Unlisted option",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "available answer")
        self.assertEqual(SurveyResponse.objects.count(), 0)

    def test_public_insights_never_show_written_answers_and_suppress_small_cells(self):
        for index in range(10):
            response = SurveyResponse.objects.create(
                survey=self.survey,
                consent_given=True,
                age_group="18-21",
                country=self.country,
                status="submitted",
            )
            SurveyAnswer.objects.create(
                response=response,
                question=self.text_question,
                answer_text=f"Private identifying narrative {index}",
                answer_value=f"Private identifying narrative {index}",
            )
            value = "I feel stressed" if index < 5 else "I need support"
            SurveyAnswer.objects.create(
                response=response,
                question=self.choice_question,
                answer_text=value,
                answer_value=value,
            )

        response = self.client.get(reverse("insights"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Private identifying narrative")
        self.assertContains(response, "I feel stressed: 5")
        self.assertContains(response, "I need support: 5")

    def test_public_insights_suppress_a_distribution_with_small_cells(self):
        for index in range(6):
            response_record = SurveyResponse.objects.create(
                survey=self.survey,
                consent_given=True,
                age_group="18-21",
                country=self.country,
                status="submitted",
            )
            value = "I feel stressed" if index < 5 else "I need support"
            SurveyAnswer.objects.create(
                response=response_record,
                question=self.choice_question,
                answer_text=value,
                answer_value=value,
            )

        response = self.client.get(reverse("insights"))
        self.assertNotContains(response, "I feel stressed: 5")
        self.assertNotContains(response, "I need support: 1")
        self.assertContains(response, "distribution includes a group with fewer than five")

    def test_public_results_are_withheld_below_five_responses(self):
        for _ in range(4):
            SurveyResponse.objects.create(
                survey=self.survey,
                consent_given=True,
                age_group="18-21",
                country=self.country,
                status="submitted",
            )
        response = self.client.get(reverse("insights"))
        self.assertContains(response, "not enough responses")
        self.assertNotContains(response, "Aggregate responses:")

    def test_restricted_dashboard_requires_staff_access(self):
        user = get_user_model().objects.create_user(username="member", password="securepass123")
        self.client.force_login(user)
        response = self.client.get(reverse("analytics-dashboard"))
        self.assertEqual(response.status_code, 302)

        admin = get_user_model().objects.create_user(username="admin", password="securepass123", is_staff=True, is_superuser=True)
        self.client.force_login(admin)
        admin_response = self.client.get(reverse("analytics-dashboard"))
        self.assertEqual(admin_response.status_code, 200)
