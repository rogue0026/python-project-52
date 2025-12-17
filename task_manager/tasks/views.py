from django.contrib import messages
from django.db import transaction
from django.shortcuts import (
    redirect,
    render,
    reverse,
)
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView

from task_manager.labels.models import (
    Label,
)
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.middleware import DeletePermissionRequiredMixin
from task_manager.tasks.models import (
    Task,
    TaskLabel,
)
from task_manager.users.mixins import (
    AuthRequiredMixin,
)


class TasksListView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_tasks = Task.objects.all()

        task_filter = TaskFilter(
            request.GET,
            queryset=all_tasks,
            request=request
        )

        return render(
            request,
            "tasks/index.html",
            context={
                "task_filter": task_filter,
                "tasks": task_filter.qs,
            }
        )


class CreateTaskView(AuthRequiredMixin, FormView):
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_list_view")

    def get_form_class(self):
        return TaskForm

    def form_valid(self, form):
        with transaction.atomic():
            task = Task(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                executor=form.cleaned_data["executor"],
                author_id=self.request.user.id,
            )
            task.save()
            labels = form.cleaned_data.get("labels")
            labels_ids = labels.values_list("id", flat=True)
            task_labels = [TaskLabel(
                task_id=task.id,
                label_id=label_id,
            ) for label_id in labels_ids]
            TaskLabel.objects.bulk_create(task_labels)
            messages.success(
                self.request,
                "Задача успешно создана",
                extra_tags="alert alert-success",
            )
            return super().form_valid(form)


class UpdateTaskView(AuthRequiredMixin, FormView):
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_list_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_id"] = self.kwargs.get("pk")

        return context

    def get_initial(self):
        task_id = self.kwargs["pk"]
        task = Task.objects.get(id=task_id)
        labels = task.labels.all()
        return {
            "name": task.name,
            "description": task.description,
            "status": task.status,
            "executor": task.executor,
            "labels": labels,
        }

    def get_form_class(self):
        return TaskForm

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


class DeleteTaskView(DeletePermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = int(kwargs.get("pk"))
        task = Task.objects.get(id=task_id)
        return render(
            request,
            "tasks/delete.html",
            context={
                "task_name": task.name,
                "task_id": task.id,
            },
        )

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            task_id = int(kwargs.get("pk"))
            task = Task.objects.get(id=task_id)
            # удаляем задачу
            task.delete()
            # теперь находим и удаляем связи между тегами и задачами
            task_label_links = TaskLabel.objects.filter(task_id=task.id)
            task_label_links.delete()
            messages.success(
                request,
                "Задача успешно удалена",
                extra_tags="alert alert-success",
            )
        return redirect(reverse("tasks_list_view"))


class DetailsTaskView(View):
    def get(self, request, *args, **kwargs):
        task_id = int(kwargs.get("pk"))
        task = Task.objects.get(id=task_id)

        task_labels = TaskLabel.objects.filter(
            task_id=task_id).values_list("label_id", flat=True)

        label_names = Label.objects.filter(
            id__in=task_labels).values_list("name", flat=True)

        return render(
            request,
            "tasks/details.html",
            context={
                "task": task,
                "task_labels": label_names,
            },
        )
