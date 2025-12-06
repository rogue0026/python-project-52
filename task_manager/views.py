from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, reverse
from django.views import View

from task_manager.forms import LoginForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "index.html",
        )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(
            request,
            "users/login.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        usr = authenticate(
            username=username,
            password=password,
        )
        if not usr:
            messages.error(
                request,
                "Неверное имя пользователя или пароль",
                extra_tags="alert alert-danger",
            )
            form = LoginForm(request.POST)
            return render(
                request,
                "users/login.html",
                context={
                    "form": form,
                },
                status=422,
            )
        login(request, usr)
        messages.success(
            request,
            "Вы залогинены",
            extra_tags="alert alert-success",
        )
        return redirect(reverse("start_page"))


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(
            request,
            "Вы разлогинены",
            "alert alert-success",
        )
        return redirect(reverse("start_page"))