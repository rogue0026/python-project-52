from django import forms


class LabelForm(forms.Form):
    name = forms.CharField(
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={
            "id": "id_name",
            "class": "form-control",
            "placeholder": "Имя",
        })
    )