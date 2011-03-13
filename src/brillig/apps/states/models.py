from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    code = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        
    def __unicode__(self):
        return self.name


class State(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=30)
    
    class Meta:
        ordering = ('name',)
        verbose_name = _('Nigerian State')
        verbose_name_plural = _('Nigerian States')
        
    def __unicode__(self):
        return self.name


class LGA(models.Model):
    state = models.ForeignKey(State, related_name='local_govt_areas')
    name = models.CharField(max_length=30)
        
    class Meta:
        ordering = ('state', 'name',)
        verbose_name = _('Local Government Area')
        verbose_name_plural = _('Local Government Areas')
        
    def __unicode__(self):
        return self.name
