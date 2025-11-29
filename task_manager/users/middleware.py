from django.contrib import messages
from django.shortcuts import redirect, reverse


class AuthRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                "Для выполнения этой операции необходимо авторизоваться",
                "alert alert-danger",
            )
            return redirect(reverse("login_view"))

        return super().dispatch(request, *args, **kwargs)


class EditPermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user_id = request.user.id
        id = kwargs.get("pk")
        print(id)
        if user_id != id:
            messages.error(
                request,
                "Недостаточно прав",
                "alert alert-danger",
            )
            return redirect(reverse("users_list_view"))

        return super().dispatch(request, *args, **kwargs)
