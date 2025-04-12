from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blog.views import home_view


def home_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")  # Redirect to login if not logged in