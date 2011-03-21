from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^$', 'find', name='customers_find_customer'),
    url(r'^(?P<msisdn>\d+)/edit/$', 'manage_customer', name='customers_edit_customer'),
    url(r'^new/$', 'manage_customer', name='customers_add_customer'),
    url(r'^services/$', 'services', name='customers_list_services'),
    url(r'^services/(?P<id>\w+)/edit/$', 'manage_service', name='customers_edit_service'),
    url(r'^services/new/$', 'manage_service', name='customers_add_service'),
    url(r'^usage/$', 'usage', name='customers_upload_usage'),
)