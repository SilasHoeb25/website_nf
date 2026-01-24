from django.shortcuts import render, redirect
from django.contrib.auth import login
#from .forms import SignUpForm


def home(request):
    if request.headers.get("HX-Request") == "true":
        return render(request, "partials/_home_content.html")
    return render(request, "home.html")

def about(request):
    if request.headers.get("HX-Request") == "true":
        return render(request, "partials/_about_content.html")
    return render(request, "about.html")

