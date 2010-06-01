#!/usr/bin/env python
# *-* coding: utf-8 *-*

# plxgraph.nx.interaction
# Diego Muñoz Escalante (escalant3 at gmail dot com)
from random import randint

import networkx as nx


class NetworkxInteractor():

    def __init__(self, nx_graph, style_dict=None):
        self.graph = nx_graph
        self.original_graph = nx_graph
        self.shown_graph = nx_graph
        self.nodes_by_type = {}
        self.styles = {}
        for node in self.graph.nodes():
            self.graph.node[node]['_visible'] = True
        for edge in self.graph.edges():
            if 'weight' not in self.graph.edge[edge[0]][edge[1]]:
                self.graph.edge[edge[0]][edge[1]]['weight'] = 1.0
        if not style_dict:
            for node_id in self.graph.nodes():
                node_type = self.graph.node[node_id].get('type', None)
                if node_type not in self.styles:
                    color = ('#%x' % randint(0, 16777216)).replace(' ', '0')
                    self.styles[node_type] = {"color": color,
                                                "size": "1.0",
                                                "label": node_type}
        if style_dict:
            self.styles = style_dict['node_styles']
        try:
            for i in (self.styles):
                self.nodes_by_type[i] = [key for key in self.graph.nodes()
                                        if self.graph.node[key]['type'] == i]
        except KeyError:
            self.nodes_by_type[0] = self.graph.node.keys()
        for key in self.styles.keys():
            self.styles[key]['show'] = True
        self.original_graph = nx_graph
        self.shown_graph = nx_graph

    def reset_graph(self):
        ''' Resets the graph to the starting point '''
        self.graph = self.original_graph.subgraph(self.original_graph.nodes())

    def save_graph(self):
        ''' Saves a snapshop of the graph state '''
        self.original_graph = self.graph.subgraph(self.graph.nodes())

    def hide_nodes(self, nodes):
        ''' Removes a list of nodes '''
        node_list = self.graph.nodes()
        for node in nodes:
            node_list.remove(node)
        self.graph = self.graph.subgraph(node_list)

    def remove_nodes(self, nodes):
        ''' Removes a list of nodes and all it edges '''
        for node in nodes:
            neighbors = self.graph.neighbors(node)
            for n in neighbors:
                self.graph.remove_edge(node, n)
            self.graph.remove_node(node)

    def remove_edges(self, edges):
        ''' Removes a list of edges'''
        for edge in edges:
            self.graph.remove_edge(edge[0], edge[1])

    def remove_isolated_nodes(self):
        ''' Removes nodes without connection '''
        for node in self.graph.nodes():
            if self.graph.degree(node) == 0:
                self.graph.remove_node(node)

    def get_nodes_neighborhood(self, nodes, depth=1):
        ''' Returns the neighborhood of a list of nodes with a given depth '''
        nodes_to_show = set()
        for node in nodes:
            nodes_to_show.add(node)
            for i in range(depth):
                expanded_nodes = []
                for nth in nodes_to_show:
                    neighbors = self.original_graph.neighbors(nth)
                    expanded_nodes += neighbors
                for en in expanded_nodes:
                    nodes_to_show.add(en)
        return nodes_to_show

    def show_nodes_neighborhood(self, nodes, depth=1):
        ''' Shows the neighborhood of a list of nodes with a given depth '''
        self.reset_graph()
        nodes_to_show = self.get_nodes_neighborhood(nodes, depth)
        self.graph = self.graph.subgraph(nodes_to_show)

    def show_nodes_by_field(self, field, value, depth=1):
        ''' Shows nodes with the field matching the given value '''
        nodes_to_show = self.nodes_by_field(self.original_graph, field, value)
        self.show_nodes_neighborhood(nodes_to_show, depth)

    def filter_nodes_by_field(self, field, value, depth=1):
        ''' Filters nodes with the field matching the given value '''
        nodes_to_show = self.nodes_by_field(self.graph, field, value)
        self.show_nodes_neighborhood(nodes_to_show, depth)
        self.graph = self.graph.subgraph(nodes_to_show)

    def nodes_by_field(self, graph, field, value):
        ''' Shows nodes with the field label matching the given value '''
        return [node for node in graph.node
                        if graph.node[node].get(field) == value]

    def subgraph_by_field(self, field, value):
        ''' Returns a subgraph of nodes matching the given field
        with the given value '''
        nodes = self.nodes_by_field(field, value)
        return self.graph.subgraph(nodes)

    def hide_labels(self, node_type=[]):
        ''' Hide all node labels. If node_type is specified it only
        hides nodes with that text-type'''
        self.graph = self.graph.subgraph(self.graph.nodes())
        if not node_type:
            for key in self.graph.node:
                self.graph.node[key]['text'] = ''
        else:
            for key in self.graph.node:
                if self.graph.node[key]['text-type'] in node_type:
                    self.graph.node[key]['text'] = ''

    def expand_node(self, node):
        ''' Expand a given node of the graph '''
        nbunch = self.get_nodes_neighborhood(node)
        subgraph = self.original_graph.subgraph(nbunch)
        self.graph = nx.compose(self.graph, subgraph)
        for node in self.graph.nodes():
            self.graph.node[node] = self.original_graph.node[node].copy()

    def get_metadata(self):
        ''' Returns information about the graph '''
        metadata = {}
        metadata['nodes'] = self.original_graph.number_of_nodes()
        metadata['nodes_shown'] = self.shown_graph.number_of_nodes()
        metadata['edges'] = self.original_graph.number_of_edges()
        metadata['edges_shown'] = self.shown_graph.number_of_edges()
        return metadata

    def get_shown_graph(self):
        ''' Creates and returns a copy of the graph with only the nodes
            specified as visible in the style dictionary '''
        self.shown_graph = self.graph.subgraph(self.graph.nodes())
        for node in self.shown_graph.nodes():
            node_type = str(self.shown_graph.node[node].get('type'))
            if node_type and self.styles.get(node_type) \
                and not self.styles[node_type]['show']:
                self.shown_graph.remove_node(node)
        return self.shown_graph

    def node_data(self, node):
        ''' Returns node data related with the network structure '''
        if not self.graph.is_multigraph():
            clustering = nx.clustering(self.graph, node)
            original_clustering = nx.clustering(self.original_graph, node)
        else:
            clustering = None
            original_clustering = None
        return {'degree': self.graph.degree(node),
                'clustering': clustering,
                'original-degree': self.original_graph.degree(node),
                'original-clustering': original_clustering}
