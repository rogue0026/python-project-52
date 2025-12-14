from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.edit import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from task_manager.users.forms import RegistrationForm
from task_manager.users.middleware import (
    AuthRequiredMixin,
    EditPermissionRequiredMixin,
)


class UserListView(ListView):
    template_name = "users/index.html"
    model = User


# class UserRegistrationView(FormView):
#     form_class = RegistrationForm
#     success_url = reverse_lazy("login_view")
#     template_name = "users/registration.html"
#
#     def form_valid(self, form):
#         usr = User.objects.create_user(
#             first_name=form.cleaned_data["first_name"],
#             last_name=form.cleaned_data["last_name"],
#             username=form.cleaned_data["username"],
#         )
#         usr.set_password(form.cleaned_data["password1"])
#         usr.save()
#
#         messages.success(
#             self.request,
#             "Пользователь успешно зарегистрирован",
#             extra_tags="alert alert-success",
#         )
#         return super().form_valid(form)


class UserRegistrationView(View):
    def get(self, request, *args, **kwargs):
        registration_form = RegistrationForm()
        return render(
            request,
            "users/registration.html",
            context={
                "form": registration_form,
            }
        )

    def post(self, request, *args, **kwargs):
        reg_form = RegistrationForm(request.POST)
        if not reg_form.is_valid():
            return render(
                request,
                "users/registration.html",
                context={
                    "form": reg_form,
                },
                status=422,
            )
        usr = User.objects.create_user(
            username=request.POST.get("username"),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
        )
        usr.set_password(request.POST.get("password1"))
        usr.save()
        messages.success(
            request,
            "Пользователь успешно зарегистрирован",
            "alert alert-success",
        )
        return redirect(reverse("login_view"))


class UpdateUserView(AuthRequiredMixin, EditPermissionRequiredMixin, UpdateView):
    login_url = reverse_lazy("login_view")
    template_name = "users/update.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("users_list_view")

    def form_valid(self, form):
        self.object.first_name = form.cleaned_data["first_name"]
        self.object.last_name = form.cleaned_data["last_name"]
        self.object.username = form.cleaned_data["username"]
        self.object.password1 = form.cleaned_data["password1"]
        self.object.password2 = form.cleaned_data["password2"]
        self.object.save()
        return super().form_valid(form)


# class UpdateUserView(AuthRequiredMixin, EditPermissionRequiredMixin, View):
#     login_url = "users/login/"
#
#     def get(self, request, *args, **kwargs):
#         user_id = kwargs.get("pk")
#         usr = User.objects.get(id=user_id)
#         form = RegistrationForm({
#             "first_name": usr.first_name,
#             "last_name": usr.last_name,
#             "username": usr.username,
#             },
#         )
#         return render(
#             request,
#             "users/update.html",
#             context={
#                 "form": form,
#             },
#         )
#
#     def post(self, request, *args, **kwargs):
#         form = RegistrationForm(request.POST)
#         if not form.is_valid():
#             return render(
#                 request,
#                 "users/update.html",
#                 context={
#                     "form": form,
#                 },
#                 status=422,
#             )
#
#         user_id = kwargs.get("pk")
#         usr = User.objects.get(id=user_id)
#         usr.first_name = form.cleaned_data["first_name"]
#         usr.last_name = form.cleaned_data["last_name"]
#         usr.username = form.cleaned_data["username"]
#         usr.set_password(form.cleaned_data["password1"])
#         usr.save()
#
#         messages.success(
#             request,
#             "Пользовательские данные успешно обновлены",
#             "alert alert-success",
#         )
#         return redirect(reverse("start_page"))


class DeleteUserView(AuthRequiredMixin, EditPermissionRequiredMixin, View):
    login_url = "users/login/"

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        print(user_id)
        usr = User.objects.get(id=user_id)
        full_name = f"{usr.first_name} {usr.last_name}".strip()
        return render(
            request,
            "users/delete.html",
            context={
                "user_id": usr.id,
                "full_name": full_name,
            }
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        print(user_id)
        User.objects.get(id=user_id).delete()
        messages.success(
            request,
            "Пользователь успешно удален",
            "alert alert-success",
        )
        return redirect(reverse("users_list_view"))
