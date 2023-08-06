from django.conf import settings
from django.db import models

from vas_core.app.models import BaseModelAbstract


class Request(BaseModelAbstract, models.Model):
    action = models.CharField(max_length=30)
    description = models.TextField()
    payload = models.JSONField(null=True, blank=True)
    service_url = models.URLField(null=False, blank=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
                                    null=True, blank=True,
                                    related_name="approved_request_set")

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.__str__()

    @property
    def is_approved(self):
        return bool(self.approved_by)
