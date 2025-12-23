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
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status
    form_class = StatusForm
    success_message = "Статус успешно создан"


class UpdateStatusView(SuccessMessageMixin, UpdateView):
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status
    form_class = StatusForm
    success_message = "Статус успешно изменен"
    context_object_name = "status"


class DeleteStatusView(DeleteView):
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status
    context_object_name = "status"

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, "Статус успешно удален")
        except ProtectedError:
            messages.error(
                self.request,
                "Невозможно удалить статус, потому что он используется",
            )
        return HttpResponseRedirect(success_url)
