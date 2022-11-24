from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView


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

