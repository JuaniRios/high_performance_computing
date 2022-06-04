from django.contrib import admin
from django.urls import path
from .views import UserList, TokenService

urlpatterns = [
    path('users', UserList.as_view()),
    path("token", TokenService.as_view())
]