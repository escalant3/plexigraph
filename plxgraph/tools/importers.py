#!/usr/bin/env python
#*-* coding: utf-8

# plxgraph.tools.importers
# Diego Muñoz Escalante (escalant3 at gmail dot com)

import csv

import networkx as nx


def dictionary_to_nx(topic_file, relation_file, styles_dict = None):
    try:
        from django.utils.encoding import smart_str
    except ImportError:
        smart_str = unicode
    f = open(topic_file, 'r')
    lines = f.readlines()
    lines = [smart_str(line) for line in lines]
    f.close()
    topics = csv.reader(lines, delimiter=' ', quotechar='"')
    topics = [(topic[1:-1]) for topic in list(topics)]
    f = open(relation_file, 'r')
    data = f.read()
    f.close()
    relationships = eval(data)
    if styles_dict:
        TOPIC_STRUCTURE = styles_dict['topic_structure']
        RELATION_NODE_INFO = styles_dict['relation_node_info']
    else:
        from styles import TOPIC_STRUCTURE, RELATION_NODE_INFO
    graph = create_nodes(topics, TOPIC_STRUCTURE)
    graph = create_edges(graph, relationships, RELATION_NODE_INFO)
    return graph


def create_nodes(topics, TOPIC_STRUCTURE):
    graph = nx.Graph()
    for topic in topics:
        node_id = None
        node_info = {}
        for field in TOPIC_STRUCTURE.keys():
            if TOPIC_STRUCTURE[field][0] == "ID":
                assert TOPIC_STRUCTURE[field][1] == 'int'
                node_id = int(topic[int(field)])
            elif TOPIC_STRUCTURE[field][1] == 'int':
                node_info[TOPIC_STRUCTURE[field][0]] = int(topic[int(field)])
            elif TOPIC_STRUCTURE[field][1] == 'string':
                node_info[TOPIC_STRUCTURE[field][0]] = topic[int(field)]
        if not node_id:
            raise Error("An ID field must be specified")
        new_node = graph.add_node(node_id)
        graph.node[node_id] = node_info
    return graph


def create_edges(graph, items, RELATION_NODE_INFO):
    # TODO: Fix this
    hyper_counter = 10000
    for item_key in items.keys():
        graph.add_node(item_key)
        graph.node[item_key] = RELATION_NODE_INFO.copy()
        for related_key, value in items[item_key]['related'].iteritems():
            graph.add_edges_from([(item_key, related_key, value)])
        for hyper_edge in items[item_key]['hyperedges']:
            if hyper_edge['related']:
                graph.add_node(hyper_counter)
                graph.node[hyper_counter] = hyper_edge
                graph.node[hyper_counter]['type'] = 10000
                graph.add_edges_from([(item_key, hyper_counter, {})])
                for hyper_related in hyper_edge['related']:
                    graph.add_edges_from([(hyper_related, hyper_counter, {})])
                hyper_counter += 1
    return graph
