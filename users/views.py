from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import CustomUserChangeForm, CustomUserCreationForm


def register(request: HttpRequest) -> HttpResponse:
    """Регистрация нового пользователя."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("index")
        messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request: HttpRequest) -> HttpResponse:
    """Авторизация пользователя."""
    if request.method == "POST":
        form = CustomUserCreationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {username}!")
                return redirect("index")
            messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    """Выход пользователя из системы."""
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect("index")


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """Просмотр профиля пользователя."""
    return render(request, "users/profile.html")


@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    """Редактирование профиля пользователя."""
    if request.method == "POST":
        form = CustomUserChangeForm(
            request.POST,
            request.FILES,
            instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён.")
            return redirect("profile")
        messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "users/profile_edit.html", {"form": form})
