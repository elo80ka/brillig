from django import forms
from django.db.transaction import commit_on_success
from django.forms import models, widgets
from django.utils.translation import ugettext_lazy as _
from accounts.models import Customer, Service
from billing.models import Account
from form_utils.base import Form, ModelForm
import uuid

class CustomerForm(ModelForm):
    services = models.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=widgets.CheckboxSelectMultiple,
        help_text=_('Select all services this customer will be subscribed to.'))
    
    class Meta:
        model = Customer
        exclude = ('account',)
        widgets = {
            'address': widgets.Textarea,
        }
        
    @commit_on_success
    def save(self, commit=True):
        account = Account.objects.create(id=uuid.uuid4().hex)
        customer = super(CustomerForm, self).save(commit=False)
        customer.account = account
        if commit:
            customer.save()
            self.save_m2m()
        return customer

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        widgets = {
            'details': widgets.Textarea,
        }
