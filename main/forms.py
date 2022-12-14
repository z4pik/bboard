from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .apps import user_registered
from .models import AdvUser, SubRubric, SuperRubric, Bb, AdditionalImage, Comment


class ChangeUserInfoForm(forms.ModelForm):
    """Форма правки основных сведений"""
    # Делаем поле email - обязательным (именно поэтому явно объявляем)
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = {'username', 'email', 'first_name', 'last_name',
                  'is_messages'}


class RegisterUserForm(forms.ModelForm):
    """Форма для занесения сведений о новом пользователе"""
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Введите тот-же пароль ещё раз для проверки')

    def clean_password1(self):
        """Проверка пароля на корректность"""
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        """Проверяем совпадают ли обо введенных пароля"""
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password2 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        """Сохраняем пользователя"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False  # Является ли пользователь активным
        user.is_activated = False  # Выполнил ли пользователь процедуру активации

        # Сохраняем в записи закодированный пароль
        if commit:
            user.save()
        # Отсылаем сигнал, чтобы отослать пользователю письмо с требованием активации
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'is_messages')


class SubRubricForm(forms.ModelForm):
    # У подрубрики сделаем поле рубрики(super_rubric) - обязательным
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(), empty_label=None,
        label='Надрубрика', required=True
    )

    class Meta:
        model = SubRubric
        fields = '__all__'


class SearchForm(forms.Form):
    """Форма для поиска"""
    keyword = forms.CharField(required=False, max_length=20, label='')


class BbForm(forms.ModelForm):
    """Форма вывода самого объявления"""
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


# Встроенный набор форм
AiFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    captcha_ = CaptchaField(label='Введите текст с картинки',
                            error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}

