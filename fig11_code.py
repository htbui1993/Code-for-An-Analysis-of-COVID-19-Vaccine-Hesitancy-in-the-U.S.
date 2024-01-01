from utils import data_folder, image_folder
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import matplotlib.colors as mc
from matplotlib.ticker import MultipleLocator, FixedFormatter, FixedLocator, FormatStrFormatter

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
    plot_df = pd.read_csv(f"{data_folder}/fig11_data.csv")
    
    fig, ax = plt.subplots(figsize=(10, 3.7))

    for idx, i in enumerate([13, 14, 29, 31, 34], start=1):
        ax.axvline(x=i, c="black", ls="--", lw=1)
        ax.text(i + 0.2, 2, f"({idx})")
        
    x = plot_df["Week"].to_list()
    y_c1 = plot_df["C1 Ranking"].to_list()
    y_c5 = plot_df["C5 Ranking"].to_list()
    fname = plot_df["Feature"].values[0]

    c1, c2 = "#1F77B4", "#FF7F0E"
    mfc1, mfc2 = lighten_color(c1, 0.5), lighten_color(c2, 0.5)
    ax.plot(x, y_c1, "o-", mfc=mfc1, ms=5, c=c1, label="Cluster 1")
    ax.plot(x, y_c5, "X--", mfc=mfc2, ms=6, c=c2, label="Cluster 5")

    ax.set_title("Stringency Index")
    ax.set_xlabel("Week Numbers")
    ax.set_ylabel("Feature Importance Ranking")

    ax.set_xlim(4-0.5, plot_df["Week"].max() + 0.5)

    show_week_labels = plot_df[plot_df["week_number"].isin(np.arange(5,41,5))]["w_month_year"].to_list()
    ax.set_xticklabels([0] + show_week_labels)
    # ax.tick_params(axis='both', labelsize= 10)

    ax.set_ylim(0.5, plot_df[["C1 Ranking", "C5 Ranking"]].max().max() + 2)
    ax.yaxis.set_major_locator(FixedLocator([1, 5, 10, 15, 20, 25, 30]))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # ax.set_facecolor("white")
    # ax.grid(axis="x", color="lightgrey")
    # ax.grid(axis="y", which="major", color="lightgrey")

    ax.spines['left'].set_color('grey')
    ax.spines['bottom'].set_color('grey')


    ax.legend(facecolor="white", framealpha=1)

    ax.text(
        0.075,
        -0.15,
        "(1) W-13: CDC revised travel guidelines, differentiating between vaccinated and unvaccinated individuals.\n"
        + "(2) W-14: Strict international travel controls and quarantine requirements were enacted.\n"
        + "(3) W-29: CDC endorsed in-person instruction with safety guidelines.\n"
        + "(4) W-31: CDC updated to require universal indoor masking in K-12 schools, regardless of vaccination status.\n"
        + "(5) W-34: CDC enforced mask-wearing on all forms of public transportation.",
        transform=plt.gcf().transFigure,
        bbox=dict(boxstyle="round", facecolor="#E5E5E5"),
    )


    ax.invert_yaxis()
    plt.tight_layout()
    # Export the figure
    plt.savefig(
        f"{image_folder}/(fig11)stringency_c1_c5.png",
        dpi=300,
        bbox_inches="tight",
    )
    print(
        f"--- Finished exporting figure  11, took {time.time() - start_time:,.2f} seconds ---"
    )