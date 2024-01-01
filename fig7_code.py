from utils import *

plt.style.use("ggplot")
plt.rcParams.update(
    {
        "text.usetex": False,
    }
)

if __name__ == "__main__":
    start_time = time.time()

    # Read in the data
    plot_df = pd.read_csv(f"{data_folder}/fig7_data.csv")

    x = plot_df["week_number"]
    show_weeks = np.arange(5, 41, 5)
    y_intent_mean = plot_df["us_sni_covid19_vaccination"]

    y_vhb_mean = plot_df["VHb_mean"]

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax2 = ax.twinx()

    for idx, i in enumerate([8, 10, 16, 24, 32], start=1):
        ax.axvline(x=i, c="black", ls="--", lw=1)
        ax.text(i + 0.2, 98, f"({idx})")

    c1, c2 = "#000000", "#1F77B4"
    mfc1, mfc2 = lighten_color(c1, 0.5), lighten_color(c2, 0.5)

    ax.plot(
        x,
        y_intent_mean,
        "o-",
        mfc=mfc1,
        c=c1,
        lw=1,
        mew=1,
        alpha=1,
        label="Google Search Insights",
    )
    ax2.plot(
        x,
        y_vhb_mean,
        "o--",
        mfc=mfc2,
        c=c2,
        lw=1,
        mew=1,
        alpha=1,
        label=r"Average VH$^b$",
    )

    show_week_labels = plot_df[plot_df["week_number"].isin(show_weeks)]["w_month_year"].to_list()

    ax.set_xlabel("Week Numbers" , color="black")
    ax.set_xlim(3.5, 43.5)
    ax.xaxis.set_major_locator(FixedLocator(show_weeks))
    ax.set_xticklabels(show_week_labels)
    ax.set_ylabel("Google Search Insights (Vaccination)", color=c1)
    ax2.set_ylabel("Average VH$^b$", color=c2)
    ax.tick_params(axis="y", colors=c1)
    ax2.tick_params(axis="y", colors=c2)
    ax2.grid(False)

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            ls="-",
            mfc=mfc1,
            mew=1,
            lw=1,
            c=c1,
            label="Google Search Insights (Vaccination)",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            ls="--",
            c=c2,
            mew=1,
            lw=1,
            mfc=mfc2,
            label=r"Average VH$^b$",
        ),
    ]

    ax.legend(
        handles=legend_elements,
        ncol=2,
        loc="upper left",
        fancybox=False,
        shadow=False,
        facecolor="white",
        frameon=False,
        fontsize=10,
        bbox_to_anchor=(0, 1.15),
    )

    txt = ax.text(
        1.15,
        0.98,
        "(1) Feb 27, 2021: The FDA authorized the Janssen COVID-19 vaccine for individuals of ages 18 or older.\n"
        + "(2) Mar 2, 2021: Teachers, school staff, and child care workers were eligible to vaccinate.\n"
        + "(3) Apr 19, 2021: All individuals of ages 16 or older were eligible to vaccinate.\n"
        + "(4) Jun 1, 2021: The 'Delta' variant  dominates and triggers a summer 2021 wave of infections.\n"
        + "(5) Aug 12, 2021: The FDA authorized a second dose of COVID-19 vaccine for immunocompromised individuals.",
        transform=ax.transAxes,
        bbox=dict(boxstyle="round", facecolor="#FAF7F7"),
        va="top",
        ha="left",
        wrap=True,
    )
    txt._get_wrap_line_width = lambda: 700

    # plt.tight_layout()
    plt.savefig(f"{image_folder}/search_insights_v2.png", dpi=300, bbox_inches="tight")
    print(f"--- Finished exporting figure  7, took {time.time() - start_time:,.2f} seconds ---")
