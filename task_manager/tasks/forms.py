from django.db.models import Value
from django import forms

from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from django.db.models.functions import Concat


class TaskForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя",
            "id": "id_name",
            "type": "text",
        }))

    description = forms.CharField(
        label="Описание",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Описание",
            "id": "id_description",
        })
    )

    status = forms.ModelChoiceField(
        label="Статус",
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "id_status",
        })
    )
    status.label_from_instance = lambda obj: f"{obj.name}"

    executor = forms.ModelChoiceField(
        label="Исполнитель",
        queryset=User.objects.all().annotate(
            full_name=Concat(
                "first_name",
                Value(" "),
                "last_name",
            )),
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "id_status",
        })
    )
    executor.label_from_instance = lambda obj: f"{obj.full_name}"

    labels = forms.ModelMultipleChoiceField(
        required=False,
        label="Метки",
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "form-control",
            "id": "id_labels",
        })
    )
    labels.label_from_instance = lambda obj: f"{obj.name}"
