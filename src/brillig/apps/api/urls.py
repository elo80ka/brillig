from django.conf.urls.defaults import patterns, url
from piston.doc import documentation_view
from api.handlers import customer_handler, service_handler

urlpatterns = patterns('',
    url(r'^customers/(?P<msisdn>\d+)$', customer_handler, name='api_customer'),
    url(r'^customers$', customer_handler, name='api_customers'),
    url(r'^services/(?P<code>\w+)$', service_handler, name='api_services'),
    url(r'^services$', service_handler, name='api_services'),
)