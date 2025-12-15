from django import forms
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class ExecutorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TaskForm(forms.Form):
    name = forms.CharField(
        label_suffix="",
        label="Имя",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя",
            "id": "id_name",
            "type": "text",
        }))

    description = forms.CharField(
        label_suffix="",
        label="Описание",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Описание",
            "id": "id_description",
            "rows": "5",
        })
    )

    status = forms.ModelChoiceField(
        label_suffix="",
        label="Статус",
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "id_status",
        })
    )
    status.label_from_instance = lambda obj: f"{obj.name}"

    executor = ExecutorChoiceField(
        label_suffix="",
        label="Исполнитель",
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "id_executor",
        })
    )

    labels = forms.ModelMultipleChoiceField(
        required=False,
        label_suffix="",
        label="Метки",
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "form-control",
            "id": "id_labels",
        })
    )
    labels.label_from_instance = lambda obj: f"{obj.name}"
