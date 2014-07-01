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
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),

    url(r'^main/$', 'feed.views.main', name='main'),
    url(r'^main/(?P<box_id>\d+)/$', 'feed.views.main_select_box', name='main_select_box'),
    url(r'^feed/article/mark_read/$', 'feed.views.upd_article', name='article_mark_read'),

    url(r'^box/default_change/$', 'administration.views.edit_default_box', name='box_edit_default'),
    url(r'^common_edit/$', 'box.views.common_edit', name='common_edit'),
    url(r'^box/add/$', 'box.views.add_box', name='box_add'),
    url(r'^box/edit/name/$', 'box.views.edit_box_name', name='box_edit_name'),
    url(r'^box/edit/priority/$', 'box.views.edit_box_priority', name='box_edit_priority'),
    url(r'^box/delete/$', 'box.views.del_box', name='box_delete'),

    url(r'^box/(?P<box_id>\d+)/feed/list/$', 'feed.views.feed_list', name='feed_list'),
    url(r'^box/(?P<box_id>\d+)/feed/search/$', 'feed.views.search_feed', name='feed_search'),
    url(r'^box/(?P<box_id>\d+)/feed/add/$', 'feed.views.add_feed', name='feed_add'),
    url(r'^box/(?P<box_id>\d+)/feed/edit/$', 'feed.views.get_feeds', name='feed_edit'),
    url(r'^box/(?P<box_id>\d+)/feed/change_box/$', 'feed.views.change_box', name='feed_change_box'),
    url(r'^box/(?P<box_id>\d+)/feed/delete/$', 'feed.views.del_feed', name='feed_delete'),

    url(r'^error/$', 'common.views.err', name='common_error'),

    url(r'^log/$', 'common.views.write_logging', name='common_write_logging'),

)

handler500 = 'common.views.err_500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
