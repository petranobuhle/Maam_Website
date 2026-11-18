from django.urls import path

from . import views

urlpatterns = [
    path("get-involved/", views.get_involved, name="get-involved"),
]
