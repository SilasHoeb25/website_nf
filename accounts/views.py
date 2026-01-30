from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignupForm, LoginForm, EmailChangeForm


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/") 
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("/")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})


@login_required
def account_view(request):
    # Default initial value
    form = EmailChangeForm(initial={"email": request.user.email})

    if request.method == "POST":
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data.get("email", "")
            request.user.save(update_fields=["email"])
            messages.success(request, "Email updated.")
            return redirect("account")

    return render(request, "accounts/account.html", {"form": form})