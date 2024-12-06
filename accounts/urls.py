from typing import Any
from django.urls import path
import django.contrib.auth.views as auth_view
from .forms import LoginForm, ChangePasswordForm
from .views import *


app_name: str = 'accounts'


urlpatterns: list[Any] = [
    path("login", auth_view.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name="login"),
    path("logout/", auth_view.LogoutView.as_view(), name="logout"),
    path("signup/", RegisterUser.as_view(), name='signup'),
    path("index/", Index.as_view(), name="index"),
    path("editprofile/", EditProfile.as_view(), name="editprofile"),
    path("changeEmail/", ChangeEmail.as_view(), name="change_email"),
    path("passwordChange/", auth_view.PasswordChangeView.as_view(template_name="accounts/changePassword.html", form_class=ChangePasswordForm, success_url="accounts:index"), name="passwordChange"),
    # verify email url path
    path("verifyEmail/", Verify_Email.as_view(), name="verify-email"),
    path("send_email_verification/<int:user_id>", send_verification_email, name="send-email-verification"),
    path("verifyEmail/<uidb64>/<token>/", activate_account, name="activate"),

]
