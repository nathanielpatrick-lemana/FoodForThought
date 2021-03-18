from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_staff = models.BooleanField('Is a staff member?', default=False)
    is_customer = models.BooleanField('Is a customer?', default=True)

    class Meta:
        db_table = 'auth_user'
