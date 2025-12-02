from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField()
    description = models.CharField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_tasks")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks_for_execution")
    created_at = models.DateTimeField(auto_now_add=True)


class TaskLabel(models.Model):
    pk = models.CompositePrimaryKey("task_id", "label_id")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="labels_set")
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
