from django.urls import path

from . import views

urlpatterns = [
    path("learn/", views.learn, name="learn"),
    path("learn/<slug:slug>/", views.article_detail, name="article-detail"),
    path("listen/", views.listen, name="listen"),
    path("watch-listen/", views.watch_listen, name="watch-listen"),
    path("stories/", views.stories, name="stories"),
    path("stories/<slug:slug>/", views.story_detail, name="story-detail"),
    path("resources/", views.resources, name="resources"),
]
