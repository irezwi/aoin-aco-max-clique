from abc import ABCMeta, abstractmethod
import random

from graph import Clique


class Algorithm(metaclass=ABCMeta):
    def __init__(self, graph, output):
        self.graph = graph
        self.output = output

    @abstractmethod
    def run(self):
        raise NotImplementedError


class AntColonyOptimizerAlgorithm(Algorithm):
    def __init__(self, graph, iterations, ants, output):
        super().__init__(graph, output)
        self.iterations = iterations
        self.ants = ants

    def run(self):
        pass


class ReferenceAlgorithm(Algorithm):
    def __init__(self, graph, output, agents):
        super().__init__(graph, output)
        self.agents = [self.Agent(graph) for _ in range(agents)]

    class Agent:
        def __init__(self, graph):
            self.clique = Clique(graph)
            # Initialize clique with randomly chosen node
            self.clique.add_node(random.choice(list(graph.nodes)))
            self.graph = graph
            self.finished = False

        def __repr__(self):
            return f'Agent(clique_size={len(self.clique.nodes)}, finished={self.finished})'

    def run(self):
        for agent in self.agents:
            while not agent.finished:
                if candidates := agent.clique.get_candidates():
                    # Select next node by random choice weighted by edges count
                    next_node = random.choices(
                        candidates, weights=[len(self.graph.get_node_edges(node)) for node in candidates], k=1)[0]
                    agent.clique.add_node(next_node)
                else:
                    agent.finished = True

            print(f'best so far: {max(len(agent.clique.nodes) for agent in self.agents)}, '
                  f'last result: {len(agent.clique.nodes)}, '
                  f'agents still alive: {len([agent for agent in self.agents if not agent.finished])}')
