from piston.handler import BaseHandler
from piston.utils import rc, require_mime, validate
from piston.utils import FormValidationError
from api.resource import Resource
from accounts.models import Customer, Service
from accounts.forms import CustomerForm, ServiceForm

class CustomerHandler(BaseHandler):
    """
    Provides a REST API for managing Customer accounts and Subscriptions.
    """
    allowed_methods = ('GET', 'POST', 'PUT',)
    model = Customer
    fields = (
        'msisdn',
        'name',
        'address',
        'created_at',
        ('account',
            ('id', 'balance',)
        ),
        ('services',
            ('code', 'name',)
        ),
    )
    
    @require_mime('json')
    @validate(CustomerForm, 'data')
    def create(self, request):
        form = request.form
        return form.save()
    
    @require_mime('json')
    def update(self, request, msisdn):
        try:
            customer = Customer.objects.get(msisdn=msisdn)
        except Customer.DoesNotExist:
            return rc.NOT_FOUND
        
        form = CustomerForm(data=request.data, instance=customer)
        if not form.is_valid():
            raise FormValidationError(form)
            
        return form.save()
        

class ServiceHandler(BaseHandler):
    """
    Provides a REST API for managing Services.
    """
    allowed_methods = ('GET', 'POST',)
    model = Service
    fields = ('code', 'name', 'rate',)


customer_handler = Resource(CustomerHandler)
service_handler = Resource(ServiceHandler)
