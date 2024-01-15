import datetime
import random
from django.conf import settings
from django.shortcuts import render


# Create your views here.
def index(request):
    current_time = datetime.datetime.now().timestamp()
    user_session = request.session.get("user", None)

    if user_session is None or user_session["time"] + 42 < current_time:
        request.session["user"] = {
            "name": random.choice(settings.SESSION_NAMES),
            "time": datetime.datetime.now().timestamp(),
        }

    uname = user_session["name"]
    return render(request, "myapp/index.html", {"uname": uname})
