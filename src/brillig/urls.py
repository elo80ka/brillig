from django.conf.urls.defaults import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', name='site_login'),
    url(r'^logout/$', 'logout', name='site_logout'),
    url(r'^reset-password/$', 'password_reset', name='site_password_reset'),
    url(r'^reset-password/done/$', 'password_reset_done', name='site_password_reset_done'),
    url(r'^reset-password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm', name="site_password_reset_confirm"),
    url(r'change-password/$', 'password_change', name='site_change_password'),
    url(r'change-password/done/$', 'password_change_done', name='site_change_password_done'),
    url(r'change-password/complete/$', 'password_reset_complete', name='site_change_password_complete'),
)

urlpatterns += patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}, name='site_index'),
    url(r'^customers/', include('accounts.urls')),
    
    # Examples:
    # url(r'^$', 'brillig.views.home', name='home'),
    # url(r'^brillig/', include('brillig.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
