from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.users.mixins import AuthRequiredMixin
from task_manager.common_views import BaseCreate, BaseUpdate, BaseDelete


class BaseStatuses:
    model = Status
    success_url = reverse_lazy("statuses_list_view")


class StatusesListView(AuthRequiredMixin, ListView):
    template_name = "statuses/index.html"
    model = Status


class CreateStatusView(BaseStatuses, BaseCreate):
    form_class = StatusForm
    success_message = "Статус успешно создан"
    extra_context = {
        "view_name": "statuses_create_view",
        "header_name": "Создать статус",
    }


class UpdateStatusView(BaseStatuses, BaseUpdate):
    form_class = StatusForm
    success_message = "Статус успешно изменен"
    extra_context = {
        "view_name": "statuses_update_view",
        "header_name": "Изменение статуса",
    }


class DeleteStatusView(BaseStatuses, BaseDelete):
    success_message = "Статус успешно удален"
    extra_context = {
        "view_name": "statuses_delete_view",
        "header_name": "Удаление статуса",
    }

    def form_valid(self, form):
        try:
            super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "Невозможно удалить статус, потому что он используется",
            )
        return HttpResponseRedirect(self.get_success_url())