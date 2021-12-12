from os import listdir
from os.path import join
from argparse import ArgumentParser, FileType

from graph import Graph
from algorithms import AntColonyOptimizerAlgorithm, ReferenceAlgorithm

arg_parser = ArgumentParser()
arg_parser.add_argument('--output', type=FileType('a+'))

subparsers = arg_parser.add_subparsers(dest='algorithm')

aco = subparsers.add_parser('aco')
aco.add_argument('--iterations', help="Number of algorithm iterations", type=int, default=1000)
aco.add_argument('--ants', help="Ants count", type=int, default=10)

subparsers.add_parser('ref')

if __name__ == '__main__':
    args = arg_parser.parse_args()

    for file in listdir('input'):
        graph = Graph.read_from_file(join('input', file))
        if args.algorithm == 'aco':
            aco = AntColonyOptimizerAlgorithm(
                graph=graph,
                iterations=args.iterations,
                ants=args.ants
            )
            aco.run()
        elif args.algorithm == 'ref':
            ref = ReferenceAlgorithm(
                output=args.output,
                graph=graph
            )
            aco.run()
        else:
            print(f'Invalid algorithm: {args.algorithm}. Supported algorithms: aco, ref')
