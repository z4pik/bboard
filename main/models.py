from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name="Прошел активацию?")
    is_messages = models.BooleanField(default=True,
                                      verbose_name="Слать-ли оповещения о новых сообщениях?")

    class Meta(AbstractUser.Meta):
        pass
