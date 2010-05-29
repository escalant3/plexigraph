from django.shortcuts import render_to_response, HttpResponseRedirect
from django.utils import simplejson

from neo4jclient import GraphDatabase
from networkx import Graph

from forms import Neo4jConnectionForm, Neo4jQueryForm
from graphview.views import set_graph_data
from plxgraph.nx.interaction import NetworkxInteractor

def index(request):
    if request.method == 'POST':
        form = Neo4jConnectionForm(request.POST)
        if form.is_valid():
            host = form.cleaned_data['host']
            gdb = GraphDatabase(host)
            request.session['gdb'] = gdb
            return HttpResponseRedirect('/viewer/neo4j/selector/')
    else:
        form = Neo4jConnectionForm()
    return render_to_response('neo4j/index.html', {
        'form': form,
    })

def selector(request):
    if request.method == 'POST':
        form = Neo4jQueryForm(request.POST)
        if form.is_valid():
            gdb = request.session.get('gdb', None)
            if gdb:
                node = gdb.node[form.cleaned_data['node']]
                depth = form.cleaned_data['depth']
                new_nodes = []
                graph = Graph()
                graph.add_node(node.id, **node.properties)
                new_nodes.append(node.id)
                for i in range(depth):
                    added_nodes = []
                    for node_id in new_nodes:
                        node = gdb.node[node_id]
                        for relation in node.relationships.all():
                            start = relation.start
                            end = relation.end
                            if start not in new_nodes:
                                graph.add_node(start.id, **start.properties)
                                added_nodes.append(start.id)
                            if end not in new_nodes:
                                graph.add_node(end.id, **end.properties)
                                added_nodes.append(end.id)
                            graph.add_edge(start.id, end.id, **relation.properties)
                    new_nodes += added_nodes
                #for i in range(depth):
                interactor = NetworkxInteractor(graph)
                request.session['interactor'] = interactor
                request.session['layout'] = None

                new_graph = set_graph_data(request, interactor, {})[0]
                metadata_list = [(key, value) for key, value 
                        in interactor.get_metadata().iteritems()]
                node_style_list = [(key,value) for key,value 
                        in interactor.styles.iteritems()]
                json_graph = simplejson.dumps(new_graph)
                form = Neo4jQueryForm()
            else:
                form = Neo4jConnectionForm()
                return render_to_response('neo4j/index.html', {
                                            'form': form})
            return render_to_response('neo4j/explorer.html',{
                                        'form': form,
                                        'json_graph':json_graph,
                                        'metadata_list': metadata_list,
                                        'showing_query': True,
                                        'node_style_list': node_style_list})
    else:
        form = Neo4jQueryForm()
    return render_to_response('neo4j/explorer.html', {
        'form': form,
    })

def interactor_query(request):
    if request.method == 'POST':
        query = request.POST.get('query', None)
        if query:
            eval(query)
    return render_to_response('graphview/explorer.html', {})
