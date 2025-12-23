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
    template_name = "users/registration.html"
    success_url = reverse_lazy("login_view")
    form_class = RegistrationForm
    success_message = "Пользователь успешно зарегистрирован"


class UpdateUserView(AuthRequiredMixin,
                     EditPermissionRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    template_name = "users/update.html"
    success_url = reverse_lazy("users_list_view")
    model = User
    form_class = UserUpdateForm
    success_message = "Пользователь успешно изменен"


class DeleteUserView(AuthRequiredMixin,
                     EditPermissionRequiredMixin,
                     SuccessMessageMixin,
                     DeleteView):
    login_url = "users/login/"
    success_url = reverse_lazy("users_list_view")
    template_name = "users/delete.html"
    model = User
    success_message = "Пользователь успешно удален"
