from django.urls import path

from . import views

urlpatterns = [
    path("insights/", views.insights, name="insights"),
    path("survey/<uuid:survey_id>/", views.survey_detail, name="survey-detail"),
    path("survey/<uuid:survey_id>/success/", views.survey_success, name="survey-success"),
    path("research/dashboard/", views.research_dashboard, name="research-dashboard"),
]
