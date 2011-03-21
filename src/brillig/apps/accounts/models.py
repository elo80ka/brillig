from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


class Customer(models.Model):
    msisdn = models.CharField(verbose_name=_('Phone number'), max_length=13, primary_key=True, db_index=True)
    account = models.OneToOneField('billing.Account')
    services = models.ManyToManyField('Service', related_name='customers')
    name = models.CharField(verbose_name=_('Full name'), max_length=100, blank=True)
    address = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    
    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
    
    def __unicode__(self):
        return self.msisdn


class Service(models.Model):
    code = models.CharField(max_length=50, primary_key=True, db_index=True,
        help_text=_("This is how you'll identify the service internally."))
    name = models.CharField(max_length=250, help_text=_("This should be a friendlier name for your customers."))
    rate = models.DecimalField(verbose_name=_('Service cost (in Naira)'), max_digits=10, decimal_places=2)
    details = models.CharField(verbose_name=_('Additional details'), max_length=250, blank=True,
        help_text=_("For example, a short description of this service."))
    
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
    
class Usage(models.Model):
    batch = models.CharField(max_length=32, db_index=True)
    customer = models.ForeignKey(Customer, related_name='usage')
    service = models.ForeignKey(Service, related_name='usage')
    used_at = models.DateTimeField(default=datetime.now)
    
    class Meta:
        verbose_name = _('Service Usage Record')
        verbose_name_plural = _('Service Usage Records')
        ordering = ('used_at',)
        
    def __unicode__(self):
        return u'%s received %s on %s' % (
            self.customer, self.service, self.used_at
        )
    