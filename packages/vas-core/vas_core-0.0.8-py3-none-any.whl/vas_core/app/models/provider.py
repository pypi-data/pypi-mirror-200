import json

from django.db import models

from vas_core.app.models import LocalizationField, BaseModelAbstract

XML_API_TYPE = "XML"
JSON_API_TYPE = "JSON"
API_TYPES = (
    (XML_API_TYPE, XML_API_TYPE),
    (JSON_API_TYPE, JSON_API_TYPE),
)


class Provider(BaseModelAbstract, models.Model):
    name = LocalizationField()
    code = models.CharField(max_length=30)
    api_url = models.URLField(null=True, blank=True)
    api_type = models.CharField(max_length=10, choices=API_TYPES, null=False,
                                blank=False)
    auth_username = models.CharField(null=True, blank=True, max_length=255)
    auth_password = models.CharField(null=True, blank=True, max_length=255)
    auth_token = models.CharField(null=True, blank=True, max_length=255)
    notify = models.BooleanField(default=True)
    accounting_entry = models.OneToOneField("AccountingEntry",
                                            null=True, blank=True,
                                            on_delete=models.SET_NULL)

    @property
    def has_url(self) -> bool:
        return self.api_url not in (None, '')

    @property
    def is_json(self) -> bool:
        return self.api_type == JSON_API_TYPE

    @property
    def is_xml(self) -> bool:
        return self.api_type == XML_API_TYPE

    def to_redis(self) -> str:
        data = {
            "name": self.name,
            "code": self.code,
            "api_url": self.api_url,
            "api_type": self.api_type,
            "auth_username": self.auth_username,
            "auth_password": self.auth_password,
            "auth_token": self.auth_token,
            "notify": self.notify,
            "accounting_entry": self.accounting_entry if self.accounting_entry.to_dict() else None,
        }
        return json.dumps(data)
