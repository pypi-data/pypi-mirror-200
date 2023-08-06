from django.db import models


class Localization(models.Model):
    lang = models.CharField(max_length=2, null=False, blank=False)
    key = models.CharField(max_length=255, null=False, blank=False,
                           unique=True, db_index=True)
    value = models.TextField(blank=False, null=False)
