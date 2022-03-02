from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from .models import UserManager
# Create your tests here.
user = get_user_model()
objects=UserManager
class testMakeUserOk(TestCase):
  def setUp(self):
    self.user=user.objects.create_user(username="test",password="helloEVerybodY123")
  def testAssertion(self):
    self.client = Client()
    login_status = self.client.logout()
    self.assertFalse(login_status)
    login_status = self.client.login(username="test",password="helloEVerybodY123")
    self.assertTrue(login_status)
  

class testMakeUserError(TestCase):
  def setUp(self):
    self.username1=""
    self.password1="helloEVerybodY123"
    self.username2="はら"
    self.password2="helloEVerybodY123"
  def testUsernameNullError(self):
    try:
      user.objects.create_user(self.username1,self.password1)
    except ValueError:
      pass
  def testUsernameValidationError(self):
      try:
         user.objects.create_user(self.username2,self.password2)
      except AttributeError:
        pass
