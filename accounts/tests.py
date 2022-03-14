from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.test import Client, TestCase
from django.urls import resolve, reverse

from .models import UserManager
from .views import SignUpView

user = get_user_model()
objects = UserManager


def username_finder(username):
    try:
        user.objects.get(username=username)
    except:
        return False
    else:
        return True


class SignUpTests(TestCase):
    def setUp(self):

        self.url = reverse('accounts:signup')
        self.home_url = reverse('twitter:homepage')

        self.data_success = {
            'username': 'test',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        data_hiragana = {
            'username': 'テスト',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(self.url, data_hiragana)

        self.response_success = self.client.post(self.url, self.data_success)

    def test_successful_create_user(self):
        self.user = user.objects.create_user(
            username="thisistest", password="helloEVerybodY123")
        self.assertTrue(user.objects.exists())

    def test_invalid_create_user_null_name(self):
        self.username1 = ""
        self.password1 = "helloEVerybodY123"
        try:
            user.objects.create_user(self.username1, self.password1)
        except ValueError:
            pass

    def test_invalid_create_user_unicode_error(self):

        self.username2 = "はら"
        self.password2 = "helloEVerybodY123"
        try:
            user.objects.create_user(self.username2, self.password2)
        except AttributeError:
            pass

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

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_hiragana_create_user(self):
        self.assertFalse(username_finder('テスト'))

    def test_redirection(self):
        self.assertRedirects(self.response_success, self.home_url)

    def test_user_creation_success(self):
        self.assertTrue(user.objects.get(username='test'))

    def test_user_authenticate_success(self):
        self.assertTrue(user.is_authenticated)

    def test_null_name_user_creation(self):
        data_null_name = {
            'username': '',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response_null_name = self.client.post(self.url, data_null_name)

        self.assertFalse(username_finder(""))

    def test_large_name_user_creation(self):
        data_large_name = {
            'username': 'testtesttesttest',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response_large_name = self.client.post(self.url, data_large_name)
        self.assertFalse(username_finder('testtesttesttest'))

    def test_small_password_user_creation(self):

        data_small_password = {
            'username': 'test1',
            'password1': 'abcdef1',
            'password2': 'abcdef1'
        }
        self.response_small_password = self.client.post(
            self.url, data_small_password)
        self.assertFalse(username_finder('test1'))

    def test_common_password_user_creation(self):
        data_common_password = {
            'username': 'test2',
            'password1': 'hellohello',
            'password2': 'hellohello'
        }
        self.response_common_password = self.client.post(
            self.url, data_common_password)
        self.assertFalse(username_finder('test2'))

    def test_only_number_password_user_creation(self):
        data_only_number_password = {
            'username': 'test3',
            'password1': '1234567',
            'password2': '1234567'
        }
        self.response_only_number_password = self.client.post(
            self.url, data_only_number_password)
        self.assertFalse(username_finder('test3'))

    def test_only_one_password_user_creation(self):
        data_only_one_password = {
            'username': 'test4',
            'password1': '1234567',
            'password2': ''
        }
        self.response_only_one_password = self.client.post(
            self.url, data_only_one_password)
        self.assertFalse(username_finder('test4'))

    def test_already_exist_user_creation(self):
        user.objects.create_user(
            username="already_exist", password="helloEVerybodY123")
        data_already_exist_username = {
            'username': 'already_exist',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response_already_exist_username = self.client.post(
            self.url, data_already_exist_username)
        self.assertEquals(
            self.response_already_exist_username.status_code, 200)
