from django.contrib.auth.backends import ModelBackend

from .models import User


class UserAuthBackend(ModelBackend):
    def authenticate(self, request=None,username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
