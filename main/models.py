from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    """Модель пользователя"""
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name="Прошел активацию?")
    is_messages = models.BooleanField(default=True,
                                      verbose_name="Слать-ли оповещения о новых сообщениях?")

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    """Модель рубрик"""
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric',
                                     on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Надрубрика')


class SuperRubricManager(models.Manager):
    """Диспетчер записей, который укажет все необходимые способы фильтрации"""
    def get_queryset(self):
        # Будет выбирать только те, в которых поле super_rubric будет пустым -> Надрубрики
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    """
        Прокси-модель для работы с надрубриками, производную от Rubric
        (прокси-модель позволяет менять лишь функциональную модели, но не набор объявленных в ней полей)
        Она будет обрабатывать только надрубрики
    """
    objects = SuperRubricManager()  # Устанавливаем кастомный диспетчер записей в кач-ве основного

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    """
    Кастомный диспетчер записей, который будет отбирать
    лишь записи с непустым полем super_rubric (т.е подрубрики)
    """
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        # Представление будет в виде - <название рубрики> - <название подрубрики>
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'
