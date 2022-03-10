from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import UserManager
from django.urls import reverse, resolve
from django.contrib.auth.forms import UserCreationForm
from .views import SignUpView

user = get_user_model()
objects = UserManager


class CreateUserTests(TestCase):
    def setUp(self):
        self.user = user.objects.create_user(
            username="test", password="helloEVerybodY123")
        self.username1 = ""
        self.password1 = "helloEVerybodY123"
        self.username2 = "はら"
        self.password2 = "helloEVerybodY123"

    def test_successful_create_user(self):
        self.client = Client()
        login_status = self.client.logout()
        self.assertFalse(login_status)
        login_status = self.client.login(
            username="test", password="helloEVerybodY123")
        self.assertTrue(login_status)

    def test_invalid_create_user_none_name(self):
        try:
            user.objects.create_user(self.username1, self.password1)
        except ValueError:
            pass

    def test_invalid_create_user_unicode_error(self):
        try:
            user.objects.create_user(self.username2, self.password2)
        except AttributeError:
            pass


class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        data_hiragana = {
            'username': 'テスト',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data_hiragana)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(user.objects.exists())


class TestsSignUpBasic(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func.view_class, SignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        data = {
            'username': 'test',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('twitter:homepage')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(user.objects.exists())
