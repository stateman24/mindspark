from typing import Any
from django.urls import path
import django.contrib.auth.views as auth_view
from .forms import LoginForm
from .views import index, RegisterUser, activate_account, Verify_Email, send_verification_email


app_name: str = 'accounts'


urlpatterns: list[Any] = [
    path("login", auth_view.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name="login"),
    path("logout/", auth_view.LogoutView.as_view(), name="logout"),
    path("signup/", RegisterUser.as_view(), name='signup'),
    path("index/", index, name="index"),
    path("verifyEmail/", Verify_Email.as_view(), name="verify-email"),
    path("send_email_verification/<int:user_id>", send_verification_email, name="send-email-verification"),
    path("verifyEmail/<uidb64>/<token>/", activate_account, name="activate")
]
