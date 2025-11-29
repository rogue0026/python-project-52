from django import forms


class StatusForm(forms.Form):
    name = forms.CharField(
        label="Имя:",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя",
            "id": "id_name",
        },
        ),
    )