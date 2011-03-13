from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from accounts.models import *
from accounts.forms import *

def find(request):
    return render_to_response('accounts/index.html',
        context_instance=RequestContext(request))
    
def manage_customer(request, msisdn=None):
    customer = get_object_or_404(Customer, msisdn=msisdn) if msisdn else None
    title = _('Update Customer') if customer else _('Add a Customer')
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, _(u'The customer was saved successfully.'))
            return redirect(find)
    else:
        form = CustomerForm(instance=customer)
    return render_to_response('accounts/form.html', {'form': form, 'instance': customer, 'title': title},
        context_instance=RequestContext(request))

def services(request):
    services = Service.objects.all()
    return render_to_response('accounts/services.html', {'services': services},
        context_instance=RequestContext(request))
    
def manage_service(request, id=None):
    service = get_object_or_404(Service, pk=id) if id else None
    title = _('Update Service') if service else _('Add a Service')
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            messages.success(request, _(u'The Service was saved successfully.'))
            return redirect(services)
    else:
        form = ServiceForm(instance=service)
    return render_to_response('accounts/form.html', {'form': form, 'instance': service, 'title': title},
        context_instance=RequestContext(request))
