from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from task_manager.tasks.models import Task


class DeletePermissionRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user_id = self.request.user.id
        task_id = self.kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        return task.author.id == user_id

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Задачу может удалить только ее автор",
        )
        return redirect(reverse_lazy("tasks_list_view"))