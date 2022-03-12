
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('twitter/', include('twitter.urls')),
    path('accounts/', include('accounts.urls'),),
    path('accounts/', include('django.contrib.auth.urls'),),
]
