from typing import Type
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model: Type[User] = User
        field = ("email", 'password')

    email = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Email address"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Email address"
    }))

