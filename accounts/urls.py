
from django.contrib import admin
from django.urls import path, include

from . views import CustomAuthToken, UserCreate, ChangePasswordView, UserUpdate

app_name = "accounts"

urlpatterns = [
    path("login", CustomAuthToken.as_view(), name="login"),
    path("register", UserCreate.as_view(), name="register"),
    path("change_password/<int:pk>", ChangePasswordView.as_view(), name="change_password"),
    path("user_update/<int:pk>", UserUpdate.as_view(), name="user_update"),
]
