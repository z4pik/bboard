from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from .utilities import get_timestamp_path, send_new_comment_notification


class AdvUser(AbstractUser):
    """Модель пользователя"""
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name="Прошел активацию?")
    is_messages = models.BooleanField(default=True,
                                      verbose_name="Слать-ли оповещения о новых сообщениях?")

    def delete(self, *args, **kwargs):
        """При удалении пользователя удаляем все связанные с ним объявления """
        for bb in self.bb_set_all():
            bb.delete()
        super().delete(*args, **kwargs)

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
    """Модель подрубрики"""
    objects = SubRubricManager()

    def __str__(self):
        # Представление будет в виде - <название рубрики> - <название подрубрики>
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class Bb(models.Model):
    """Модель рубрики"""
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT,
                               verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    contacts = models.TextField(verbose_name='Контакты')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
                               verbose_name='Автор')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """Перед удалением текущей записи мы перебираем т удаляем все связанные дополнительные иллюстрации"""
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE,
                           verbose_name='Объявления')
    image = models.ImageField(upload_to=get_timestamp_path,
                              verbose_name='Изображения')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


class Comment(models.Model):
    """Модель комментария"""
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE,
                           verbose_name='Объявления')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликован')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    """Отправка оповещений пользователю о новом комметарии"""
    author = kwargs['instance'].bb.author
    if kwargs['created'] and author.is_messages:
        send_new_comment_notification(kwargs['instance'])


post_save.connect(post_save_dispatcher, sender=Comment)
