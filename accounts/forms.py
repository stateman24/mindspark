from typing import Type

from django.forms import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model: Type[User] = User
        field = ("email", 'password')

