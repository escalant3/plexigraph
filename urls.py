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
    (r'^viewer/explore/relayout/$', 'plexigraph.graphview.views.relayout'),
    (r'^viewer/explore/reset/$', 'plexigraph.graphview.views.reset'),
    (r'^viewer/explore/delete_nodes/(?P<node_list>[-\w,]+)$', 
            'plexigraph.graphview.views.delete_nodes'),
    (r'^viewer/explore/delete_edges/(?P<edge_list>[-\w,]+)$', 
            'plexigraph.graphview.views.delete_edges'),
    (r'^viewer/explore/expand_nodes/(?P<node_list>[-\w,]+)$', 
            'plexigraph.graphview.views.expand_nodes'),
    (r'^viewer/explore/toggle_nodes/(?P<node_type>\w+)$',
            'plexigraph.graphview.views.toggle_nodes'),
    (r'^viewer/explore/load_state/$', 'plexigraph.graphview.views.load_state'),
    (r'^viewer/explore/save_state/$', 'plexigraph.graphview.views.save_state'),
    (r'^viewer/explore/delete_isolated/$', 'plexigraph.graphview.views.delete_isolated'),
    (r'^viewer/explore/interactor_query/$', 
         'plexigraph.graphview.views.interactor_query'),
    (r'^viewer/neo4j/', include('neo4j.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': site_media}),
)
