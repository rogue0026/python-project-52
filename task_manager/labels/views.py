from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.users.mixins import (
    AuthRequiredMixin,
)


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"


class CreateLabelView(AuthRequiredMixin, FormView):
    template_name = "labels/create.html"
    success_url = reverse_lazy('labels_list_view')

    def get_form_class(self):
        return LabelForm

    def form_valid(self, form):
        label_name = form.cleaned_data["name"]
        label = Label.objects.create(name=label_name)
        label.save()
        messages.success(
            self.request,
            "Метка успешно создана",
            extra_tags="alert alert-success",
        )
        return super().form_valid(form)


class UpdateLabelView(AuthRequiredMixin, FormView):
    success_url = reverse_lazy("labels_list_view")
    template_name = "labels/update.html"

    def get_form_class(self):
        return LabelForm

    def get_initial(self):
        label_id = int(self.kwargs.get("pk"))
        existing_label = Label.objects.get(id=label_id)

        return {
            "name": existing_label.name
        }

    def get_context_data(self, **kwargs):
        label_id = self.kwargs.get("pk")

        context = super().get_context_data(**kwargs)
        context["label_id"] = label_id

        return context

    def form_valid(self, form):
        label_id = self.kwargs.get("pk")

        existing_label = Label.objects.get(id=label_id)
        existing_label.name = form.cleaned_data["name"]
        existing_label.save()

        messages.success(
            self.request,
            "Метка успешно изменена",
            extra_tags="alert alert-success",
        )

        return super().form_valid(form)


class DeleteLabelView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = int(kwargs.get("pk"))
        label = Label.objects.get(id=label_id)
        return render(
            request,
            "labels/delete.html",
            context={
                "label_name": label.name,
                "label_id": label_id,
            },
        )

    def post(self, request, *args, **kwargs):
        label_id = int(kwargs.get("pk"))
        label = Label.objects.get(id=label_id)
        try:
            label.delete()
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется",
                extra_tags="alert alert-danger",
            )
            return redirect(reverse("labels_list_view"))

        messages.success(
            request,
            "Метка успешно удалена",
            extra_tags="alert alert-success",
        )
        return redirect(reverse("labels_list_view"))
