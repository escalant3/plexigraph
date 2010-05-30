from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^selector/$', 'plexigraph.neo4j.views.selector'),
    (r'^interactor_query', 'plexigraph.neo4j.views.interactor_query'),
    (r'^new_query', 'plexigraph.neo4j.views.new_query'),
    (r'^$', 'plexigraph.neo4j.views.index'),
)
