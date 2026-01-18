from django.urls import path

from .views import create_score, list_scores

urlpatterns = [
    path("scores/", create_score, name="create_score"),
    path("scores/list/", list_scores, name="list_scores"),
]
