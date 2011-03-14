from django.conf.urls.defaults import patterns, url
from api.handlers import customer_handler

urlpatterns = patterns('',
    url(r'^customers/(?P<msisdn>\d+)$', customer_handler, name='api_customer_details'),
    url(r'^customers$', customer_handler, name='api_customers'),
)