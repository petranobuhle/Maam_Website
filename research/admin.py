from django.contrib import admin

from .models import Survey, SurveyAnswer, SurveyQuestion, SurveyResponse


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("title", "version", "country", "language", "is_active")
    list_filter = ("is_active", "country", "language")
    search_fields = ("title", "slug")


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("survey", "order", "question_type", "is_required")
    list_filter = ("question_type", "is_required")
    search_fields = ("question_text",)


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ("survey", "status", "consent_given", "submitted_at")
    list_filter = ("status", "consent_given")


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ("response", "question")
    search_fields = ("response__survey__title", "question__question_text")
