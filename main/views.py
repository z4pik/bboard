from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .models import AdvUser
from .forms import ChangeUserInfoForm


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
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'

