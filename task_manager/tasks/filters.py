import django_filters
from django import forms
from django.contrib.auth.models import User
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from task_manager.tasks.forms import ExecutorChoiceField
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class ExecutorFilter(django_filters.ModelChoiceFilter):
    field_class = ExecutorChoiceField


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        label="Статус",
        label_suffix="",
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={
            "id": "id_status",
            "class": "form-control",
        }),
    )

    executor = ExecutorFilter(
        label="Исполнитель",
        label_suffix="",
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            "id": "id_executor",
            "class": "form-control",
        }),
    )

    label = ModelChoiceFilter(
        label="Метка",
        label_suffix="",
        field_name="labels",
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={
            "id": "id_label",
            "class": "form-control",
        }),
    )

    only_my_tasks = BooleanFilter(
        label="Только свои задачи",
        label_suffix="",
        method="filter_only_my_tasks",
        widget=forms.CheckboxInput(attrs={
            "id": "id_self_tasks",
            "class": "form-check-input",
        }),
    )

    def filter_only_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

