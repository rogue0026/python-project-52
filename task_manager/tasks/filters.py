from django import forms
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        label="Статус",
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={
            "id": "id_status",
            "class": "form-control",
        }),
    )

    executor = ModelChoiceFilter(
        label="Исполнитель",
        queryset=User.objects.all().annotate(
            full_name=Concat(
                "first_name",
                Value(" "),
                "last_name",
            )),
        widget=forms.Select(attrs={
            "id": "id_executor",
            "class": "form-control",
        }),
    )

    label = ModelChoiceFilter(
        label="Метка",
        field_name="labels",
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={
            "id": "id_executor",
            "class": "form-control",
        }),
    )

    only_my_tasks = BooleanFilter(
        label="Только мои задачи",
        method="filter_only_my_tasks",
        widget=forms.CheckboxInput(attrs={
            "id": "id_only_my_tasks",
            "class": "form-check-input",
        }),
    )

    def filter_only_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
