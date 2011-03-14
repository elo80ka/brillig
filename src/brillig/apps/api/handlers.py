from piston.handler import BaseHandler
from piston.utils import require_mime, validate
from api.resource import Resource
from accounts.models import Customer, Service
from accounts.forms import CustomerForm, ServiceForm

class CustomerHandler(BaseHandler):
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

customer_handler = Resource(CustomerHandler)
