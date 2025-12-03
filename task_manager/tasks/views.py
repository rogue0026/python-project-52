from django.contrib import messages
from django.db import transaction
from django.shortcuts import (
    redirect,
    render,
    reverse,
)
from django.views import View

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
from task_manager.users.middleware import (
    AuthRequiredMixin,
)


class TasksListView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_tasks = Task.objects.all()

        tasks_filter = TaskFilter(
            request.GET,
            queryset=all_tasks,
            request=request,
        )

        return render(
            request,
            "tasks/index.html",
            context={
                "tasks_filter": tasks_filter,
                "tasks": tasks_filter.qs,
            }
        )


class CreateTaskView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(
            request,
            "tasks/create.html",
            context={
                "form": form,
            }
        )

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "tasks/create.html",
                context={
                    "form": form,
                },
                status=422,
            )

        with transaction.atomic():
            task = Task(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                executor=form.cleaned_data["executor"],
                author_id=request.user.id,
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
                request,
                "Задача успешно создана",
                extra_tags="alert alert-success",
            )

        return redirect(reverse("tasks_list_view"))


class UpdateTaskView(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = int(kwargs.get("pk"))
        task = Task.objects.get(id=task_id)

        labels_ids = TaskLabel.objects.filter(
            task_id=task_id).values_list("label_id", flat=True)

        linked_labels = Label.objects.filter(id__in=labels_ids)

        form = TaskForm({
            "name": task.name,
            "description": task.description,
            "status": task.status,
            "executor": task.executor,
            "labels": linked_labels,
        })

        return render(
            request,
            "tasks/update.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "users/update.html",
                context={
                    "form": form,
                },
                status=422,
            )

        task_id = int(kwargs.get("pk"))
        with transaction.atomic():
            # получаем таску
            task = Task.objects.get(id=task_id)

            # копируем имя описание статус и исполнителя
            task.name = form.cleaned_data["name"]
            task.description = form.cleaned_data["description"]
            task.status = form.cleaned_data["status"]
            task.executor = form.cleaned_data["executor"]

            # удаляем старые теги
            old_labels = task.labels_set.all()
            print(old_labels.values())
            old_labels.delete()

            # получаем из формы новые теги
            labels = form.cleaned_data["labels"]

            # создаем для таски новые связи с тегами
            labels_ids = labels.values_list("id", flat=True)
            new_task_labels = [
                TaskLabel(task_id=task.id, label_id=label_id,)
                for label_id in labels_ids
            ]
            TaskLabel.objects.bulk_create(new_task_labels)

            messages.success(
                request,
                "Задача успешно изменена",
                extra_tags="alert alert-success",
            )

        return redirect(reverse("tasks_list_view"))


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
