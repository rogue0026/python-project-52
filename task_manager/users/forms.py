from django import forms


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label="Имя:",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя",
            "id": "id_first_name",
        },
        ),
    )

    last_name = forms.CharField(
        label="Фамилия:",
        required=True,
        widget=forms.TextInput(attrs={
             "class": "form-control",
             "placeholder": "Фамилия",
             "id": "id_last_name",
        }),
    )

    username = forms.CharField(
        label="Имя пользователя:",
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя пользователя",
            "id": "id_username",
        }),
    )

    password1 = forms.CharField(
        label="Пароль",
        required=False,
        min_length=3,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "type": "password",
            "id": "id_password1",
        }),
    )

    password2 = forms.CharField(
        label="Подтверждение пароля:",
        required=False,
        min_length=3,
        widget=forms.TextInput(attrs={
            "class": "form-control mb-3",
            "type": "password",
            "id": "id_password2",
        }),
    )

    def clean_username(self):
        valid_symbols = "abcdefghijklmnopqrstuvwxyz0123456789@.+-_"
        data = self.cleaned_data['username']
        if len(data) > 150:
            raise forms.ValidationError("Имя пользователя не должно превышать 150 символов")  # noqa: E501

        for s in data.lower():
            if s not in valid_symbols:
                raise forms.ValidationError("Имя пользователя содержит недопустимые символы")  # noqa: E501

        return data

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if password2 != self.cleaned_data['password1']:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

