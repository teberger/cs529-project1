__author__ = 'Taylor'

from sys import argv
from DnaRegion import *
from Utilities import *
from functools import partial
from Tree import *

import graphviz
import pygraphviz

m_bases = set(['a', 'c', 'g', 't'])
m_classes = set([True, False])
g_id = 0
ALPHA = 0

def is_pure(data):
    _, count = majority(data)
    return (len(data) == count)

def on_chi_squared(data, index):
    split_data = separate_by_attribute(data, index, m_bases)
    score = chi_squared(split_data, m_classes)

    if ALPHA == 0.95:
        return score <= 7.82
    elif ALPHA == 0.99:
        return score <= 11.34
    else:
        return is_pure(data)

def majority(data):
    pos_count = len(filter(lambda x: x.clazz, data))
    neg_count = len(data) - pos_count

    if pos_count >= neg_count:
        return True, pos_count
    else:
        return False, neg_count

def get_max_gain_index(data):
    info_partial = partial(information_gain,
                           instance_list = data,
                           attribute_classes = m_bases,
                           classes = m_classes)
                        
    return argmax(range(len(data[0].attributes)), info_partial)

def get_misclass_index(data):
    mis_partial = partial(misclassification_rate,
                          instance_list = data,
                          attribute_classes = m_bases,
                          classes = m_classes)

    return argmin(range(len(data[0].attributes)), mis_partial)
    

def build_tree(graph, split_proc, end_proc, data, parent_id):
    split_index = split_proc(data)

    if (end_proc(data, split_index)):
        lable, _ = majority(data)
        child = DecisionLeaf(lable)
        child.id = parent_id + '->' + str(lable)

        graph.node(child.id, str(lable))
        return child

    this_id = parent_id + '->' + str(split_index)
    graph.node(this_id, str(split_index))
    separated_data = separate_by_attribute(data, split_index, m_bases)

    children = {}
    for d in separated_data.keys():
        #If data set is empty, use parent majority, not the empty majority
        if len(separated_data[d]) == 0:
            lable, _ = majority(data)
            child = DecisionLeaf(lable)
            child_id = this_id + '->' + str(lable)
            graph.node(child_id, str(lable))

        else:
            #construct the DecisionTree child for this branch of the tree
            child = build_tree(graph, split_proc, end_proc, separated_data[d], this_id+'('+str(d)+')')
            child_id = child.id

        children[d] = child
        graph.edge(this_id, child_id, label=str(d))

    f = lambda x : children[x.attributes[split_index]]
    node = DecisionTree(this_id, f, children)
    return node

if __name__ == '__main__':
    print "Starting decision tree learning..."
    print "Training data: ", argv[3]
    print "Testing data : ", argv[4]

    if argv[1] == '-p':
        procedure = get_misclass_index
        str_proc = 'mis'
    elif argv[1] == '-i':
        procedure = get_max_gain_index
        str_proc = 'info'
    else:
        raise Exception("Invalid first argument, the argument can be: -p, -i")

    ALPHA = float(argv[2])

    lines_train = open(argv[3]).read().splitlines()
    lines_valid = open(argv[4]).read().splitlines()

    training_data = map(lambda x: read_instance(x), lines_train)
    validation_data = map(lambda x: read_instance(x), lines_valid)

    graph = graphviz.Digraph(format='png')
    
    root = build_tree(graph, procedure, on_chi_squared, training_data, "")
    graph.render('output/graph_' + str(ALPHA) + '_' + str_proc)
    
    score = 0.0
    total = len(validation_data)
    for v in validation_data:
        if v.clazz == root.classify(v):
            score += 1

    print (score / total)
