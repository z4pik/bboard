# Создаем новый обработчик контекста

from .models import SubRubric


def bboard_context_processor(request):
    """Обработчик, который будет формировать список подрубрик"""
    context = {}
    context['rubrics'] = SubRubric.objects.all()
    return context
