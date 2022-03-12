from django.contrib import admin
from django.urls import path

from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.HomepageView.as_view(), name="homepage"),
]
