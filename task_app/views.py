from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from .models import Task, Comment, CommentLike
from .forms import TaskForm, CommentForm


class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(FormMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.author = request.user
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'task_form.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.created_by != request.user and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.created_by != request.user and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class TaskCreateView(CreateView):
    model = Task
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['content', 'file']
    template_name = 'comment_form.html'

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()
    return redirect('task_detail', pk=comment.task.pk)
