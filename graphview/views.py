from django.shortcuts import render_to_response, redirect, HttpResponse
from django.utils import simplejson

import networkx as nx
import pickle
from plxgraph.nx.interaction import NetworkxInteractor
from plxgraph.tools import importers

import settings
from plexigraph.graphview.models import Dataset

SCALE = settings.EXPLORER_CANVAS_SIZE


def main(request):
    return render_to_response('graphview/main.html')


def index(request):
    datasets = Dataset.objects.all()
    request.session.pop('interactor', None)
    return render_to_response('graphview/index.html', {'datasets':datasets})


def explore(request, dataset_id):
    request.session['viewer'] = request.path_info
    dataset = Dataset.objects.get(pk=dataset_id)
    interactor = request.session.get('interactor')
    interactive_mode = False
    if (not interactor):
        styles = dataset.node_styles()
        try:
            if dataset.data_type == 'plxgh':
                graph = importers.dictionary_to_nx(dataset.topics.path,
                                            dataset.relations.path,
                                            dataset.get_configuration())
            else:
                graph = getattr(nx, 'read_%s' % dataset.data_type)(dataset.graph_file)
        except ValueError:
            return redirect('plexigraph.graphview.views.index')
        interactor = NetworkxInteractor(graph, dataset.get_configuration())
        request.session['interactor'] = interactor
        new_graph = {'nodes': {}, 'edges':{}}
    else:
        new_graph, interactive_mode = set_graph_data(interactor)
    metadata_list = [(key, value) for key, value 
                        in interactor.get_metadata().iteritems()]
    node_style_list = [(key,value) for key,value 
                        in interactor.styles.iteritems()]
    json_graph = simplejson.dumps(new_graph)
    if interactive_mode:
        template = 'graphview/interactive_explorer.html'
    else:
        template = 'graphview/explorer.html'
    return render_to_response(template, 
                                {'json_graph':json_graph,
                                'dataset': dataset,
                                'metadata_list': metadata_list,
                                'node_style_list': node_style_list})


def set_graph_data(interactor):
    graph = interactor.get_shown_graph()
    if graph.number_of_nodes() < settings.MAX_INTERACTIVE_NODES:
        interactive_mode = True
    else:
        interactive_mode = False
    nodes = {}
    edges = {}
    for node in graph.nodes():
        nodes[node] = graph.node[node].copy()
        nodes[node]['ID'] = node
        nodes[node].update(interactor.node_data(node))
        try:
            nodes[node]['color'] = interactor.styles[str(graph.node[node]['type'])]['color']
        except KeyError:
            nodes[node]['color'] = "#ffffff"
    for i, edge in enumerate(graph.edges()):
        edges[i] = {'ID': i,
                    'node1': edge[0],
                    'node2': edge[1]}
        edges[i].update(graph.edge[edge[0]][edge[1]])
    return ({'nodes': nodes, 'edges':edges}, interactive_mode)


def delete_nodes(request, node_list):
    node_list = node_list.split(',')
    interactor = request.session.get('interactor')
    if interactor:
        for node_id in node_list:
            interactor.remove_nodes([node_id])
        request.session['interactor'] = interactor
    #return redirect(request.session['viewer'])
    return HttpResponse(simplejson.dumps({'success':True, 'node_list':node_list}))


def delete_edges(request, edge_list):
    edge_list = zip(*[iter(edge_list.split(','))]*2)
    interactor = request.session.get('interactor')
    if interactor:
        for edge_tuple in edge_list:
            interactor.remove_edges([edge_tuple])
        request.session['interactor'] = interactor
        new_graph = set_graph_data(interactor)[0]
        response_dictionary = {'success': True,
                                'new_gdata': new_graph}
    return HttpResponse(simplejson.dumps(response_dictionary))


def toggle_nodes(request, node_type):
    styles = request.session['interactor'].styles
    styles[node_type]['show'] = not styles[node_type]['show']
    request.session['node_styles'] = styles
    return redirect(request.session['viewer'])


def reset(request):
    interactor = request.session.get('interactor')
    if interactor:
        request.session.pop('interactor')
    return redirect(request.session['viewer'])


def save_state(request):
    interactor = request.session.get('interactor')
    if interactor:
        interactor.save_graph()
        request.session['interactor'] = interactor
    return HttpResponse(simplejson.dumps({'success':True}))


def load_state(request):
    interactor = request.session.get('interactor')
    if interactor:
        interactor.reset_graph()
        request.session['interactor'] = interactor
        new_graph = set_graph_data(interactor)[0]
        response_dictionary = {'success': True,
                                'new_gdata': new_graph}
    return HttpResponse(simplejson.dumps(response_dictionary))


def delete_isolated(request):
    interactor = request.session.get('interactor')
    if interactor:
        deleted_nodes = interactor.remove_isolated_nodes()
        request.session['interactor'] = interactor
        response_dictionary = {'success': True,
                                'deleted_nodes': deleted_nodes}
    return HttpResponse(simplejson.dumps(response_dictionary))


def expand_nodes(request, node_list):
    node_list = node_list.split(',')
    interactor = request.session.get('interactor')
    if interactor:
        previous_nodes = interactor.graph.nodes()[:]
        for node_id in node_list:
            interactor.expand_node([node_id])
        request.session['interactor'] = interactor
        new_graph = set_graph_data(interactor)[0]
        response_dictionary = {'success': True,
                                'new_gdata': new_graph}
    return HttpResponse(simplejson.dumps(response_dictionary))


def interactor_query(request):
    if request.method == 'POST':
        interactor = request.session.get('interactor')
        query = request.POST.get('query', None)
        if query:
            eval(query)
            request.session['interactor'] = interactor
    return redirect(request.session['viewer'])
