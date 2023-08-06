import json

from django.db import models
from vas_core.app.models.base import BaseModelAbstract, LocalizationField


class Category(BaseModelAbstract, models.Model):
    description = LocalizationField()
    country = models.ForeignKey("Country", on_delete=models.DO_NOTHING,
                                null=True, blank=True)
    is_active = models.BooleanField(default=True)
    requires_consent = models.BooleanField(default=False)

    def __str__(self):
        x = []
        for k, v in self.description:
            x.append(f"{k}: {v}")
        return ',\n'.join(x)

    def __unicode__(self):
        return self.__str__()

    class Meta:
        ordering = ('description', )

    def get_description(self, lang) -> str:
        return self.description.get(lang.lower())

    def to_redis(self) -> str:
        data = {
            "id": self.id,
            "desc": self.description,
            "country_code": self.country.code,
            "requires_consent": self.requires_consent,
        }
        return json.dumps(data)
