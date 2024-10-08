from django.shortcuts import render
from .forms import RegisterUser
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy

def index(request):
    return render(request, "accounts/index.html")

# register User
class RegisterUser(FormView):
    template_name: str = "accounts/register.html"
    form_class: RegisterUser = RegisterUser
    success_url: str = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user: User = User.objects.create_user(
            username=form.cleaned_data["email"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )
        return redirect(self.get_success_url())
