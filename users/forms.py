# from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации нового пользователя с дополнительными полями."""

    class Meta:
        model = User
        fields = ("username", "email", "avatar", "phone_number", "country")


class CustomUserChangeForm(UserChangeForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ("username", "email", "avatar", "phone_number", "country")
