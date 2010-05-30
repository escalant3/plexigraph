from django.shortcuts import render_to_response, HttpResponseRedirect, redirect
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
    request.session['viewer'] = request.path_info
    if request.method == 'POST':
        form = Neo4jQueryForm(request.POST)
        if form.is_valid():
            gdb = request.session.get('gdb', None)
            if gdb:
                node = gdb.node[form.cleaned_data['node']]
                depth = form.cleaned_data['depth']
                new_nodes = []
                graph = Graph()
                node_id = str(node.id)
                graph.add_node(node_id, **node.properties)
                new_nodes.append(node_id)
                for i in range(depth):
                    added_nodes = []
                    for node_id in new_nodes:
                        node = gdb.node[node_id]
                        for relation in node.relationships.all():
                            start = relation.start
                            end = relation.end
                            if start not in new_nodes:
                                start_id = str(start.id)
                                graph.add_node(start_id, **start.properties)
                                added_nodes.append(start_id)
                            if end not in new_nodes:
                                end_id = str(end.id)
                                graph.add_node(end_id, **end.properties)
                                added_nodes.append(end_id)
                            graph.add_edge(start_id, end_id, **relation.properties)
                    new_nodes += added_nodes
                interactor = NetworkxInteractor(graph)
                request.session['interactor'] = interactor
                request.session['layout'] = None
                request.session['showing_query'] = True,
                response_dictionary = set_response_dictionary(request)
            else:
                form = Neo4jConnectionForm()
                return render_to_response('neo4j/index.html', {
                                            'form': form,
                                            })
            return render_to_response('neo4j/explorer.html',
                                        response_dictionary)
    else:
        interactor = request.session.get('interactor')
        return render_to_response('neo4j/explorer.html',
                                set_response_dictionary(request))


def set_response_dictionary(request):
    response_dictionary = {}
    response_dictionary['form'] = Neo4jQueryForm()
    interactor = request.session.get('interactor')
    if interactor:
        new_graph = set_graph_data(request, interactor)[0]
        response_dictionary['new_graph'] = new_graph
        response_dictionary['metadata_list'] = [(key, value) for key, value
                in interactor.get_metadata().iteritems()]
        response_dictionary['node_style_list'] = [(key, value) for key, value
                in interactor.styles.iteritems()]
        response_dictionary['json_graph'] = simplejson.dumps(new_graph)
        response_dictionary['showing_query'] = True
    return response_dictionary


def interactor_query(request):
    if request.method == 'POST':
        query = request.POST.get('query', None)
        if query:
            eval(query)
    return render_to_response('graphview/explorer.html', {})


def new_query(request):
    request.session.pop('showing_query')
    request.session.pop('interactor')
    return redirect(request.session['viewer'])
