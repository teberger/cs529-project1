__author__ = 'Taylor'

from numpy import log2

def entropy(instance_list, classes):
    """
    Calculates the entropy of the instance_list using the specified classes

    :param instance_list: the instance (pairs of the form (x,y) where x
                          is the data and y is the class of the data)
    :param classes: the classes to use to calculate the entropy. This 
                    assumes all classes (y) are in this iterable. If not,
                    they are not counted properly and the calculation of
                    entropy is incorrect
    :return: the calculated entropy of the instance_list
    """
    
    separated  = filter(lambda x : x != 0, [len([(x,y) for (x,y) in instance_list if y == c]) for c in classes])

    n = float(len(instance_list))

    #Entropy is a fold over the list, starting at 0
    entropy = reduce(lambda x, y: x - (y/n * log2(y/n)), separated, 0)

    return entropy

def information_gain(instance_list, accessor_function, attribute_classes, classes):
    """
    Calculates the information gain for the data using the attribute accessor
    function as the splitting function which maps the instances which result
    in a specific value to another list with all the same values in it. 

    :param instance_list: 
         the iterable of all instance in the current data set
    :param accessor_function: 
         the function used to access and return an attribute from an instance
    :param attribute_classes: 
         an iterable which contains all discrete values of the attributes that
         could be the result of the accessor_function call
    :param classes:
         an iterable that contains all classes any of the instances my be
         classified as
    :return: 
         the calculated information gain for the attribute identified by the
         accessor function
    """
    entropy_current = entropy(instance_list, classes)

    separated = separate_by_attribute(instance_list, accessor_function, attribute_classes)
    
    n = float(len(instance_list))
    info_gain = entropy_current + reduce(lambda x, y: \
                                           x - (len(y)/n * entropy(y, classes)),
                                         separated, 0)
    
    return info_gain

def separate_by_attribute(instance_list, accessor_function, attribute_classes):
    return [[(x,y) for (x,y) in instance_list if accessor_function(x) == a] for a in attribute_classes]


def chi_squared():
    pass


def argmin(arg_iter, func):
    arg_val = None
    ret = None

    for arg in arg_iter:
        v_1 = func(arg)
        if (arg_val == None or v_1 < arg_val):
            arg_val = v_1
            ret = arg

    return ret

def argmax(arg_iter, func):
    arg_val = None
    ret = None
    for arg in arg_iter:
        v_1 = func(arg)
        if (arg_val == None or v_1 > arg_val):
            arg_val = v_1
            ret = arg

    return ret

if __name__ == '__main__':
    data = [(1,True), (2,False), (2,False), (2,False), (1,True), (2,True)]
    classes = [True, False]
    print "Entropy: ", entropy(data, classes)
    print "Info Gain: ", information_gain(data, lambda x : x, [1,2], classes)
