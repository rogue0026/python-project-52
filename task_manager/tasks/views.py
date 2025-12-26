from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django_filters.views import FilterView
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.mixins import DeletePermissionRequiredMixin
from task_manager.tasks.models import Task
from task_manager.users.mixins import AuthRequiredMixin


class TasksListView(AuthRequiredMixin, FilterView):
    template_name = "tasks/index.html"
    model = Task
    filterset_class = TaskFilter
    context_object_name = "tasks"


class CreateTaskView(AuthRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_list_view")
    model = Task
    form_class = TaskForm
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.author = self.request.user
            return super().form_valid(form)


class UpdateTaskView(AuthRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_list_view")
    model = Task
    form_class = TaskForm
    context_object_name = "task"
    success_message = "Задача успешно изменена"


class DeleteTaskView(DeletePermissionRequiredMixin,
                     SuccessMessageMixin,
                     DeleteView):
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_list_view")
    model = Task
    context_object_name = "task"
    success_message = "Задача успешно удалена"


class DetailsTaskView(DetailView):
    template_name = "tasks/details.html"
    model = Task
    context_object_name = "task"
