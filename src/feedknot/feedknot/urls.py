# -*- coding: utf-8 -*-
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

    #url(r'^$', 'sample.views.index', name='index'),
    #url(r'^detail/(?P<sample_id>\d+)/$', 'sample.views.detail', name='detail'),
    #url(r'^create/$', 'sample.views.create', name='create'),
    #url(r'^edit/(?P<sample_id>\d+)/$', 'sample.views.edit', name='edit'),
    #url(r'^delete/(?P<sample_id>\d+)/$', 'sample.views.delete', name='delete'),

    url(r'^$', 'administration.views.index', name='index'),
    #url(r'^oAuth/$', 'administration.views.oAuth', name='oAuth'),
    #url(r'^login/$', 'administration.views.login', name='login'),
    #url(r'^logout/$', 'administration.views.logout', name='logout'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^main/$', 'feed.views.main', name='main'),

    url(r'^commonEdit/$', 'box.views.commonEdit', name='commonEdit'),
    url(r'^searchFeed/$', 'box.views.searchFeed', name='searchFeed'),

    url(r'^add_feed/$', 'feed.views.add_feed', name='add_feed'),
    url(r'^del_feed/$', 'feed.views.del_feed', name='del_feed'),

    url(r'^add_box/$', 'box.views.add_box', name='add_box'),
    url(r'^del_box/$', 'box.views.del_box', name='del_box'),

    url(r'^upd_article/$', 'feed.views.upd_article', name='upd_article'),
    url(r'^change_box/$', 'feed.views.change_box', name='change_box'),

    url(r'^error/$', 'common.views.err', name='common_error'),

    url(r'^log/$', 'common.views.write_logging', name='common_write_logging'),

)

handler500 = 'common.views.err_500'

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
