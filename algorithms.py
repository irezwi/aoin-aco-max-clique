from abc import ABCMeta, abstractmethod


class Algorithm(metaclass=ABCMeta):
    def __init__(self, graph):
        self.graph = graph

    @abstractmethod
    def run(self):
        raise NotImplementedError


class AntColonyOptimizerAlgorithm(Algorithm):
    def __init__(self, graph, iterations, ants):
        super().__init__(graph)
        self.iterations = iterations
        self.ants = ants

    def run(self):
        pass


class ReferenceAlgorithm(Algorithm):

    def run(self):
        pass
