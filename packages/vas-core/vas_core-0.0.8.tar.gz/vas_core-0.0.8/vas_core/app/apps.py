from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'vas_core.app'

    def ready(self):
        from .signals import (
            category_delete_hook, category_update_hook,
            channel_delete_hook, channel_update_hook, biller_delete_hook,
            biller_update_hook, country_delete_hook, country_update_hook,
            biller_field_update_hook, biller_field_delete_hook
        ) # noqa
