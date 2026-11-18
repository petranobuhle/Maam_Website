from django.urls import path

from . import views

urlpatterns = [
    path("support/", views.support_directory, name="support"),
    path("support/<uuid:id>/", views.support_detail, name="support-detail"),
]
