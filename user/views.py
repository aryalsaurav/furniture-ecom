from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserSignupForm, UserProfileForm


def signup_view(request):
    """User registration."""
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user_profile = profile_form.save()
            user_profile.user = user
            user_profile.save()
            login(request, user)
            return redirect("furniture:home")  # Adjust to your desired redirect
    else:
        form = UserSignupForm()
        profile_form = UserProfileForm()
    return render(
        request, "user/signup.html", {"form": form, "profile_form": profile_form}
    )


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
