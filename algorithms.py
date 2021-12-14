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
        should_stop = False

        while not should_stop:
            unfinished_agents = filter(lambda a: not a.finished, self.agents)
            for agent in unfinished_agents:
                candidates = agent.clique.get_candidates()
                if not candidates:
                    agent.finished = True
                else:
                    # Select next node by random choice weighted by edges count
                    next_node = random.choices(
                        candidates, weights=[len(self.graph.get_node_edges(node)) for node in candidates], k=1)[0]
                    agent.clique.add_node(next_node)

            should_stop = all(map(lambda x: x.finished, self.agents))
            print(f'best so far: {max(len(agent.clique.nodes) for agent in self.agents)}, '
                  f'agents still alive: {len([agent for agent in self.agents if not agent.finished])}')
