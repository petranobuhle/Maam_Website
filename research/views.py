import json
from collections import Counter

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Country
from .models import Survey, SurveyAnswer, SurveyQuestion, SurveyResponse

PUBLIC_CELL_MINIMUM = 5


def _get_active_country():
    return Country.objects.filter(is_active=True).first()


def _aggregate_survey_data(survey):
    responses = SurveyResponse.objects.filter(
        survey=survey,
        status="submitted",
        consent_given=True,
    )
    total = responses.count()
    if total < PUBLIC_CELL_MINIMUM:
        return {
            "total_responses": None,
            "age_group_counts": {},
            "age_groups_suppressed": True,
            "question_summaries": [],
            "suppressed": True,
        }

    age_counts = Counter(
        age_group
        for age_group in responses.values_list("age_group", flat=True)
        if age_group
    )
    age_groups_suppressed = any(
        0 < count < PUBLIC_CELL_MINIMUM for count in age_counts.values()
    )

    question_summaries = []
    for question in survey.questions.order_by("order", "id"):
        if question.question_type != SurveyQuestion.QuestionType.CHOICE:
            continue
        allowed_choices = {
            choice for choice in question.choices if isinstance(choice, str)
        }
        answers = SurveyAnswer.objects.filter(
            question=question,
            response__survey=survey,
            response__status="submitted",
            response__consent_given=True,
            answer_value__in=allowed_choices,
        )
        counted = Counter(answers.values_list("answer_value", flat=True))
        small_cell_exists = any(
            0 < count < PUBLIC_CELL_MINIMUM for count in counted.values()
        )
        publishable = [] if small_cell_exists else [
            {"label": label, "count": count}
            for label, count in sorted(counted.items(), key=lambda item: (-item[1], item[0]))
            if count
        ]
        question_summaries.append(
            {
                "question": question.question_text,
                "answers": publishable,
                "suppressed": small_cell_exists,
                "has_answers": bool(counted),
            }
        )

    return {
        "total_responses": total,
        "age_group_counts": {} if age_groups_suppressed else dict(sorted(age_counts.items())),
        "age_groups_suppressed": age_groups_suppressed,
        "question_summaries": question_summaries,
        "suppressed": False,
    }


def insights(request):
    survey = Survey.objects.filter(country=_get_active_country(), is_active=True).order_by("-created_at").first()
    summary = (
        _aggregate_survey_data(survey)
        if survey
        else {"total_responses": None, "age_group_counts": {}, "question_summaries": [], "suppressed": False}
    )
    return render(request, "research/insights.html", {"survey": survey, "summary": summary})


def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, is_active=True, country=_get_active_country())
    questions = survey.questions.order_by("order", "id")

    if request.method == "POST":
        errors = []
        consent = request.POST.get("consent") == "on"
        age_group = request.POST.get("age_group")
        if not consent:
            errors.append("You must consent to participate before submitting this anonymous survey.")
        if age_group not in {"18-21", "22-25", "26-29"}:
            errors.append("Please select your age group before continuing.")

        submitted_answers = {}
        for question in questions:
            field_name = f"question_{question.id}"
            if question.question_type == SurveyQuestion.QuestionType.MULTIPLE_CHOICE:
                values = [value.strip() for value in request.POST.getlist(field_name) if value.strip()]
                allowed_choices = {
                    choice for choice in question.choices if isinstance(choice, str)
                }
                if any(value not in allowed_choices for value in values):
                    errors.append("Please choose only an available answer.")
                if question.is_required and not values:
                    errors.append(f"The question '{question.question_text}' is required.")
                submitted_answers[question.id] = values
                continue

            value = request.POST.get(field_name, "").strip()
            if question.is_required and not value:
                errors.append(f"The question '{question.question_text}' is required.")
            if question.question_type == SurveyQuestion.QuestionType.CHOICE:
                allowed_choices = {
                    choice for choice in question.choices if isinstance(choice, str)
                }
                if value and value not in allowed_choices:
                    errors.append("Please choose an available answer.")
            elif len(value) > 2000:
                errors.append("Please keep each written response under 2,000 characters.")
            submitted_answers[question.id] = value

        if errors:
            return render(
                request,
                "research/survey_detail.html",
                {"survey": survey, "questions": questions, "errors": errors, "submitted": request.POST},
            )

        with transaction.atomic():
            response = SurveyResponse.objects.create(
                survey=survey,
                anonymous_token="",
                consent_given=True,
                age_group=age_group,
                country=survey.country,
                status="submitted",
            )
            for question in questions:
                answer = submitted_answers[question.id]
                if not answer:
                    continue
                if question.question_type == SurveyQuestion.QuestionType.MULTIPLE_CHOICE:
                    answer_text = ", ".join(answer)
                    answer_value = json.dumps(answer)
                elif question.question_type == SurveyQuestion.QuestionType.CHOICE:
                    answer_text = answer
                    answer_value = answer
                else:
                    answer_text = answer
                    answer_value = ""
                SurveyAnswer.objects.create(
                    response=response,
                    question=question,
                    answer_text=answer_text,
                    answer_value=answer_value,
                )

        messages.success(request, "Your anonymous survey response was submitted successfully.")
        return redirect("survey-success", survey_id=survey.id)

    return render(request, "research/survey_detail.html", {"survey": survey, "questions": questions})


def survey_success(request, survey_id):
    survey = get_object_or_404(
        Survey,
        id=survey_id,
        is_active=True,
        country=_get_active_country(),
    )
    return render(request, "research/survey_success.html", {"survey": survey})


@staff_member_required(login_url="admin:login")
def research_dashboard(request):
    survey = Survey.objects.filter(country=_get_active_country(), is_active=True).order_by("-created_at").first()
    summary = (
        _aggregate_survey_data(survey)
        if survey
        else {"total_responses": None, "age_group_counts": {}, "question_summaries": [], "suppressed": False}
    )
    return render(request, "research/dashboard.html", {"survey": survey, "summary": summary})
