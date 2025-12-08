from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render, reverse
from django.views import View
from task_manager.forms import LoginForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "index.html",
        )


class Login(LoginView):

    template_name="login.html"
    redirect_authenticated_user = False
    authentication_form = LoginForm

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.",
            extra_tags="alert alert-danger",
        )
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        messages.success(
            self.request,
            "Вы залогинены",
            extra_tags="alert alert-success",
        )
        return super().form_valid(form)


class Logout(LogoutView):
    template_name = "logout.html"

    def post(self, request, *args, **kwargs):
        messages.success(
            request,
            "Вы разлогинены",
            extra_tags="alert alert-success",
        )
        return super().post(request, *args, **kwargs)
