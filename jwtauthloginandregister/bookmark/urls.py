from django.urls import path
from bookmark.api import RegisterBookmark, BookmarkDetail

urlpatterns = [
    path('', RegisterBookmark.as_view()),
    path('<str:pk>', BookmarkDetail.as_view())
]