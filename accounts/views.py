from typing import Any
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, redirect
from .forms import RegisterUser, EditProfileForm
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
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
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
User: AbstractUser = get_user_model()


class Index(LoginRequiredMixin,  TemplateView):
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        if self.request.user.is_authenticated:
            if self.request.user.is_active:
                messages.success(self.request, "Your have verified your email")
            else:
                messages.warning(self.request, "Please verify you email adderess")
        return context


# verify user email
class Verify_Email(LoginRequiredMixin, TemplateView):
    template_name = "verify_email.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
    

# register User
class RegisterUser(FormView):
    template_name: str = "accounts/register.html"
    form_class: RegisterUser = RegisterUser
    success_url: str = reverse_lazy("accounts:verify-email")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.username = form.cleaned_data["email"]  # set username to email address
        new_user.set_password(form.cleaned_data["password"]) # set user password
        new_user.is_active = False # deactivate account until email verification
        new_user.save()
        Profile.objects.create(user=new_user) # create a proile for the new user
        User: AbstractUser | None = authenticate(self.request, username=new_user.username, password=new_user.password)
        if User is not None:
           login(self.request, User)
        return redirect(self.get_success_url())
    

class EditProfile(LoginRequiredMixin, FormView):
    template_name = "accounts/editprofile.html"
    form_class = EditProfileForm
    success_url = reverse_lazy("accounts:index")

    def form_valid(self, form):
        edit_form = form(instance=self.request.user, data=self.request.POST, files=self.request.FILES)
        if edit_form.is_valid:
            edit_form.save()
        return redirect(self.success_url)


def send_verification_email(request, user_id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    user = User.objects.get(pk=user_id)
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
                        recipient_list=[user.email], 
                        html_message=message)
    return redirect("accounts:verify-email")
        
        
def activate_account(request, uidb64, token) -> HttpResponseRedirect | HttpResponsePermanentRedirect | None:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("accounts:index")

