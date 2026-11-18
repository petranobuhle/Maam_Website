import uuid

from django.db import models

from core.models import Country, Language


class Survey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    intro_text = models.TextField(blank=True)
    version = models.PositiveIntegerField(default=1)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="surveys")
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="surveys")
    is_active = models.BooleanField(default=False)
    target_age_min = models.PositiveIntegerField(default=18)
    target_age_max = models.PositiveIntegerField(default=29)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["slug", "version"], name="unique_survey_slug_version")
        ]

    def __str__(self):
        return f"{self.title} v{self.version}"


class SurveyQuestion(models.Model):
    class QuestionType(models.TextChoices):
        TEXT = "text", "Text"
        CHOICE = "choice", "Choice"
        MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices, default=QuestionType.TEXT)
    choices = models.JSONField(default=list, blank=True)
    help_text = models.TextField(blank=True)
    is_required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.question_text


class SurveyResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, related_name="responses")
    anonymous_token = models.CharField(max_length=64, blank=True, db_index=True)
    consent_given = models.BooleanField(default=False)
    age_group = models.CharField(max_length=20, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL, related_name="survey_responses")
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("draft", "Draft"), ("submitted", "Submitted")], default="draft")

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Response for {self.survey.title}"


class SurveyAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(SurveyQuestion, on_delete=models.PROTECT, related_name="answers")
    answer_text = models.TextField(blank=True)
    answer_value = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["question__order"]
        constraints = [
            models.UniqueConstraint(fields=["response", "question"], name="unique_response_question_answer")
        ]

    def __str__(self):
        return f"{self.question.question_text[:60]}"
