from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from auth_system.forms import LoginForm, RegisterForm

class CustomLoginView(LoginView):
    template_name = "login_page.html"
    form_class = LoginForm

class RegisterView(CreateView):
    template_name = "register_page.html"
    form_class = RegisterForm
    success_url = '/login/'