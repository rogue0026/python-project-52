from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy


class AuthRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Для выполнения этой операции необходимо авторизоваться",
        )
        return redirect(reverse_lazy("login_view"))


class EditPermissionRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == int(self.kwargs.get("pk"))

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения",
        )
        return redirect(reverse_lazy("users_list_view"))
