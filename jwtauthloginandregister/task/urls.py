from django.urls import path, include
from .api import RegisterTask, TaskDetail

urlpatterns = [
      path('', RegisterTask.as_view()),
      path('<str:pk>', TaskDetail.as_view())
]