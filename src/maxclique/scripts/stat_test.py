from itertools import permutations

import pandas as pd
import numpy as np
from scipy.stats import wilcoxon

from maxclique.config import OUTPUT_DIR, PROJECT_ROOT
from maxclique.scripts.run import TESTED_FILES

ALPHA = .05

files = [f"{file}.csv" for file in TESTED_FILES]

for file in files:
    file_name = file.split(".")[0]

    aco_results = pd.read_csv(
        OUTPUT_DIR / "aco" / file,
        names=["ants", "iterations", "alpha", "rho", "score", "t"],
    )
    ref_results = pd.read_csv(
        OUTPUT_DIR / "ref" / file,
        names=["iterations", "score", "t"],
    )

    # To compare both algorithms we introduced "searches" column which is equal to agents * iterations
    # For reference algorithm len(agents) == 1 so "searches" is always equal to "iterations"
    ref_results["searches"] = ref_results["iterations"]
    aco_results["searches"] = aco_results["ants"] * aco_results["iterations"]

    aco_results['algorithm'] = 'ACO(' + aco_results['searches'].astype(str) + ', ' \
                               + aco_results['alpha'].astype(str) + ', ' \
                               + aco_results['rho'].astype(str) + ')'
    ref_results['algorithm'] = 'REF(' + ref_results['searches'].astype(str) + ')'
    ref_results.drop(columns=['iterations', 'searches'], inplace=True)
    aco_results.drop(columns=['ants', 'iterations', 'alpha', 'rho', 'searches'], inplace=True)

    all_results = pd.concat([ref_results, aco_results])

    all_results.set_index('algorithm', inplace=True)

    algorithms = list(np.unique(all_results.index.values))
    all_pairs = list(permutations(algorithms, 2))

    mean_results = all_results.groupby(['algorithm']).mean()
    mean_results = mean_results.reset_index()
    mean_results['better_score_than'] = [[] for _ in range(len(mean_results))]
    mean_results['better_t_than'] = [[] for _ in range(len(mean_results))]
    mean_results.index.name = 'L.p.'

    params = (
        ('score', 'greater'),
        ('t', 'less'),
    )

    for alg1, alg2 in all_pairs:
        for param_name, param_comparison in params:
            alg1_values = all_results[all_results.index == alg1][param_name]
            alg2_values = all_results[all_results.index == alg2][param_name]

            w, p = wilcoxon(alg1_values, alg2_values, alternative=param_comparison, zero_method='zsplit')

            alg1_idx = (mean_results['algorithm'] == alg1).argmax()
            alg2_idx = (mean_results['algorithm'] == alg2).argmax()

            if p < ALPHA:
                mean_results.at[alg1_idx, f'better_{param_name}_than'].append(alg2_idx)

    with open(PROJECT_ROOT / "tables" / f'{file_name}_stats.md', 'w') as f:
        f.write(mean_results.to_markdown())
