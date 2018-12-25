from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile = models.CharField(max_length=30, verbose_name='用户手机号')

    class Meta:
        db_table = 'tb_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'