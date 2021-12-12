from abc import ABCMeta, abstractmethod
import random


class Algorithm(metaclass=ABCMeta):
    def __init__(self, graph, output):
        self.graph = graph
        self.graph = output

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
    def __init__(self, graph, iterations):
        super().__init__(graph, output)
        self.iterations = iterations

    def run(self):

        agents = []
        should_stop = False

        while not should_stop:
            for ag in agents:
                candidates = ag.cliqe.get_candidates()
                if not candidates:
                    ag.finished = True
                else:
                    next_node = random.choice(candidates)
                    ag.clique.add_node(next_node)
                    print(f'Maksymalna klika:')
                    print(ag)
            self.iterations -= 1
            should_stop = all(map(lambda x: x.finished, agents)) or self.iterations == 0
