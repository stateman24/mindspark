from typing import Any
from django.urls import path
import django.contrib.auth.views as auth_view


app_name: str = 'accounts'


urlpatterns: list[Any] = [
    path("login", auth_view.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path("logout/", auth_view.LogoutView.as_view(), name="logout")
]
