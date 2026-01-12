from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.users.mixins import AuthRequiredMixin


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"


class CreateLabelView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "common/create.html"
    success_url = reverse_lazy('labels_list_view')
    model = Label
    form_class = LabelForm
    success_message = "Метка успешно создана"
    extra_context = {
        "view_name": "labels_create_view",
        "header_name": "Создать метку",
    }


class UpdateLabelView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView):
    template_name = "common/update.html"
    success_url = reverse_lazy("labels_list_view")
    model = Label
    form_class = LabelForm
    success_message = "Метка успешно изменена"
    extra_context = {
        "view_name": "labels_update_view",
        "header_name": "Изменение метки",
    }


class DeleteLabelView(AuthRequiredMixin,
                      SuccessMessageMixin,
                      DeleteView):
    template_name = "common/delete.html"
    success_url = reverse_lazy("labels_list_view")
    model = Label
    success_message = "Метка успешно удалена"
    extra_context = {
        "view_name": "labels_delete_view",
        "header_name": "Удаление метки",
    }

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "Невозможно удалить метку, потому что она используется",
            )
        return HttpResponseRedirect(self.get_success_url())
