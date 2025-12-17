from django import forms
from django.contrib.auth.models import User
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        label="Статус",
        # label_suffix="",
        queryset=Status.objects.all()
    )

    executor = ModelChoiceFilter(
        label="Исполнитель",
        # label_suffix="",
        queryset=User.objects.all(),
    )

    label = ModelChoiceFilter(
        label="Метка",
        # label_suffix="",
        field_name="labels",
        queryset=Label.objects.all(),
    )

    self_tasks = BooleanFilter(
        label="Только свои задачи",
        # label_suffix="",
        method="filter_only_my_tasks",
    )

    def filter_only_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

