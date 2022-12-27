from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    email = models.EmailField('Почта пользователя', unique=True, max_length=254)
    confirmation_code = models.CharField(
        'Токен подтверждения', max_length=50, blank=True
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(choices=ROLES,
                            default=USER,
                            max_length=25,
                            blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
