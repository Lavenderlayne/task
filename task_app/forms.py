from django import forms
from .models import Task, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-light',
                'rows': 3,
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control bg-dark text-white border-light',
            }),
        }
        labels = {
            'content': '',
            'file': '',
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-light',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-light',
                'rows': 4,
            }),
            'status': forms.Select(attrs={
                'class': 'form-select bg-dark text-white border-light',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select bg-dark text-white border-light',
            }),
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control bg-dark text-white border-light',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            classes = existing_classes.split()
            additional_classes = ['form-control', 'bg-dark', 'text-white', 'border-light']
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                additional_classes[0] = 'form-select'
            for c in additional_classes:
                if c not in classes:
                    classes.append(c)
            field.widget.attrs['class'] = ' '.join(classes)
