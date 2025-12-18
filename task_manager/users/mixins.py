from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AuthRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Для выполнения этой операции необходимо авторизоваться",
        )
        return redirect(reverse_lazy("login_view"))


class EditPermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user_id = request.user.id
        id = int(kwargs["pk"])
        if user_id != id:
            messages.error(
                request,
                "У вас нет прав для изменения",
            )
            return redirect(reverse_lazy("users_list_view"))
        return super().dispatch(request, *args, **kwargs)
