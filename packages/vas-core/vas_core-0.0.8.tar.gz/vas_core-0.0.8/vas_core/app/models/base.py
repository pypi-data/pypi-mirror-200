from django.conf import settings
from django.db import models
from safedelete.models import SafeDeleteModel


class BaseModelAbstract(SafeDeleteModel):
    old_id = models.CharField(null=True, blank=True, max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                                   blank=True, null=True)
    
    deleted = models.BooleanField(default=False)
    deleted_by_id = models.CharField(blank=True, null=True, max_length=255)
    
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ('-created_at', )

    def delete(self, by=None, force_policy=None, **kwargs):
        self.deleted_by_id = by
        self.deleted = True
        super(BaseModelAbstract, self).delete(force_policy, **kwargs)

    def undelete(self, force_policy=None, **kwargs):
        self.deleted_by_id = None
        self.deleted = False
        super(BaseModelAbstract, self).undelete(force_policy, **kwargs)

    def to_redis(self) -> str:
        raise NotImplemented()


class LocalizationField(models.JSONField):
    def __init__(
            self,
            verbose_name=None,
            name=None,
            encoder=None,
            decoder=None,
            **kwargs,
    ):
        super(LocalizationField, self).__init__(verbose_name=verbose_name,
                                                name=name, encoder=encoder,
                                                decoder=decoder, null=False,
                                                blank=False)
