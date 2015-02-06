__author__ = 'Taylor'

from numpy import log2
from DnaRegion import accessor_f

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
    
    separated  = filter(lambda x : x != 0, [len([i for i in instance_list if i.clazz == c]) for c in classes])

    n = float(len(instance_list))

    #Entropy is a fold over the list, starting at 0
    entropy = reduce(lambda x, y: x - (y/n * log2(y/n)), separated, 0)

    return entropy

def misclassification(instance_list, classes):
    class_counts = counts(instance_list, classes)
    n = float(len(instance_list))
    return max(map(lambda x : x / n, class_counts.values()))

def misclassification_rate(index, instance_list, attribute_classes, classes):
    mis_current = misclassification(instance_list, classes)
    
    split_data = separate_by_attribute(instance_list, index, attribute_classes)
    
    errors = []
    for d_prime in split_data.values():
        if len(d_prime) == 0:
            continue

        d_len = float(len(d_prime))
        errors.append( d_len / len(instance_list) * misclassification(d_prime, classes))
    
    return mis_current - sum(errors)

def counts(instance_list, classes):
    count = {}
    for c in classes:
        count[c] = len(filter(lambda x : x.clazz == c, instance_list))
    return count
        

def information_gain(index, instance_list, attribute_classes, classes):
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

    separated = separate_by_attribute(instance_list, index, attribute_classes).values()

    n = float(len(instance_list))
    info_gain = entropy_current + reduce(lambda x, y: \
                                           x - (len(y)/n * entropy(y, classes)),
                                         separated, 0)
    
    return info_gain

def separate_by_attribute(instance_list, index, attribute_classes):
    return  {a:[x for x in instance_list if x.attributes[index] == a] for a in attribute_classes}

def chi_squared(separated_data, classes):
    table = {}
    total_columns = {}
    total_row = {}
    total = 0
    for key in separated_data.keys():
        table[key] = {}
        total_row[key] = 0

        for c in classes:
            table[key][c] = len([x for x in separated_data[key] if x.clazz == c])
            total_row[key] += table[key][c]
            total += table[key][c]

            if c in total_columns:
                total_columns[c] += table[key][c]
            else:
                total_columns[c] = table[key][c]

    expected = lambda attribute, c : total_row[attribute] / float(total) * total_columns[c]

    chi = 0
    for att in separated_data.keys():
        for c in classes:
            e = expected(att, c)
            if e == 0:
                return 0.0

            chi += ((table[att][c] - e) ** 2) / e

    return chi
    

def argmax(arg_iter, func):
    arg_val = None
    ret = None
    for arg in arg_iter:
        v_1 = func(arg)
        if (arg_val == None or v_1 > arg_val):
            arg_val = v_1
            ret = arg

    return ret

def argmin(arg_iter, func):
    arg_val = None
    ret = None
    for arg in arg_iter:
        v_1 = func(arg)
        if (arg_val == None or v_1 < arg_val):
            arg_val = v_1
            ret = arg

    return ret
