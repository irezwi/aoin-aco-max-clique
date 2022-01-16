from collections import namedtuple
from subprocess import call, DEVNULL
from multiprocessing import Pool, cpu_count
from itertools import product

from maxclique.config import OUTPUT_DIR, INPUT_DIR, PYTHON, MAIN

# INPUT_FILES = INPUT_DIR.glob("**/keller*")
INPUT_FILES = [
    INPUT_DIR / "keller4.mtx",
    INPUT_DIR / "C500-9.mtx",
]

AGENTS = [
    16,
]
ITERATIONS = [
    100,
    200,
    300,
]

AcoParam = namedtuple("AcoParam", ["rho", "alpha"])
ACO_PARAMS = [
    AcoParam(0.9, 1),
    AcoParam(0.8, 1),
    AcoParam(0.9, 2),
]
REPEATS = 10


def run_ref(*args):
    file, agents_count, _, iterations = args[0]
    cmd = f'{PYTHON} {MAIN} --input {file} --output {OUTPUT_DIR / "ref" / f"{file.name}.csv"} ref --agents {agents_count * iterations}'
    call(cmd, shell=False, stdout=DEVNULL)


def run_aco(*args):
    file, agents_count, _, iterations, aco_params = args[0]
    print(f'{file.resolve().name}: {iterations=} {agents_count=} {aco_params=}')
    cmd = f'{PYTHON} {MAIN} --input {file} --output {OUTPUT_DIR / "aco" / f"{file.name}.csv"} aco --ants {agents_count} --iterations {iterations} --alpha {aco_params.alpha} --rho {aco_params.rho}'
    call(cmd, shell=False, stdout=DEVNULL)


if __name__ == '__main__':
    # args = tuple(product(INPUT_FILES, AGENTS, range(REPEATS), ITERATIONS))
    # with Pool(cpu_count()) as p:
    #     p.map(run_ref, args)

    args = tuple(product(INPUT_FILES, AGENTS, range(REPEATS), ITERATIONS, ACO_PARAMS))
    with Pool(cpu_count()) as p:
        p.map(run_aco, args)
