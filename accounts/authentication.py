from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .models import Profile

UserModel = get_user_model()


def create_profile(backend, user, *args, **kwargs):
    """
        Create User Profile when  user is authenticated via social media
    """
    Profile.objects.get_or_create(user=user)


def check_user_exists(backend, response, request,  *args, **kwargs):
    """
        Check and authencicate a user that already exists
    """
    social_email = response.get("email") # get  the email from the social auth provider
    if UserModel.objects.filter(email=social_email).exists(): # check if email exists
        user = UserModel.objects.get(email=social_email) # get the user
        auth_user = authenticate(request, username=user.username, password=user.password)  # authenticate the user
        if auth_user is not None:
           login(request, auth_user)
        return redirect("accounts:index") # redirect to the profile Page



class EmailAuthentication:
    def authenticate(self, request, username=None, password=None):
        try:
            user: User = User.objects.get(email=username)
            if user.check_password:
                return user
            return None
        except (User.MultipleObjectsReturned, User.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    


