import datetime
import random
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Tip

from .forms import SignUpForm, TipForm, UserLoginForm
from .signals import vote


# Create your views here.
def index(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse("myapp:index"))
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect("/")
    else:
        form = TipForm()

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

    tips = Tip.objects.all()
    for i in range(len(tips)):
        tips[i].upvotesCount = len(tips[i].upvotes.all())
        tips[i].downvotesCount = len(tips[i].downvotes.all())

    return render(
        request, "myapp/index.html", {"uname": uname, "tips": tips, "form": form}
    )


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


def update_tip(request, pk):
    if request.method != "POST":
        return redirect("/")
    if not request.user.is_authenticated:
        return redirect("/")
    tip = get_object_or_404(Tip, pk=pk)
    action = request.POST.get("action")
    if action == "delete":
        if request.user == tip.author or request.user.has_perm("myapp.delete_tip"):
            tip.delete()
    elif action == "upvote":
        if request.user in tip.upvotes.all():
            tip.upvotes.remove(request.user)
            vote.send(Tip, bonus=-5, user=tip.author)
        else:
            if request.user in tip.downvotes.all():
                tip.downvotes.remove(request.user)
                vote.send(Tip, bonus=2, user=tip.author)
            tip.upvotes.add(request.user)
            vote.send(Tip, bonus=5, user=tip.author)
        tip.save()
    elif action == "downvote":
        if request.user == tip.author or request.user.has_perm("myapp.can_downvote"):
            if request.user in tip.downvotes.all():
                tip.downvotes.remove(request.user)
                vote.send(Tip, bonus=2, user=tip.author)
            else:
                if request.user in tip.upvotes.all():
                    tip.upvotes.remove(request.user)
                    vote.send(Tip, bonus=-5, user=tip.author)
                tip.downvotes.add(request.user)
                vote.send(Tip, bonus=-2, user=tip.author)
            tip.save()
    return redirect("/")
