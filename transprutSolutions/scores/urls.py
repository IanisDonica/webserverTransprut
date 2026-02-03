from django.urls import path

from .views import create_score, list_scores, list_scores_by_level

urlpatterns = [
    path("scores/", create_score, name="create_score"),
    path("scores/list/", list_scores, name="list_scores"),
    path("scores/list/<int:level>/", list_scores_by_level, name="list_scores_by_level"),
]
