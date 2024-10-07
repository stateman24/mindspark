from typing import Any
from django.urls import path
import django.contrib.auth.views as auth_view
from .forms import LoginForm
from .views import index, register


app_name: str = 'accounts'


urlpatterns: list[Any] = [
    path("login", auth_view.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name="login"),
    path("logout/", auth_view.LogoutView.as_view(), name="logout"),
    path("signup/", register, name='signup'),
    path("index/", index, name="index"),
]
