from typing import Literal, Type
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import CharField
from .models import Profile
from django.forms.models import inlineformset_factory
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
    password: CharField = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "password",
        'class': "border rounded-lg border-primary px-[1rem] cursor-pointer focus:border-hover_col focus:ring-1 focus:ring-primary focus:outline-none"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'id': "email",
        'class': "border rounded-lg border-primary px-[1rem] cursor-pointer focus:border-hover_col focus:ring-1 focus:ring-primary focus:outline-none"
    }))
    
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
    

class EditProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField()
    city = forms.CharField(widget=forms.TextInput)
    phone_number = forms.CharField(widget=forms.TextInput)
    address = forms.CharField(widget=forms.TextInput)
    profile_pic = forms.ImageField()
    
    class Meta:
        model = User
        fields: tuple[Literal['']] = ('first_name', 'last_name', 'username', 'date_of_birth', 'city', 'phone_number', 'address', 'profile_pic')
    
    def __init__(self, *args, **kwargs):
        self.profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs) # initiate superclass constructor
        # pass profile instance if available
        if self.profile_instance:
            self.fields["date_of_birth"].initial = self.profile_instance.date_of_birth
            self.fields["city"].initial = self.profile_instance.city
            self.fields["address"].initial = self.profile_instance.address
            self.fields["profile_pic"].initial = self.profile_instance.profile_pic
            self.fields["phone_number"].initial = self.profile_instance.phone_number

    def save(self, commit = True):
        user =  super().save(commit=False)

        if self.profile_instance:
            self.profile_instance.date_of_birth = self.cleaned_data["date_of_birth"]
            self.profile_instance.city = self.cleaned_data["city"]
            self.profile_instance.address = self.cleaned_data["address"]
            self.profile_instance.profile_pic = self.cleaned_data["profile_pic"]
            self.profile_instance.phone_number = self.cleaned_data["phone_number"]

        if commit:
            self.profile_instance.save()

        return user


class EmailEditForm(forms.ModelForm):
    new_email = forms.CharField(widget=forms.EmailInput(attrs={
        "id": "new-email"
    }))
    confirm_email = forms.CharField(widget=forms.EmailInput(attrs={
        "id": "confirm-email"
    }))

    class Meta:
        model = User
        fields = ("new_email" ,"confirm_email",)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # check if the email is valid
        if not re.match(email_regex, new_email) and re.match(email_regex, confirm_email):
            raise forms.ValidationError("Enter a valid Email address")

        if new_email != confirm_email:
            raise forms.ValidationError("Enter the correct Email")

        # check if the email already exists
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("This email already exists")
        
        return email
    
    def save(self, commit = True):
        user =  super().save(commit=False)

        if self.clean_email:
            user.email = self.cleaned_data["new_email"]
        
        if commit:
            user.save()
        return user
    

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "new-password"
    }))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "new-password"
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "confirm-password"
    }))