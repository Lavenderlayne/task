from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    CommentUpdateView,
    CommentDeleteView,
    like_comment,
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),

    # Коментарі
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/like/', like_comment, name='like_comment'),
]
