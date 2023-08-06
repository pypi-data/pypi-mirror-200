from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "country")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "first_name", "last_name",
                           "country", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "country", "is_staff",
                    "is_superuser", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups",
                   "country")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email", "first_name")
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


User_ = get_user_model()

admin.site.register(User_, UserAdmin)
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(AccountConfig)
admin.site.register(FeeAccountConfig)
admin.site.register(AccountingEntry)
admin.site.register(Biller)
admin.site.register(BillerField)
admin.site.register(Provider)
admin.site.register(Channel)
admin.site.register(Request)
