from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_not_me
from .constants import (
    MAX_LENGTH_USERNAME,
    MAX_LENGTH_EMAIL,
)


class User(AbstractUser):
    """Модель пользователя"""

    class Role(models.TextChoices):
        USER = ('user', 'Пользователь')
        MODERATOR = ('moderator', 'Модератор')
        ADMIN = ('admin', 'Администратор')

    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            validate_not_me,
        ],
    )
    email = models.EmailField(
        'Почта', max_length=MAX_LENGTH_EMAIL, unique=True
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=max(len(value) for value, _ in Role.choices),
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_user(self):
        """Проверка роли пользователя"""
        return self.role == self.Role.USER

    @property
    def is_moderator(self):
        """Проверка роли модератора"""
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        """Проверка роли администратора"""
        return (
            self.role == self.Role.ADMIN or self.is_superuser or self.is_staff
        )

    def __str__(self):
        return self.username
