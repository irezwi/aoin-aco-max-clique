import sys
from pathlib import Path

""" Project level configs """
PROJECT_ROOT = (Path(__file__) / ".." / ".." / "..").resolve()
SRC_ROOT = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"
INPUT_DIR = PROJECT_ROOT / "input"
BENCHMARK_RESULT = OUTPUT_DIR / "aco" / "rank_C500-9.mtx.csv"
MAIN = SRC_ROOT / "maxclique" / "main.py"

""" User level configs """
PYTHON = sys.executable
