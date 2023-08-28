from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Переопределенный класс пользователя. """

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Электронная почта',
        help_text='Введите электронную почту',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
