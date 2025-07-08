from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікуєця'),
        ('in_progress', 'У процесі'),
        ('completed', 'Завершено'),
    ]
    PRIORITY_CHOICES= [
        ('low', 'Низький'),
        ('medium', 'Середній'),
        ('high', 'Високий'),
    ]
    title = models.CharField(max_length= 255, verbose_name='Назва')
    description = models.TextField(null=True , blank=True, verbose_name='Опис')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medim', verbose_name='Пріоритет')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='Термін Виконання')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата Створення')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', verbose_name='Створення Ким')

    def __str__(self):
        return self.title