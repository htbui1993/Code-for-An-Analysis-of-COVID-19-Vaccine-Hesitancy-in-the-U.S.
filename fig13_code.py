import time

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import data_folder, image_folder

plt.style.use("ggplot")
plt.rcParams.update(
    {
        "font.family": "Times New Roman",
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
d3_c = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"]

if __name__ == "__main__":
    start_time = time.time()

    plot_df = pd.read_csv(f"{data_folder}/fig13_data.csv")
    plt.figure(figsize=(8, 3))
    bars = plt.bar(plot_df["internet_access_group"], plot_df["avg_tweet_count"], color=d3_c)

    # Adding labels on top of each bar
    for bar, value in zip(bars, plot_df["avg_tweet_count"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            round(value, 2),
            ha="center",
            va="bottom",
            fontsize=10,
        )

    # Adding internet access range below each bar
    access_ranges = ["≤ 60%", "> 60% and ≤ 80%", "> 80%"]
    for bar, access_range in zip(bars, access_ranges):
        plt.text(
            bar.get_x() + bar.get_width() / 2, 0, access_range, ha="center", va="bottom", fontsize=10, color="blue"
        )

    plt.title("Average Tweet Count by Internet Access Group")
    plt.xlabel("Internet Access Group")
    plt.ylabel("Average Tweet Count")
    plt.tight_layout()

    # Export the figure
    plt.savefig(f"{image_folder}/(fig13)avg_tweet_count_by_internet_access_group.png", dpi=300, bbox_inches="tight")

    print(f"--- Finished exporting figure 13, took {time.time() - start_time:,.2f} seconds ---")
