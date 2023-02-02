from django.urls import path
from .api import RegisterComment, CommentDetail

urlpatterns = [
    path('', RegisterComment.as_view()),
    path('<str:pk>', CommentDetail.as_view())
]