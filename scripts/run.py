from pathlib import Path
from subprocess import call, DEVNULL
from multiprocessing import Pool, cpu_count
from itertools import product

PROJECT_ROOT = Path(__file__) / ".." / ".."
PYTHON = PROJECT_ROOT / 'venv' / 'Scripts' / 'python.exe'
INPUT_FILES = (PROJECT_ROOT / "input").glob("**/*")
OUTPUT_DIR = PROJECT_ROOT / "output"
MAIN = PROJECT_ROOT / "main.py"
AGENTS = [16, 32, 64, 128, 256]
ITERATIONS = [100, 500, 1000]
ALPHAS = [0.8, 0.9, 0.99]
RHOS = [1, 2, 3]
REPEATS = 10


def run_ref(*args):
    print(args)
    file, agents_count, _ = args[0]
    cmd = f'{PYTHON} {MAIN} --input {file} --output {OUTPUT_DIR / "ref" / f"{file.name}.csv"} ref --agents {agents_count}'
    call(cmd, shell=False, stdout=DEVNULL)


def run_aco(*args):
    print(args)
    file, agents_count, _, iterations, alpha, rho = args[0]
    cmd = f'{PYTHON} {MAIN} --input {file} --output {OUTPUT_DIR / "aco" / f"{file.name}.csv"} aco --ants {agents_count} --iterations {iterations} --alpha {alpha} --rho {rho}'
    call(cmd, shell=False, stdout=DEVNULL)


if __name__ == '__main__':
    args = tuple(product(INPUT_FILES, AGENTS, range(REPEATS)))
    with Pool(cpu_count()) as p:
        p.map(run_ref, args)

    args = tuple(product(INPUT_FILES, AGENTS, range(REPEATS), ITERATIONS, ALPHAS, RHOS))
    with Pool(cpu_count()) as p:
        p.map(run_aco, args)
