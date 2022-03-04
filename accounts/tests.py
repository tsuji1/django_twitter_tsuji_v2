from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from .models import UserManager

user = get_user_model()
objects=UserManager
class CreateUserTests(TestCase):
    def setUp(self):
        self.user=user.objects.create_user(username="test",password="helloEVerybodY123")
        self.username1=""
        self.password1="helloEVerybodY123"
        self.username2="はら"
        self.password2="helloEVerybodY123"
    def test_successful_create_user(self):
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status)
        login_status = self.client.login(username="test",password="helloEVerybodY123")
        self.assertTrue(login_status)
    def test_invalid_create_user_none_name(self):
        try:
            user.objects.create_user(self.username1,self.password1)
        except ValueError:
            pass
    def test_invalid_create_user_unicode_error(self):
        try:
           user.objects.create_user(self.username2,self.password2)
        except AttributeError:
           pass
