__author__ = 'Taylor'

from sys import argv
from DnaRegion import *
from Utilities import information_gain, argmax, purity, separate_by_attribute
from functools import partial
from Tree import *

import graphviz
import pygraphviz

m_bases = set(['a', 'c', 'g', 't'])
m_classes = set([True, False])
g_id = 0

def is_pure(data):
    _, count = majority(data)
    return (len(data) == count)

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

def build_tree(graph, split_proc, end_proc, data, parent_id):
    if (end_proc(data)):
        lable, _ = majority(data)
        child = DecisionLeaf(lable)
        child.id = parent_id + '->' + str(lable)

        graph.node(child.id, str(lable))
        return child

    split_index = split_proc(data)
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


def classify(graph, root, instance):
    pass
    

if __name__ == '__main__':
    print "Starting decision tree learning..."
    print "Training data: ", argv[3]
    print "Testing data : ", argv[4]
    
    if argv[1] == '-p':
        procedure = get_max_gain_index
    elif argv[1] == '-i':
        procedure = get_max_gain_index
    else:
        raise Exception("Invalid first argument, the argument can be: -p, -i")

    alpha = float(argv[2])

    lines_train = open(argv[3]).read().splitlines()
    lines_valid = open(argv[4]).read().splitlines()

    training_data = map(lambda x: read_instance(x), lines_train)
    validation_data = map(lambda x: read_instance(x), lines_valid)

    graph = graphviz.Digraph(format='png')
    
    root = build_tree(graph, procedure, is_pure, training_data, "")
    graph.render('output/graph')
    
    score = 0.0
    total = len(validation_data)
    for v in validation_data:
        if v.clazz == root.classify(v):
            score += 1

    print (score / total)
            
        


