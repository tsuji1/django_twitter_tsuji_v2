from django.contrib.auth import get_user_model

from .models import UserManager

user = get_user_model()
objects = UserManager


def username_finder(username):
    try:
        user.objects.get(username=username)
    except:
        return False
    else:
        return True
