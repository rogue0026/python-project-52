from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from task_manager.common_views import BaseCreate, BaseUpdate, BaseDelete
from task_manager.users.forms import RegistrationForm, UserUpdateForm
from task_manager.users.mixins import (
    AuthRequiredMixin,
    EditPermissionRequiredMixin,
)


class BaseUsers:
    model = User


class UserListView(ListView):
    template_name = "users/index.html"
    model = User


class UserRegistrationView(BaseUsers, BaseCreate):
    success_url = reverse_lazy("login_view")
    form_class = RegistrationForm
    success_message = "Пользователь успешно зарегистрирован"
    extra_context = {
        "view_name": "registration_view",
        "header_name": "Регистрация",
        "create_button_name": "Зарегистрировать",
    }


class UpdateUserView(BaseUsers,
                     AuthRequiredMixin,
                     EditPermissionRequiredMixin,
                     BaseUpdate):
    success_url = reverse_lazy("users_list_view")
    form_class = UserUpdateForm
    success_message = "Пользователь успешно изменен"
    extra_context = {
        "view_name": "users_update_view",
        "header_name": "Редактирование данных пользователя",
    }


class DeleteUserView(BaseUsers,
                     AuthRequiredMixin,
                     EditPermissionRequiredMixin,
                     BaseDelete):
    login_url = "users/login/"
    success_url = reverse_lazy("users_list_view")
    success_message = "Пользователь успешно удален"
    extra_context = {
        "view_name": "users_delete_view",
    }
