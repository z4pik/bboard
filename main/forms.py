from django import forms

from .models import AdvUser


class ChangeUserInfoForm(forms.ModelForm):
    """Форма правки основных сведений"""
    # Делаем поле email - обязательным (именно поэтому явно объявляем)
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = {'username', 'email', 'first_name', 'last_name',
                  'is_messages'}

