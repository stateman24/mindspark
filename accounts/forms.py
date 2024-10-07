from typing import Type, Tuple
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import CharField
import re


class LoginForm(AuthenticationForm):
    class Meta:
        model: Type[User] = User
        field: tuple[str, str] = ("username", 'password')

    username: CharField = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'email',
        'class': "border rounded-lg border-primary px-[1rem] cursor-pointer focus:border-hover_col focus:ring-1 focus:ring-primary focus:outline-none"
    }))

    password: CharField = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "password",
        'class': "border rounded-lg border-primary px-[1rem] cursor-pointer focus:border-hover_col focus:ring-1 focus:ring-primary focus:outline-none"
    }))


class RegisterUser(forms.ModelForm):
    password: CharField = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model: User = User
        fields: tuple[str, str] = ('email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # check if the email is valid
        if not re.match(email_regex, email):
            raise forms.ValidationError("Enter a valid Email address")

        # check if the email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        return email


