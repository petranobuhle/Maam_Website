from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from research.models import Survey
from research.views import _aggregate_survey_data, _get_active_country


@staff_member_required(login_url="admin:login")
def dashboard(request):
    survey = Survey.objects.filter(country=_get_active_country(), is_active=True).order_by("-created_at").first()
    summary = _aggregate_survey_data(survey) if survey else {"total_responses": 0, "age_group_counts": {}, "question_summaries": []}
    return render(request, "analytics/dashboard.html", {"survey": survey, "summary": summary})
