from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'feedknot.views.home', name='home'),
    # url(r'^feedknot/', include('feedknot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'sample.views.index', name='index'),
    url(r'^detail/(?P<sample_id>\d+)/$', 'sample.views.detail', name='detail'),
    url(r'^create/$', 'sample.views.create', name='create'),
    url(r'^edit/(?P<sample_id>\d+)/$', 'sample.views.edit', name='edit'),
    url(r'^delete/(?P<sample_id>\d+)/$', 'sample.views.delete', name='delete'),
    url(r'^main/$', 'feed.views.main', name='main'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )