from django.urls import path
from .api import RegisterVote

urlpatterns = [
    path('', RegisterVote.as_view()),
]