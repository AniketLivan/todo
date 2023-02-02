from django.urls import path
from .api import RegisterApi, RegisterAccountDetail

urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      path('<str:pk>', RegisterAccountDetail.as_view())
]