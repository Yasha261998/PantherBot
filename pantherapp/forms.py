from django import forms


class LoginForm(forms.Form):
    """Форма авторизации"""
    username = forms.CharField(min_length=5, max_length=64,
                               error_messages={'invalid': "Пароль должен содержать от 5 до 64 символов"},
                               label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=5, max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               error_messages={'invalid': "Пароль должен содержать от 5 до 32 символов"},
                               label="Пароль")
    remember = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type': 'checkbox'}), required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username or '.' in username or ',' in username or ' ' in username:
            raise forms.ValidationError('Имя пользователя не должно содержать символы: @ , . и пробелы')
        return username
