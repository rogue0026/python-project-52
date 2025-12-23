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
    template_name = "labels/create.html"
    success_url = reverse_lazy('labels_list_view')
    model = Label
    form_class = LabelForm
    success_message = "Метка успешно создана"


class UpdateLabelView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView):
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels_list_view")
    model = Label
    form_class = LabelForm
    success_message = "Метка успешно изменена"


class DeleteLabelView(AuthRequiredMixin,
                      SuccessMessageMixin,
                      DeleteView):
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels_list_view")
    model = Label
    context_object_name = "label"
    success_message = "Метка успешно удалена"

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "Невозможно удалить метку, потому что она используется",
            )
        return HttpResponseRedirect(self.get_success_url())
