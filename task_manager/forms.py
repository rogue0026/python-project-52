from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя пользователя",
            "id": "id_username",
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.TextInput(attrs={
            "type": "password",
            "class": "form-control",
            "placeholder": "Пароль",
            "id": "id_password",
        })
    )
