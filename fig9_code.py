from utils import *

plt.style.use("ggplot")
plt.rcParams.update(
    {
        "text.usetex": False,
    }
)

if __name__ == "__main__":
    start_time = time.time()
    plot_df = pd.read_csv(f"{data_folder}/fig9_data.csv")

    fig, ax = plt.subplots(figsize=(8, 3.5))

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

    ax.set_title("Stringency Index Ranking For Cluster 1 and Cluster 5", color="black")
    ax.set_xlabel("Week Numbers", color="black")
    ax.set_ylabel("Feature Importance Ranking", color="black")

    ax.set_xlim(4 - 0.5, plot_df["Week"].max() + 0.5)

    show_week_labels = plot_df[plot_df["week_number"].isin(np.arange(5, 41, 5))]["w_month_year"].to_list()
    ax.set_xticklabels([0] + show_week_labels, color="black")

    ax.set_ylim(0.5, plot_df[["C1 Ranking", "C5 Ranking"]].max().max() + 2)
    ax.yaxis.set_major_locator(FixedLocator([1, 5, 10, 15, 20, 25, 30]))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    

    ax.spines["left"].set_color("grey")
    ax.spines["bottom"].set_color("grey")

    ax.legend(facecolor="white", framealpha=1)
    ax.invert_yaxis()
    plt.tight_layout()
    txt = ax.text(
        1.01,
        0.98,
        "(1) W-13: CDC revised travel guidelines, differentiating between vaccinated and unvaccinated individuals.\n"
        + "(2) W-14: Strict international travel controls and quarantine requirements were enacted.\n"
        + "(3) W-29: CDC endorsed in-person instruction with safety guidelines.\n"
        + "(4) W-31: CDC updated to require universal indoor masking in K-12 schools, regardless of vaccination status.\n"
        + "(5) W-34: CDC enforced mask-wearing on all forms of public transportation.",
        transform=ax.transAxes,
        bbox=dict(boxstyle="round", facecolor="#FAF7F7"),
        va="top",
        ha="left",
        wrap=True,
    )

    txt._get_wrap_line_width = lambda: 700

    # Export the figure
    plt.savefig(
        f"{image_folder}/ranking_stringency_v2.png",
        dpi=300,
        bbox_inches="tight",
    )
    print(f"--- Finished exporting figure  9, took {time.time() - start_time:,.2f} seconds ---")
