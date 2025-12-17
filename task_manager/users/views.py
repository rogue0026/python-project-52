from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.users.forms import RegistrationForm
from task_manager.users.mixins import (
    AuthRequiredMixin,
    EditPermissionRequiredMixin,
)


class UserListView(ListView):
    template_name = "users/index.html"
    model = User


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    success_url = reverse_lazy("login_view")
    form_class = RegistrationForm

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return super().form_valid(form)


class UpdateUserView(AuthRequiredMixin, EditPermissionRequiredMixin, UpdateView):
    template_name = "users/update.html"
    success_url = reverse_lazy("users_list_view")
    model = User
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        return context

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно изменен")
        return super().form_valid(form)


class DeleteUserView(AuthRequiredMixin, EditPermissionRequiredMixin, DeleteView):
    login_url = "users/login/"
    success_url = reverse_lazy("users_list_view")
    template_name = "users/delete.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        return context

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно удален")
        return super().form_valid(form)
