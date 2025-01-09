from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserSignupForm


def signup_view(request):
    """User registration."""
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # This also triggers the signal to create UserProfile
            # Optionally log the user in directly after sign up:
            login(request, user)
            return redirect("home")  # Adjust to your desired redirect
    else:
        form = UserSignupForm()
    return render(request, "user/signup.html", {"form": form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect("home")  # If already logged in, redirect somewhere appropriate

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("furniture:home")
    else:
        form = AuthenticationForm()
    return render(request, "user/login.html", {"form": form})


def logout_view(request):
    """User logout."""
    if request.user.is_authenticated:
        logout(request)
    return redirect("furniture:home")
