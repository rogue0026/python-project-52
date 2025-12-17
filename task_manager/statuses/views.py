from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.users.mixins import AuthRequiredMixin


class StatusesListView(AuthRequiredMixin, ListView):
    template_name = "statuses/index.html"
    model = Status


class CreateStatusView(CreateView):
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status
    form_class = StatusForm

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class UpdateStatusView(UpdateView):
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status
    form_class = StatusForm

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменен")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_id"] = self.kwargs.get("pk")
        return context


class DeleteStatusView(DeleteView):
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses_list_view")
    model = Status

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
            messages.success(self.request, "Статус успешно удален")
        except ProtectedError:
            messages.error(self.request, "Невозможно удалить статус, потому что он используется")

        return HttpResponseRedirect(success_url)
