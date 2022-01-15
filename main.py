from argparse import ArgumentParser, FileType

from algorithms import AntColonyOptimizerAlgorithm, ReferenceAlgorithm
from graph import Graph

arg_parser = ArgumentParser()
arg_parser.add_argument("--input", type=FileType("r"))
arg_parser.add_argument("--output", type=FileType("a+"))

subparsers = arg_parser.add_subparsers(dest="algorithm")

aco = subparsers.add_parser("aco")
aco.add_argument(
    "--iterations", help="Number of algorithm iterations", type=int, default=100
)
aco.add_argument("--ants", help="Ants count", type=int, default=100)
aco.add_argument("--alpha", help="Alpha parameter", type=float, default=2.0)
aco.add_argument("--rho", help="Rho parameter", type=float, default=0.995)

ref = subparsers.add_parser("ref")
ref.add_argument("--agents", help="Agents count", type=int, default=10)

if __name__ == "__main__":
    args = arg_parser.parse_args()
    algo = None
    graph = Graph(args.input)
    if args.algorithm == "aco":
        algo = AntColonyOptimizerAlgorithm(
            graph=graph,
            output=args.output,
            iterations=args.iterations,
            ants=args.ants,
            alpha=args.alpha,
            rho=args.rho,
        )
    elif args.algorithm == "ref":
        algo = ReferenceAlgorithm(
            output=args.output,
            graph=graph,
            agents=args.agents,
        )
    else:
        print(f"Invalid algorithm: {args.algorithm}. Supported algorithms: aco, ref")

    if algo:
        result = algo.run()
        result.save(args.output)
        print(f"Execution time: {result.execution_time}")
