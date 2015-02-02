__author__ = 'Taylor'

from sys import argv
from DnaRegion import *

if __name__ == '__main__':
    print "Starting decision tree learning..."
    print "Training data: ", argv[1]
    print "Testing data : ", argv[2]

    lines_train = open(argv[1]).read().splitlines()
    lines_valid = open(argv[2]).read().splitlines()

    training_data = map(lambda x: build_from_string(x), lines_train)
    validation_data = map(lambda x: build_from_string(x), lines_valid)    
    
    
