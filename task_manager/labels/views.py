from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from task_manager.common_views import BaseCreate, BaseUpdate, BaseDelete
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.users.mixins import AuthRequiredMixin


class BaseLabels:
    success_url = reverse_lazy('labels_list_view')
    model = Label


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"


class CreateLabelView(BaseLabels,
                      AuthRequiredMixin,
                      BaseCreate):
    form_class = LabelForm
    success_message = "Метка успешно создана"
    extra_context = {
        "view_name": "labels_create_view",
        "header_name": "Создать метку",
    }


class UpdateLabelView(BaseLabels,
                      AuthRequiredMixin,
                      BaseUpdate):
    form_class = LabelForm
    success_message = "Метка успешно изменена"
    extra_context = {
        "view_name": "labels_update_view",
        "header_name": "Изменение метки",
    }


class DeleteLabelView(BaseLabels,
                      AuthRequiredMixin,
                      BaseDelete):
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
