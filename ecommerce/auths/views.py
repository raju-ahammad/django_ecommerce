from django.shortcuts import render
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import CreateView, UpdateView
from  django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = ('registration/signup.html')
