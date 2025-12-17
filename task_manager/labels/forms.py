from task_manager.labels.models import Label
from django import forms


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "id": "id_name",
                    "class": "form-control",
                    "placeholder": "Имя",
                },
            ),
        }
