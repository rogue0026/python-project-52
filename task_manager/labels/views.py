from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.users.mixins import AuthRequiredMixin


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"


class CreateLabelView(AuthRequiredMixin, CreateView):
    template_name = "labels/create.html"
    success_url = reverse_lazy('labels_list_view')
    model = Label
    form_class = LabelForm

    def form_valid(self, form):
        messages.success(
            self.request,
            "Метка успешно создана",
            extra_tags="alert alert-success",
        )
        return super().form_valid(form)


class UpdateLabelView(AuthRequiredMixin, UpdateView):
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels_list_view")
    model = Label
    form_class = LabelForm

    def get_context_data(self, **kwargs):
        label_id = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        context["label_id"] = label_id
        return context

    def form_valid(self, form):
        messages.success(self.request,"Метка успешно изменена")
        return super().form_valid(form)


class DeleteLabelView(AuthRequiredMixin, DeleteView):
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels_list_view")
    model = Label

    def get_context_data(self, **kwargs):
        label_id = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        context["label_id"] = label_id
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, "Метка успешно удалена")
        except ProtectedError:
            messages.error(self.request,"Невозможно удалить метку, потому что она используется")
        return HttpResponseRedirect(success_url)
