import datetime
import random
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .forms import SignUpForm, UserLoginForm


# Create your views here.
def index(request):
    current_time = datetime.datetime.now().timestamp()
    user_session = request.session.get("user", None)

    if request.user.is_authenticated:
        uname = request.user.get_full_name() or request.user.username
    elif user_session is None or user_session["time"] + 42 < current_time:
        request.session["user"] = {
            "name": random.choice(settings.SESSION_NAMES),
            "time": current_time,
        }
        uname = request.session["user"]["name"]
    else:
        uname = user_session["name"]

    return render(request, "myapp/index.html", {"uname": uname})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    else:
        form = UserLoginForm()
    return render(request, "myapp/login.html", {"form": form})


def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "myapp/signup.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("/")