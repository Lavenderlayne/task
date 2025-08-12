from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView
from auth_system.forms import LoginForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from task_app.models import Task

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"
    def get_queryset(self):
        queryset = Task.objects.filter(created_by=self.request.user)
        return queryset

class CustomLoginView(LoginRequiredMixin, LoginView):
    template_name = "login_page.html"
    form_class = LoginForm

class RegisterView(LoginRequiredMixin,CreateView):
    template_name = "register_page.html"
    form_class = RegisterForm
    success_url = '/login/'