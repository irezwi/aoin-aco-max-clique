from abc import ABCMeta, abstractmethod
import random
import time

from graph import Clique


class Algorithm(metaclass=ABCMeta):
    def __init__(self, graph, output):
        self.graph = graph
        self.output = output

    @abstractmethod
    def run(self):
        raise NotImplementedError


class ExecutionResult:
    def __init__(self, *args, **kwargs):
        self.__dict__ |= kwargs

    def save(self, file_path):
        file_path.write(','.join(map(str, vars(self).values())))
        file_path.write('\n')


class Agent:
    def __init__(self, graph):
        self.clique = Clique(graph)
        # Initialize clique with randomly chosen node
        self.clique.add_node(random.choice(list(graph.nodes)))
        self.graph = graph
        self.finished = False

    def __repr__(self):
        return f'{self.__class__.__name__}(clique_size={len(self.clique.nodes)}, finished={self.finished})'


class AntColonyOptimizerAlgorithm(Algorithm):
    T_MIN = 0.01
    T_MAX = 5

    def __init__(self, graph, output, iterations, ants, alpha, rho):
        super().__init__(graph, output)
        self.iterations = iterations
        self.ants = ants
        self.alpha = alpha
        self.rho = rho

    def __initialize_pheromone(self):
        for edge in self.graph.edges:
            edge.pheromone = self.T_MAX

    def __evaporate_pheromone(self):
        for edge in self.graph.edges:
            edge.pheromone = max(edge.pheromone * self.rho, self.T_MIN)

    def __lay_pheromone(self, iter_best: Clique, runtime_best: Clique):
        for edge in iter_best.edges:
            edge.pheromone = min(edge.pheromone + 1 / (1 + len(runtime_best.nodes) - len(iter_best.nodes)), self.T_MAX)

    def run(self):
        start_time = time.time()
        self.__initialize_pheromone()

        current_iteration = 0
        runtime_best = None

        while current_iteration < self.iterations:
            ants = [Agent(self.graph) for _ in range(self.ants)]
            for ant in ants:
                while candidates := ant.clique.get_candidates():

                    ph_factors = [ant.clique.get_pheromone_factor(candidate) ** self.alpha for candidate in candidates]
                    # ph_probabi = [factor / sum(ph_factors) for factor in ph_factors]

                    next_node = random.choices(population=candidates, weights=ph_factors, k=1)[0]
                    ant.clique.add_node(next_node)

            iter_best = sorted([ant.clique for ant in ants], key=lambda c: len(c.nodes))[-1]
            if not runtime_best or len(iter_best.nodes) > len(runtime_best.nodes):
                runtime_best = iter_best
            self.__evaporate_pheromone()
            self.__lay_pheromone(iter_best, runtime_best)

            print(f'{current_iteration}: {len(runtime_best.nodes)}')
            current_iteration += 1

        return ExecutionResult(
            ants=self.ants,
            alpha=self.alpha,
            rho=self.rho,
            best_clique_size=len(runtime_best.nodes),
            execution_time=time.time() - start_time,
        )


class ReferenceAlgorithm(Algorithm):
    def __init__(self, graph, output, agents):
        super().__init__(graph, output)
        self.agents = [Agent(graph) for _ in range(agents)]

    def run(self):
        best_clique_size = -1
        start_time = time.time()

        for agent in self.agents:
            while not agent.finished:
                if candidates := agent.clique.get_candidates():
                    # Select next node by random choice weighted by edges count
                    next_node = random.choices(
                        candidates, weights=[len(self.graph.get_node_edges(node)) for node in candidates], k=1)[0]
                    agent.clique.add_node(next_node)
                else:
                    agent.finished = True

            best_clique_size = max(len(agent.clique.nodes) for agent in self.agents)
            print(f'best so far: {best_clique_size}, '
                  f'last result: {len(agent.clique.nodes)}, '
                  f'agents still alive: {len([agent for agent in self.agents if not agent.finished])}')

        execution_time = time.time() - start_time
        return ExecutionResult(
            agents=len(self.agents),
            best_clique_size=best_clique_size,
            execution_time=execution_time,
        )
