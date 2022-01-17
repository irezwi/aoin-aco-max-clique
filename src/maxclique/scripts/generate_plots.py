import pandas as pd
import matplotlib.pyplot as plt

from maxclique.scripts.run import TESTED_FILES
from maxclique.config import OUTPUT_DIR, PROJECT_ROOT

files = [f"{file}.csv" for file in TESTED_FILES]

for file in files:

    file_name = file.split('.')[0]

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

    aco_pivot_tbl = pd.pivot_table(data=aco_results, columns=["rho", "alpha"], index="searches")
    ref_pivot_tbl = pd.pivot_table(data=ref_results, index="searches")

    statistics = (
        ('score', 'Rozmiar', f'Średni rozmiar kliki - {file_name}'),
        ('t', 'Czas [s]', f'Średni czas wykonania - {file_name}'),
    )

    for statistic, y_label, plot_title in statistics:

        ax1 = aco_pivot_tbl[statistic].plot(label='aco')
        ax2 = ref_pivot_tbl[statistic].plot(label='reference')

        ax1.legend(
            [*(f'ACO(rho={rho}, alpha={alpha})' for rho, alpha in list(aco_pivot_tbl.score.columns.values)), 'Alg. referencyjny']
        )
        ax1.set_xticks(aco_pivot_tbl.index.values)
        ax2.set_ylabel(y_label)
        ax1.set_title(plot_title)

        plt.grid()
        plt.savefig(PROJECT_ROOT / "plots" / f"{file_name}__{statistic}.png")
