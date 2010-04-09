import os

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

site_media = os.path.join(os.path.dirname(__file__), 'site_media')
urlpatterns = patterns('',
    # Example:
    # (r'^djangovertex/', include('djangovertex.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^viewer/$', 'djangovertex.graphview.views.index'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/$', 'djangovertex.graphview.views.explore'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/relayout/$', 'djangovertex.graphview.views.relayout'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/reset/$', 'djangovertex.graphview.views.reset'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/delete_node/(?P<node_id>\d+)$', 
            'djangovertex.graphview.views.delete_node'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/expand_node/(?P<node_id>\d+)$', 
            'djangovertex.graphview.views.expand_node'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/toggle_nodes/(?P<node_type>\d+)$',
            'djangovertex.graphview.views.toggle_nodes'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/load_state/$', 'djangovertex.graphview.views.load_state'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/save_state/$', 'djangovertex.graphview.views.save_state'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/delete_isolated/$', 'djangovertex.graphview.views.delete_isolated'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/interactor_query/(?P<query>[^$]+)$', 
         'djangovertex.graphview.views.interactor_query'),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': site_media}),
        
)
