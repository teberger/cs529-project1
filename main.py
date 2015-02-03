__author__ = 'Taylor'

from sys import argv
from DnaRegion import *
from functools import partial

if __name__ == '__main__':
    print "Starting decision tree learning..."
    print "Training data: ", argv[1]
    print "Testing data : ", argv[2]

    lines_train = open(argv[1]).read().splitlines()
    lines_valid = open(argv[2]).read().splitlines()

    training_data = map(lambda x: read_instance(x), lines_train)
    validation_data = map(lambda x: read_instance(x), lines_valid)    
    
    # No current indices have been used
    used_accessors = set()

    m_bases = set('A', 'C', 'G', 'T')
    m_classes = set(True, False)
    
    max_info = partial(information_gain, instance_list = training_data,
                                         attribute_classes = m_bases,
                                         classes = m_classes)
                                        
