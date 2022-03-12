from django.contrib.auth import authenticate, get_user_model, login
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import UserChangeForm, UserCreationForm
from .models import User

user = get_user_model()


class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('twitter:homepage')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(self.request, user)
                return HttpResponseRedirect(reverse_lazy('twitter:homepage'))
            else:
                return redirect(reverse('accounts:signup'))
        else:
            redirect(reverse('accounts:signup'))


class PasswordChangeView(CreateView):
    form_class = UserChangeForm
    template_name = 'accounts/password_change_done.html'
    success_url = reverse_lazy('twitter:homepage')
