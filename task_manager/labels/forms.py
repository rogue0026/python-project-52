from django import forms


class LabelForm(forms.Form):
    name = forms.CharField(
        required=True,
        label_suffix="",
        label="Имя",
        widget=forms.TextInput(attrs={
            "id": "id_name",
            "class": "form-control",
            "placeholder": "Имя",
        })
    )