from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView, ListView

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.mixins import DeletePermissionRequiredMixin
from task_manager.tasks.models import (
    Task,
    TaskLabel,
)
from task_manager.users.mixins import (
    AuthRequiredMixin,
)


class TasksListView(AuthRequiredMixin, ListView):
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = TaskFilter(
            self.request.GET,
            queryset=Task.objects.all(),
            request=self.request,
        )
        context["filter_form"] = filter.form
        context["tasks"] = filter.qs
        return context


# class TasksListView(AuthRequiredMixin, TemplateView):
#     template_name = "tasks/index.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         all_tasks = Task.objects.all()
#         task_filter = TaskFilter(
#             self.request.GET,
#             queryset=all_tasks,
#             request=self.request,
#         )
#         context["task_filter"] = task_filter
#         context["tasks"] = task_filter.qs
#         return context


class CreateTaskView(AuthRequiredMixin, CreateView):
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_list_view")
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class UpdateTaskView(AuthRequiredMixin, UpdateView):
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_list_view")
    model = Task
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_id"] = self.kwargs.get("pk")
        return context

    def form_valid(self, form):
        task_id = self.kwargs["pk"]

        with transaction.atomic():
            # получаем задачу
            task = Task.objects.get(id=task_id)

            # обновляем имя, описание, статус и исполнителя
            task.name = form.cleaned_data["name"]
            task.description = form.cleaned_data["description"]
            task.status = form.cleaned_data["status"]
            task.executor = form.cleaned_data["executor"]

            # чистим связи меток с данной задачей в промежуточной таблице
            labels = TaskLabel.objects.filter(task_id=task.id)
            labels.delete()

            # получаем из формы новые метки
            labels = form.cleaned_data["labels"]

            # создаем для задачи новые связи с метками в промежуточной таблице
            new_task_label_links = [
                TaskLabel(task_id=task.id, label_id=label.id) for label in labels  # noqa: E501
            ]
            TaskLabel.objects.bulk_create(new_task_label_links)

            # сохраняем задачу в базу
            task.save()

            messages.success(
                self.request,
                "Задача успешно изменена",
                extra_tags="alert alert-success",
            )
            return super().form_valid(form)


class DeleteTaskView(DeletePermissionRequiredMixin, DeleteView):
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_list_view")
    model = Task
    context_object_name = "task"

    def form_valid(self, form):
        success_url = self.get_success_url()
        with transaction.atomic():
            self.object.delete()
            messages.success(self.request, "Задача успешно удалена")
        return HttpResponseRedirect(success_url)


class DetailsTaskView(DetailView):
    template_name = "tasks/details.html"
    model = Task
    context_object_name = "task"
