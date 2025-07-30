from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Твій Логін',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    password = forms.CharField(
        label='Твій Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''})
    )

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'