from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=USER,
        blank=True
    )

