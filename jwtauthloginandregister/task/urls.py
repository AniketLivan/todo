from django.urls import path, include
from .api import RegisterTask, TaskDetail, RegisterApi, RegisterAccountDetail, RegisterBookmark, BookmarkDetail, RegisterComment, CommentDetail, RegisterPermission, PermissionDetail, RegisterVote

urlpatterns = [
      path('', RegisterTask.as_view()),
      path('<str:pk>', TaskDetail.as_view()),
      path('api/register', RegisterApi.as_view()),
      path('<str:pk>', RegisterAccountDetail.as_view()),
      path('', RegisterBookmark.as_view()),
      path('<str:pk>', BookmarkDetail.as_view()),
      path('', RegisterComment.as_view()),
      path('<str:pk>', CommentDetail.as_view()),
      path('', RegisterPermission.as_view()),
      path('<str:pk>', PermissionDetail.as_view()),
      path('', RegisterVote.as_view()),
]