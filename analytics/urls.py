from django.urls import path

from . import views

urlpatterns = [
    path("analytics/dashboard/", views.dashboard, name="analytics-dashboard"),
]
