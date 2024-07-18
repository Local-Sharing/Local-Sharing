from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Gender_Choices(models.TextChoices):
        Male = 'M', '남성'
        Female = 'F', '여성'

    nickname = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='meida/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=1, choices=Gender_Choices.choices)
    age = models.CharField(max_length=3)

    REQUIRED_FIELDS = ['nickname', 'gender', 'age']

    def __str__(self):
        return self.username