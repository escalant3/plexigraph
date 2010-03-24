from django.shortcuts import render_to_response, redirect
from django.utils import simplejson

import networkx as nx
import pickle
from plexigraph.nx.interaction import NetworkxInteractor
from plexigraph.tools import importers

from djangovertex.graphview.models import Dataset

def index(request):
    datasets = Dataset.objects.all()
    return render_to_response('graphview/index.html', {'datasets':datasets})


def explore(request, dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)
    styles = dataset.node_styles()
    interactor = request.session.get('interactor')
    if (not interactor):
        graph = importers.dictionary_to_nx(dataset.topics.path,
                                        dataset.relations.path)
        interactor = NetworkxInteractor(graph)
        request.session['interactor'] = interactor
    graph = interactor.graph
    layout = request.session.get('layout')
    if (not layout):
        if not dataset.layout:
            layout = nx.drawing.spring_layout(graph, scale=600)
            request.session['layout'] = layout
            dataset.layout = pickle.dumps(layout)
            dataset.save()
        else:
            layout = dataset.layout
            request.session['layout'] = layout
    nodes = {}
    edges = {}
    for node in graph.nodes():
        nodes[node] = graph.node[node].copy()
        nodes[node]['ID'] = node
        nodes[node]['xpos'] = layout[node][0]
        nodes[node]['ypos'] = layout[node][1]
        nodes[node]['color'] = styles[str(graph.node[node]['type'])]['color']
        nodes[node]['size'] = styles[str(graph.node[node]['type'])]['size']
        nodes[node].update(interactor.node_data(node))
    for i in range(len(graph.edges())):
        edge = graph.edges()[i]
        edges[i] = {'ID': i,
                    'node1': edge[0],
                    'node2': edge[1]}
    new_graph = {'nodes': nodes, 'edges':edges}
    node_style_list = [(key,value) for key,value in styles.iteritems()]
    json_graph = simplejson.dumps(new_graph)
    return render_to_response('graphview/explorer.html', 
                                {'json_graph':json_graph,
                                'dataset': dataset,
                                'node_style_list': node_style_list})


def delete_node(request, dataset_id, node_id):
    interactor = request.session.get('interactor')
    if interactor:
        interactor.remove_nodes([int(node_id)])
        request.session['interactor'] = interactor
    return redirect('djangovertex.graphview.views.explore', dataset_id=dataset_id)


def relayout(request, dataset_id):
    interactor = request.session.get('interactor')
    if interactor:
        layout = nx.drawing.spring_layout(interactor.graph, scale=600)
        request.session['layout'] = layout
    return redirect('djangovertex.graphview.views.explore', dataset_id=dataset_id)


def reset(request, dataset_id):
    interactor = request.session.get('interactor')
    if interactor:
        request.session.pop('interactor')
        request.session.pop('layout')
    return redirect('djangovertex.graphview.views.explore', dataset_id=dataset_id)


def save_state(request, dataset_id):
    interactor = request.session.get('interactor')
    if interactor:
        interactor.save_graph()
        request.session['interactor'] = interactor
    return redirect('djangovertex.graphview.views.explore', dataset_id=dataset_id)


def load_state(request, dataset_id):
    interactor = request.session.get('interactor')
    if interactor:
        interactor.reset_graph()
        request.session['interactor'] = interactor
        layout = nx.drawing.spring_layout(interactor.graph, scale=600)
        request.session['layout'] = layout
    return redirect('djangovertex.graphview.views.explore', dataset_id=dataset_id)


def interactor_query(request, dataset_id, query):
    interactor = request.session.get('interactor')
    if interactor:
        """
        for method in dir(interactor):
            if method == query_data[0]:
                break
        else:
            pass
        parameters = query_data[1:]
        getattr(interactor, method)(parameters)
        """
        try:
            eval(query)
            request.session['interactor'] = interactor
        except:
            print "Fix me"
    return redirect('djangovertex.graphview.views.explore', dataset_id=dataset_id)
