from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    """Кастомный класс для пользователя"""

    id_telegram = models.IntegerField("ID пользователя в Telegram")
    password = models.CharField("Пароль", max_length=100)
    REQUIRED_FIELDS = ['id_telegram']
