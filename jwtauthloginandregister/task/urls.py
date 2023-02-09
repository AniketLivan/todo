from django.urls import path, include
from .api import  TaskDetail, RegisterApi, RegisterAccountDetail, RegisterBookmark, BookmarkDetail, RegisterComment, CommentDetail, RegisterPermission, PermissionDetail, RegisterVote
from rest_framework import routers
from .api import TaskListViewSet
router = routers.DefaultRouter()
router.register(r'api/task', TaskListViewSet)
urlpatterns = [
      # path('api/task', RegisterTask.as_view()),
      path('api/task/<str:pk>', TaskDetail.as_view()),
      path('api/register', RegisterApi.as_view()),
      path('api/account/<str:pk>', RegisterAccountDetail.as_view()),
      path('api/bookmark', RegisterBookmark.as_view()),
      path('api/bookmark/<str:pk>', BookmarkDetail.as_view()),
      path('api/comment', RegisterComment.as_view()),
      path('api/comment/<str:pk>', CommentDetail.as_view()),
      path('api/permission', RegisterPermission.as_view()),
      path('api/permission/<str:pk>', PermissionDetail.as_view()),
      path('api/vote', RegisterVote.as_view()),
      path('', include(router.urls)),
]