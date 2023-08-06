import json

from django.db import models

from vas_core.app.models import BaseModelAbstract


class BillerField(BaseModelAbstract, models.Model):
    biller = models.OneToOneField("Biller", on_delete=models.CASCADE)
    validation_field = models.TextField(blank=True)
    klass = models.URLField(null=True, blank=True)
    requery_url = models.URLField(null=True, blank=True)
    fields_json = models.JSONField(null=False, blank=False)

    def __str__(self):
        return f"{self.biller}'s Fields"

    def __unicode__(self):
        return self.__str__()

    def to_redis(self):
        data = {
            "validation_field": self.validation_field,
            "klass": self.klass,
            "requery_url": self.requery_url,
            "fields_json": self.fields_json,
        }
        return json.dumps(data)
