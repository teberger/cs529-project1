__author__ = 'Taylor'

class DecisionTree:
    def __init__(self, f, children):
        """
        :param f:
        :param children:
        :return:
        """
        self.f = f
        self.children = children


    def classify(self, instance):
        """
        :param instance:
        :return:
        """
        pass

class DecisionLeaf(DecisionTree):
    def __init__(self, clazz):
        super(DecisionLeaf, self).__init__(self, None, [])
        """

        :param clazz:
        :return:
        """
        self.clazz = clazz

    def classify(self, instance):
        return self.clazz

class DnaRegion:
    def __init__(self, nucleotides):
        """

        :param nucleotides:
        :return:
        """
        self.nucleotides = nucleotides