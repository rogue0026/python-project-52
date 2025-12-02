from django.contrib import messages
from django.shortcuts import redirect, reverse
from task_manager.tasks.models import Task


class DeletePermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user_id = request.user.id
        task_id = kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        if task.author.id != user_id:
            messages.error(
                request,
                "Задачу может удалить только её автор",
                "alert alert-danger",
            )
            return redirect(reverse("tasks_list_view"))

        return super().dispatch(request, *args, **kwargs)
