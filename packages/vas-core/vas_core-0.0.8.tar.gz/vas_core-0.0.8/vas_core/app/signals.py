from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from . import categories_redis_store, countries_redis_store, \
    billers_redis_store, channels_redis_store, biller_fields_redis_store, providers_redis_store
from .models import Category, Country, Biller, Channel, BillerField, Provider

#
__all__ = [
    'category_update_hook', 'category_delete_hook', 'country_update_hook',
    'country_delete_hook', 'biller_update_hook', 'biller_delete_hook',
    'biller_field_update_hook', 'biller_field_delete_hook',
    'channel_update_hook', 'channel_delete_hook'
]


@receiver(post_save, sender=Category)
def category_update_hook(sender, instance, **kwargs):
    if instance.is_active:
        categories_redis_store.store(instance.pk, instance.to_redis())
    else:
        categories_redis_store.delete(instance.pk)


@receiver(post_delete, sender=Category)
def category_delete_hook(sender, instance, **kwargs):
    categories_redis_store.delete(instance.pk)


@receiver(post_save, sender=Country)
def country_update_hook(sender, instance, **kwargs):
    countries_redis_store.store(instance.code, instance.to_redis())


@receiver(post_delete, sender=Country)
def country_delete_hook(sender, instance, **kwargs):
    countries_redis_store.delete(instance.code)


@receiver(post_save, sender=Biller)
def biller_update_hook(sender, instance, **kwargs):
    if instance.is_active:
        billers_redis_store.store(instance.biller_id, instance.to_redis())
    else:
        billers_redis_store.delete(instance.biller_id)


@receiver(post_delete, sender=Biller)
def biller_delete_hook(sender, instance, **kwargs):
    billers_redis_store.delete(instance.biller_id)


@receiver(post_save, sender=Channel)
def channel_update_hook(sender, instance, **kwargs):
    if instance.is_active and not instance.deleted:
        channels_redis_store.store(instance.shortcode, instance.to_redis())
    else:
        categories_redis_store.delete(instance.shortcode)


@receiver(post_delete, sender=Channel)
def channel_delete_hook(sender, instance, **kwargs):
    channels_redis_store.delete(instance.shortcode)


@receiver(post_save, sender=BillerField)
def biller_field_update_hook(sender, instance, **kwargs):
    # if not instance.deleted:
    biller_fields_redis_store.store(instance.biller.biller_id,
                                    instance.to_redis())
    # else:
    #     biller_fields_redis_store.delete(instance.biller_id)


@receiver(post_delete, sender=BillerField)
def biller_field_delete_hook(sender, instance, **kwargs):
    biller_fields_redis_store.delete(instance.biller.biller_id)


@receiver(post_save, sender=Provider)
def provider_update_hook(sender, instance, **kwargs):
    providers_redis_store.store(instance.id, instance.to_redis())


@receiver(post_delete, sender=Provider)
def provider_delete_hook(sender, instance, **kwargs):
    providers_redis_store.delete(instance.id)
