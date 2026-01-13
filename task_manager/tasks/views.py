from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django_filters.views import FilterView
from task_manager.common_views import BaseCreate, BaseUpdate, BaseDelete
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.mixins import DeletePermissionRequiredMixin
from task_manager.tasks.models import Task
from task_manager.users.mixins import AuthRequiredMixin


class BaseTasks:
    model = Task
    success_url = reverse_lazy("tasks_list_view")


class TasksListView(AuthRequiredMixin, FilterView):
    template_name = "tasks/index.html"
    model = Task
    filterset_class = TaskFilter
    context_object_name = "tasks"


class CreateTaskView(BaseTasks,
                     AuthRequiredMixin,
                     BaseCreate):
    form_class = TaskForm
    success_message = "Задача успешно создана"
    extra_context = {
        "view_name": "tasks_create_view",
        "header_name": "Создать задачу",
    }

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.author = self.request.user
            return super().form_valid(form)


class UpdateTaskView(BaseTasks,
                     AuthRequiredMixin,
                     BaseUpdate):
    form_class = TaskForm
    success_message = "Задача успешно изменена"
    extra_context = {
        "view_name": "tasks_update_view",
        "header_name": "Изменение задачи",
    }


class DeleteTaskView(BaseTasks,
                     DeletePermissionRequiredMixin,
                     BaseDelete):
    success_message = "Задача успешно удалена"
    extra_context = {
        "view_name": "tasks_delete_view",
        "header_name": "Удаление задачи",
    }


class DetailsTaskView(DetailView):
    template_name = "tasks/details.html"
    model = Task
    context_object_name = "task"
