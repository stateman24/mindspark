from django.shortcuts import render, redirect
from .forms import RegisterUser
from django.views.generic import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from .models import Profile
# imports for email verification
from django.contrib import messages
from django.core.mail import send_mail
from .token import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.contrib.auth import login
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

User = get_user_model()

def index(request):
    if request.user.is_authenticated:
        if request.user.is_active:
            messages.success(request, "Your have verified your email")
        else:
            messages.warning(request, "Please verify you email adderess")
    return render(request, "accounts/index.html")

# register User
class RegisterUser(FormView):
    template_name: str = "accounts/register.html"
    form_class: RegisterUser = RegisterUser
    success_url: str = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data["email"]  # set username to email address
        user.set_password(form.cleaned_data["password"]) # set user password
        user.is_active = False # deactivate account until email verification
        user.save()
        Profile.objects.create(user=user) # create a proile for the new user
        # send email verification
        send_verification_email(self.request, user, form.cleaned_data["email"])
        return redirect(self.get_success_url())
    

def send_verification_email(request, user, to_email):
    current_site = get_current_site(request)
    email_context = {
        "user": user.username,
        "domain" : current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
    }
    subject = "Activate your account"
    message = render_to_string(template_name="activate_email.html", context=email_context)
    html_message = strip_tags(message)
    email = send_mail(subject=subject, 
                        message=html_message, 
                        from_email= settings.EMAIL_HOST_USER, 
                        recipient_list=[to_email], 
                        html_message=message)
        

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("accounts:index")

