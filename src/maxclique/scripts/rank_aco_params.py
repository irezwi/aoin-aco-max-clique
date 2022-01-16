"""
Requires benchmark results to be generated
"""

import pandas as pd

from maxclique.config import BENCHMARK_RESULT

if not BENCHMARK_RESULT.exists():
    print(f"No benchmark results under {BENCHMARK_RESULT.resolve()}")
    exit(-1)

results = pd.read_csv(BENCHMARK_RESULT, names=["ants", "alpha", "rho", "score", "t"])
rank = (
    results.groupby(["rho", "alpha"])
    .mean()
    .sort_values(["score", "t"], ascending=[False, True])
)

print(rank)
