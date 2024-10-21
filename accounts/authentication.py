from django.contrib.auth.models import User
from .models import Profile
from .views import send_verification_email


def social_email_verification(request, response, user, *args, **kwrags):
        email = response.get("email") # get the user email
        if user:
            user.is_active = False
            send_verification_email(request, user, email)        

def create_profile(backend, user, *args, **kwargs):
    """
        Create User Profile when  user is authenticated via social media
    """
    Profile.objects.get_or_create(user=user)


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
        
    


