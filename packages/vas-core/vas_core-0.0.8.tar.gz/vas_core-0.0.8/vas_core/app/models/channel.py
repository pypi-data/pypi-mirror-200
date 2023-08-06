import json

from django.db import models

from vas_core.app.models import BaseModelAbstract


class Channel(BaseModelAbstract, models.Model):
    code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255)
    shortcode = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.__str__()

    def save(self, keep_deleted=False, **kwargs):
        self.code = self.code.upper()
        self.shortcode = self.shortcode.upper()
        super(BaseModelAbstract, self).save(keep_deleted, **kwargs)

    def to_redis(self) -> str:
        data = {
            "code": self.code,
            "desc": self.description
        }
        return json.dumps(data)
