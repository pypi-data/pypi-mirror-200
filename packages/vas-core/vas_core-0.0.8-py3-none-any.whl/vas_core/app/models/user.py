from django.contrib.auth.models import AbstractUser
from django.db import models

from .base import BaseModelAbstract


class User(AbstractUser, BaseModelAbstract):
    """
        Overrides django's default auth model
    """
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]
    
    email = models.EmailField(unique=True, null=False, blank=False)
    verificationMode = models.CharField(db_column='verificationMode',
                                        max_length=255, blank=True,
                                        null=True)
    user_country = models.ForeignKey("Country", models.CASCADE, null=True,
                                     blank=True)

    class Meta:
        db_table = 'Users'
