from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
        UNKNOWN = ("unknown", "Unknown")

    avatar = models.ImageField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
    )
    gender = models.CharField(
        max_length=10, choices=GenderChoices.choices, default=GenderChoices.UNKNOWN
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'
    )