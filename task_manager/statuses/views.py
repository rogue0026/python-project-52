from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.users.mixins import AuthRequiredMixin


class StatusesListView(AuthRequiredMixin, ListView):
    template_name = "statuses/index.html"
    model = Status


class CreateStatusView(SuccessMessageMixin, CreateView):
    template_name = "common/create.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status
    form_class = StatusForm
    success_message = "Статус успешно создан"
    extra_context = {
        "view_name": "statuses_create_view",
        "header_name": "Создать статус",
    }


class UpdateStatusView(SuccessMessageMixin, UpdateView):
    template_name = "common/update.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status
    form_class = StatusForm
    success_message = "Статус успешно изменен"
    context_object_name = "status"
    extra_context = {
        "view_name": "statuses_update_view",
        "header_name": "Изменение статуса",
    }


class DeleteStatusView(SuccessMessageMixin,
                       DeleteView):
    template_name = "common/delete.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status
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