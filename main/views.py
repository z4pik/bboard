from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy

from .models import AdvUser
from .utilities import signer
from .forms import ChangeUserInfoForm, RegisterUserForm


def index(request):
    # Главная
    return render(request, 'main/index.html')


def other_page(request, page):
    try:
        # Пытаемся загрузить страницу, если она найдена, формируем ответ с этим шаблоном
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        # Если страница не найдена, даём 404
        raise Http404
    # В любом случае возвращаем ответ
    return HttpResponse(template.render(request=request))


class BbLoginView(LoginView):
    # Логин
    template_name = 'main/login.html'


@login_required
def profile(request):
    # Профиль пользователя
    return render(request, 'main/profile.html')


class BbLogoutView(LoginRequiredMixin, LogoutView):
    """Страница выхода должна быть доступна только зарегистрированным пользователям, которые выполнили вход.
    Поэтому я и добавил LoginRequiredMixin """
    template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Изменение информации о пользователе"""
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    # setup - Данный метод выполняется в самом начале исполнения контроллера-класса
    # и получает объект запроса в качестве одного из параметров
    def setup(self, request, *args, **kwargs):
        # Извлечем ключ пользователя и сохраним
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    # Извлечение исправляемой записи
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BbPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """Сброс пароля"""
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


class RegisterUserView(CreateView):
    """Регистрация пользователя"""
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    """Вывод ответа об успешной регистрации"""
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    """Активация пользователя"""
    try:
        # Извлекаем имя пользователя из полученного подписанного идентификатора
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    # Сохраняем ключ текущего пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        print(request)
        return super().setup(request, *args, **kwargs)

    # Перед удалением пользователя необходимо сделать выход
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    # Отыскали по ключу пользователя и удалили его
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


