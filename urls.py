import os

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

site_media = os.path.join(os.path.dirname(__file__), 'site_media')
urlpatterns = patterns('',
    # Example:
    # (r'^plexigraph/', include('plexigraph.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^viewer/$', 'plexigraph.graphview.views.index'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/$', 'plexigraph.graphview.views.explore'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/relayout/$', 'plexigraph.graphview.views.relayout'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/reset/$', 'plexigraph.graphview.views.reset'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/delete_node/(?P<node_id>-?\d+)$', 
            'plexigraph.graphview.views.delete_node'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/expand_node/(?P<node_id>-?\d+)$', 
            'plexigraph.graphview.views.expand_node'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/toggle_nodes/(?P<node_type>\d+)$',
            'plexigraph.graphview.views.toggle_nodes'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/load_state/$', 'plexigraph.graphview.views.load_state'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/save_state/$', 'plexigraph.graphview.views.save_state'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/delete_isolated/$', 'plexigraph.graphview.views.delete_isolated'),
    (r'^viewer/(?P<dataset_id>\d+)/explore/interactor_query/(?P<query>[^$]+)$', 
         'plexigraph.graphview.views.interactor_query'),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': site_media}),
        
)
