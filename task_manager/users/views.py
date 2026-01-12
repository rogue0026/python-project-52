from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView
)
from django.views.generic.list import ListView
from task_manager.users.forms import RegistrationForm, UserUpdateForm
from task_manager.users.mixins import (
    AuthRequiredMixin,
    EditPermissionRequiredMixin,
)


class UserListView(ListView):
    template_name = "users/index.html"
    model = User


class UserRegistrationView(SuccessMessageMixin,
                           CreateView):
    template_name = "common/create.html"
    success_url = reverse_lazy("login_view")
    form_class = RegistrationForm
    success_message = "Пользователь успешно зарегистрирован"
    extra_context = {
        "view_name": "registration_view",
        "header_name": "Регистрация",
        "create_button_name": "Зарегистрировать",
    }


class UpdateUserView(AuthRequiredMixin,
                     EditPermissionRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    template_name = "common/update.html"
    success_url = reverse_lazy("users_list_view")
    model = User
    form_class = UserUpdateForm
    success_message = "Пользователь успешно изменен"
    extra_context = {
        "view_name": "users_update_view",
        "header_name": "Редактирование данных пользователя",
    }


class DeleteUserView(AuthRequiredMixin,
                     EditPermissionRequiredMixin,
                     SuccessMessageMixin,
                     DeleteView):
    login_url = "users/login/"
    success_url = reverse_lazy("users_list_view")
    template_name = "common/delete.html"
    model = User
    success_message = "Пользователь успешно удален"
    extra_context = {
        "view_name": "users_delete_view",
    }
