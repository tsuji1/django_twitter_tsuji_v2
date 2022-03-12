from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
  path('signup/',views.SignUpView.as_view(),name='signup'),
  ]
