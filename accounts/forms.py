from typing import Type
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model: Type[User] = User
        field = ("username", 'password')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'email',
        'class': "border rounded-lg border-primary px-[1rem] cursor-pointer focus:border-hover_col focus:ring-1 focus:ring-primary focus:outline-none"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "password",
        'class': "border rounded-lg border-primary px-[1rem] cursor-pointer focus:border-hover_col focus:ring-1 focus:ring-primary focus:outline-none"
    }))

