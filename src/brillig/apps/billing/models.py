from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import date, datetime
from decimal import Decimal


class Account(models.Model):
    """A container for a customer's current balance, and billing history.
    """
    id = models.CharField(max_length=32, primary_key=True, db_index=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
    
    def __unicode__(self):
        return self.id


class Charge(models.Model):
    """A record of an amount (including applicable tariff) owed by a customer, for services received.
    """
    account = models.ForeignKey('Account', related_name='charges')
    description = models.CharField(max_length=350, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now)
    
    class Meta:
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')
    
    def __unicode__(self):
        return u'%.2f for %s' % (
            self.cost, self.description
        )


class PaymentStatus(models.Model):
    """Payment Gateway-defined status messages. E.g: 'Pending', 'Done', 'Failed' etc.
    """
    name = models.CharField(max_length=100, primary_key=True, db_index=True)
    
    class Meta:
        verbose_name = _('Payment status')
        verbose_name_plural = _('Payment statuses')
    
    def __unicode__(self):
        return self.name


class Payment(models.Model):
    """A payment made to offset an amount owed.
    """
    charge = models.OneToOneField('billing.Charge')
    account = models.ForeignKey(Account, related_name='payments')
    status = models.ForeignKey(PaymentStatus)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
    
    def __unicode__(self):
        return self.amount
