from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AuthRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Для выполнения этой операции необходимо авторизоваться",
        )
        return redirect(reverse_lazy("login_view"))


class EditPermissionRequiredMixin(UserPassesTestMixin):

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.error(
                self.request,
                "У вас нет прав для изменения",
            )
            return redirect(reverse_lazy("users_list_view"))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        current_user_id = self.request.user.id
        editable_user = self.kwargs.get("pk")
        return current_user_id == editable_user
