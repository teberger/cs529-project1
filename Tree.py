__author__ = 'Taylor'

class DecisionTree:
    def __init__(self, id, f, children):
        """
        :param f:
        :param children:
        :return:
        """
        self.id = id
        self.f = f
        self.children = children


    def classify(self, instance):
        """
        :param instance:
        :return:
        """
        return self.f(instance).classify(instance)

class DecisionLeaf(DecisionTree):
    def __init__(self, clazz):
        """

        :param clazz:
        :return:
        """
        self.clazz = clazz

    def classify(self, instance):
        return self.clazz
