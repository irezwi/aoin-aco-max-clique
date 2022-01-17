from collections import namedtuple
from itertools import product
from multiprocessing import Pool, cpu_count
from subprocess import DEVNULL, call

from maxclique.config import INPUT_DIR, MAIN, OUTPUT_DIR, PYTHON

AcoParam = namedtuple("AcoParam", ["rho", "alpha"])

TESTED_FILES = [
    "keller4.mtx",
    "C250-9.mtx",
    "C500-9.mtx",
    "keller5.mtx",
]
INPUT_FILES = [INPUT_DIR / file for file in TESTED_FILES]
AGENTS = [
    16,
]
ITERATIONS = [
    100,
    200,
    300,
]
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
    print(f"{file.resolve().name}: {iterations=} {agents_count=} {aco_params=}")
    cmd = f'{PYTHON} {MAIN} --input {file} --output {OUTPUT_DIR / "aco" / f"{file.name}.csv"} aco --ants {agents_count} --iterations {iterations} --alpha {aco_params.alpha} --rho {aco_params.rho}'
    call(cmd, shell=False, stdout=DEVNULL)


if __name__ == "__main__":
    args_ref = tuple(product(INPUT_FILES, AGENTS, range(REPEATS), ITERATIONS))
    args_aco = tuple(
        product(INPUT_FILES, AGENTS, range(REPEATS), ITERATIONS, ACO_PARAMS)
    )
    with Pool(cpu_count() // 2) as p:
        p.map(run_aco, args_aco)
        p.map(run_ref, args_ref)
