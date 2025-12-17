from django import forms
from django.contrib.auth.models import User
from django_filters import (
    BooleanFilter,
    FilterSet,
    ModelChoiceFilter
)

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        label="Статус",
        queryset=Status.objects.all()
    )

    executor = ModelChoiceFilter(
        label="Исполнитель",
        queryset=User.objects.all(),
    )

    label = ModelChoiceFilter(
        label="Метка",
        field_name="labels",
        queryset=Label.objects.all(),
    )

    self_tasks = BooleanFilter(
        label="Только свои задачи",
        method="filter_only_my_tasks",
        widget=forms.CheckboxInput(),
    )

    def filter_only_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

