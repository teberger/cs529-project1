__author__ = 'Taylor'

class DnaRegion:
    """
    """
    def __init__(self, sequence):
        self.sequence = sequence

    def get_region(self, start, stop=-1):
        """
        Gets a region of the DNA sequence identified by the start and stop parameters

        :param start: the start index
        :param stop: the stop index (exclusive and optional)
        :return: if the stop index is not specified it will return a single element at the index
                 of the start parameter, otherwise it will return a slice of elements from start to the stop index -1.
        """
        if stop == -1:
            return self.sequence[start]
        else:
            return self.sequence[start:stop]

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return str(self)


class Instance:
    """
    """
    def __init__(self, attributes, clazz):
        """
        """
        self.attributes = attributes
        self.clazz = clazz

    def __str__(self):
        return '(' + str(self.attributes) + ', ' + str(self.clazz) + ')'

    def __repr__(self):
        return str(self)

def accessor_f(index):
    """
    """
    return lambda x: x.attributes[index]



def read_instance(string):
    """
    """
    [s1, c] = string.split(' ')

    if c == '+':
        c = True
    else:
        c = False

    return Instance(s1, c)
