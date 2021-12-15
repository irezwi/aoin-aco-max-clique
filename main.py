from argparse import ArgumentParser, FileType

from graph import Graph
from algorithms import AntColonyOptimizerAlgorithm, ReferenceAlgorithm

arg_parser = ArgumentParser()
arg_parser.add_argument('--input', type=FileType('r'))
arg_parser.add_argument('--output', type=FileType('a+'))

subparsers = arg_parser.add_subparsers(dest='algorithm')

aco = subparsers.add_parser('aco')
aco.add_argument('--iterations', help="Number of algorithm iterations", type=int, default=1000)
aco.add_argument('--ants', help="Ants count", type=int, default=10)

ref = subparsers.add_parser('ref')
ref.add_argument('--agents', help="Agents count", type=int)

if __name__ == '__main__':
    args = arg_parser.parse_args()

    graph = Graph.read_from_file(args.input)
    if args.algorithm == 'aco':
        aco = AntColonyOptimizerAlgorithm(
            graph=graph,
            iterations=args.iterations,
            ants=args.ants,
            output=args.output,
        )
        aco.run()
    elif args.algorithm == 'ref':
        ref = ReferenceAlgorithm(
            output=args.output,
            graph=graph,
            agents=args.agents,
        )
        result = ref.run()
        result.save(args.output)
        print(f'Execution time: {result.execution_time}')
    else:
        print(f'Invalid algorithm: {args.algorithm}. Supported algorithms: aco, ref')
