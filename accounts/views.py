from django.shortcuts import render, redirect
from .forms import RegisterUser
from django.views.generic import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
# imports for email verification
from django.core.mail import send_mail
from .token import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.contrib.auth import login
from django.http import HttpResponse
from django.template.loader import render_to_string

User = get_user_model()

def index(request):
    return render(request, "accounts/index.html")

# register User
class RegisterUser(FormView):
    template_name: str = "accounts/register.html"
    form_class: RegisterUser = RegisterUser
    success_url: str = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # deactivate account until email verification
        user.save()
        # send email verification
        self.send_verification_email(user)
        return redirect(self.get_success_url())
    
    def send_verification_email(self, user):
        current_site = get_current_site(self.request)
        subject = "Activate your account"
        message = render_to_string("accounts/activate_email.html", {
            "user": user,
            "domain" : current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token(user)
        })
        send_mail(subject, message, "noreply@mindspark.com", [user.email], fail_silently=True)

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

