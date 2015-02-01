__author__ = 'Taylor'

class DnaRegion:
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

