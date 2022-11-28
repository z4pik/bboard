from django.contrib import admin
import datetime

from .forms import SubRubricForm
from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage
from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


send_activation_notifications.short_description = \
    'Отправка писем с требованиями активации'


class NonActivatedFilter(admin.SimpleListFilter):
    """Фильтр пользователей"""
    title = "Прошли активацию?"
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('week', 'Не прошли более недели'),
            ('non_activated', 'Не прошли'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'non_activated':
            return queryset.filter(is_active=False, is_activated=False)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
    """Отображение полей в админке"""
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonActivatedFilter,)
    fields = (
        ('username', 'email'), ('first_name', 'last_name'),
        ('is_messages', 'is_active', 'is_activated'),
        ('is_staff', 'is_superuser'),
        'groups', 'user_permissions',
        ('last_login', 'date_joined')
    )
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


admin.site.register(AdvUser, AdvUserAdmin)


class SubRubricInline(admin.TabularInline):
    """Позволит добавлять несколько подрубрик внутри модели рубрики"""
    model = SubRubric


class SubRubricAdmin(admin.ModelAdmin):
    """Присваиваем кастомную форму для подрубрик"""
    form = SubRubricForm


admin.site.register(SubRubric, SubRubricAdmin)


class SuperRubricAdmin(admin.ModelAdmin):
    # Исключаем поле, чтобы пользователь не мог в рубрике создать надрубрику
    exclude = ('super_rubric',)
    # Даем возможность пользователю сразу заполнить Рубрику, подрубриками
    inlines = (SubRubricInline,)


admin.site.register(SuperRubric, SuperRubricAdmin)


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price',
              'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline,)


admin.site.register(Bb, BbAdmin)
