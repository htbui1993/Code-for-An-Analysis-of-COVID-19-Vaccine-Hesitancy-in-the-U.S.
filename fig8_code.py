import colorsys
import time

import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import (FixedFormatter, FixedLocator,
                               FormatStrFormatter, MultipleLocator)
from utils import data_folder, image_folder

plt.style.use("ggplot")
plt.rcParams.update(
    {
        "font.family": "CMU Serif",
        "text.usetex": False,
        "font.size": 12,
        "font.weight": "normal",
        "figure.titlesize": "medium",
        "xtick.color": "black",
        "ytick.color": "black",
        "axes.labelcolor": "black",
        "text.color": "black",
        "savefig.dpi": 300,
        "figure.dpi": 100,
    }
)


def lighten_color(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

if __name__ == "__main__":
    start_time = time.time()

    # Read in the data
    plot_df = pd.read_csv(f"{data_folder}/fig8_data.csv")
    
    fig, axes = plt.subplots(ncols=2, figsize=(10, 3.2))

    order_plot = ["Political Affiliation", "Google Search Insights"]
    alphabet = ["a)", "b)"]
    colors = ["#000000", "#D6133A"]
    for i, fname in enumerate(order_plot):
        j = plot_df[plot_df["Feature"] == fname]
        x = j["Week"].to_list()
        y_c1 = j["C1 Ranking"].to_list()
        y_c5 = j["C5 Ranking"].to_list()
        c = colors[i]
        mfc = lighten_color(c, 0.5)

        axes[i].plot(x, y_c1, "o-", c=c, mfc=mfc, lw=1, ms=4)
        axes[i].plot(x, y_c5, "X--", c=c, mfc=mfc, lw=1, ms=5)

        axes[i].annotate("C1", (x[-1] + 0.5, y_c1[-1]), ha="left", va="center", c=c, weight="bold")
        axes[i].annotate("C5", (x[-1] + 0.5, y_c5[-1]), ha="left", va="center", c=c, weight="bold")

        #     axes[i] = add_rect(5, axes[i])
        #     axes[i] = add_rect(7, axes[i])
        #     axes[i] = add_rect([9, 15],axes[i])
        #     axes[i] = add_rect(42,axes[i])
        show_week_labels = j[j["week_number"].isin(np.arange(10, 41, 10))]["w_month_year"].to_list()

        axes[i].set_title(f"{alphabet[i]} {fname}")
        axes[i].set_xticklabels([0] + show_week_labels)
        axes[i].set_xlabel("Week Numbers")

        axes[i].xaxis.set_major_locator(MultipleLocator(10))
        axes[i].yaxis.set_major_locator(FixedLocator([1, 5, 10, 15, 20, 25]))
        axes[i].yaxis.set_minor_locator(MultipleLocator(1))
        # axes[i].yaxis.set_minor_formatter(FormatStrFormatter("%.0f"))

        if i == 0:
            axes[i].set_ylabel("Feature Importance Ranking")
            axes[i].tick_params(axis="y", which="minor", labelsize=8)
            axes[i].spines["left"].set_color("grey")
        else:
            axes[i].tick_params(axis="y", which="both", length=0, width=0, labelsize=0, color="white", left=False)

        axes[i].invert_yaxis()
        axes[i].spines["bottom"].set_color("grey")

    legend_elements = [
        Line2D([0], [0], marker="o", c="k", ms=7, label="Cluster 1", mfc=lighten_color(colors[0], 0.5)),
        Line2D([0], [0], marker="X", linestyle="--", c="k", ms=7, label="Cluster 5", mfc=lighten_color(colors[0], 0.5)),
    ]

    axes[0].legend(
        handles=legend_elements,
        # bbox_to_anchor=(1.05, 0.4),
        ncol=1,
        loc="lower right",
        fancybox=True,
        frameon=True,
        shadow=False,
        facecolor="white",
    )
    plt.tight_layout()
    plt.savefig(
        f"{image_folder}/(fig8)ranking_political_search.png", dpi=300, bbox_inches="tight"
    )
    print(
        f"--- Finished exporting figure  8, took {time.time() - start_time:,.2f} seconds ---"
    )