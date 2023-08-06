from django.db import models

from vas_core.app.models import BaseModelAbstract


class AccountConfig(BaseModelAbstract, models.Model):
    account = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)
    is_dynamic = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} - {self.account}"

    def __unicode__(self):
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "account": self.account,
            "desc": self.description,
            "is_dynamic": self.is_dynamic,
        }


class FeeAccountConfig(BaseModelAbstract, models.Model):
    account = models.ForeignKey("AccountConfig", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=5, max_digits=50, null=False,
                                 blank=False)
    is_percentage = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account} - {self.amount}{ self.is_percentage if '%' else ''}"

    def __unicode__(self):
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "account_config": self.account.to_dict(),
            "amount": self.amount,
            "is_percentage": self.is_percentage,
        }


class AccountingEntry(BaseModelAbstract, models.Model):
    settlement_account = models.ForeignKey("AccountConfig",
                                           on_delete=models.CASCADE)
    fees = models.ManyToManyField("FeeAccountConfig", null=True, blank=True)

    def to_dict(self) -> dict:
        _fees = []
        for fee in self.fees.all():
            _fees.append(fee.to_dict())
        return {
            "settlement_account": "",
            "fees": _fees
        }
