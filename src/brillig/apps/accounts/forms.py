from django import forms
from django.conf import settings
from django.db import transaction
from django.forms import fields, models, widgets
from django.utils.translation import ugettext_lazy as _
from accounts.models import Customer, Service, Usage
from accounts.messaging import customer_created
from billing.models import Account
from form_utils.base import Form, ModelForm
import csv
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
        
    @transaction.commit_on_success
    def save(self, commit=True):
        if not self.instance:
            # We're dealing with a new customer.
            account = Account.objects.create(id=uuid.uuid4().hex)
            customer = super(CustomerForm, self).save(commit=False)
            customer.account = account    
            if commit:
                customer.save()
                self.save_m2m()
            # Pop this customer in our queue:
            customer_dict = models.model_to_dict(customer)
            customer_created(customer_dict)
            # Return our brand-new customer:
            return customer
        else:
            return super(CustomerForm, self).save(commit=commit)

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        widgets = {
            'details': widgets.Textarea,
        }
    
class UsageForm(Form):
    file = fields.FileField(label=u'Select usage file (CSV)',
        help_text=_('You can download a <a href="%sfiles/sample-usage.csv">sample usage file</a>.' % settings.STATIC_URL))
    
    def clean_file(self):
        uploaded = self.cleaned_data.get('file')
        if uploaded and uploaded.content_type != 'text/csv':
            raise forms.ValidationError(u'Usage file should be a CSV file.')
        return uploaded
    
    @transaction.commit_manually
    def save(self):
        # Note: For now, I don't attempt to filter out non-existent customers
        #       or services -- be a good lad, and don't send me crap :|
        #       I'll fix this soon as I can write a more efficient import query.
        batch = uuid.uuid4().hex
        rdr = csv.reader(self.cleaned_data['file'].file)
        headers = rdr.next()
        try:
            for row in rdr:
                kwargs = dict(zip(headers, row))
                kwargs['batch'] = batch
                Usage.objects.create(**kwargs)
            transaction.commit()
        except:
            transaction.rollback()
            raise
