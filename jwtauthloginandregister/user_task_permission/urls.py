from django.urls import path
from .api import RegisterPermission, PermissionDetail

urlpatterns = [
    path('', RegisterPermission.as_view()),
    path('<str:pk>', PermissionDetail.as_view())
]