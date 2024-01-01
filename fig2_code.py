from utils import *

plt.style.use("ggplot")


def get_surrounded_counties(df, wq, fips, verbose=True):
    lookup_idx = df[df["fips"] == fips].index.values[0]
    sur_df = df[df.index.isin(wq[lookup_idx].keys())]
    sur_fips = sur_df["fips"].values
    sur_counties = sur_df["county"].values
    print(f"+ Surrounded counties: {', '.join(sur_counties)}") if verbose else None
    return (sur_df, sur_fips)


def fill_missing_values_with_mean(df, wq, missing_fips, fill_col):
    sur_df, _ = get_surrounded_counties(df, wq, missing_fips, verbose=False)
    mean_val = sur_df[fill_col].mean()
    return mean_val


def fill_missing_VHb_surrounding_counties(df, wq, verbose=True):
    """Fill missing VHb values with mean of surrounding counties

    Args:
        df (DataFrame): Dataframe with VHb values
        wq (Weight Object): Weight object
        verbose (bool, optional): Print some statement. Defaults to True.

    Returns:
        DataFrame: Dataframe with filled VHb values
    """
    missing_fips_list = df[df["VHb"].isna()]["fips"].to_list()
    count_before = len(missing_fips_list)
    for fips in missing_fips_list:
        fips_idx = df[df["fips"] == fips].index[0]
        fill_val = fill_missing_values_with_mean(df, wq, fips, "VHb")
        df.loc[fips_idx, "VHb"] = fill_val

    count_after = df[df["VHb"].isna()].shape[0]
    print(f"+ Number of counties with missing VHb: {count_before} => {count_after}.") if verbose else None
    return df


def get_wq(gdf):
    wq = lps.weights.Rook.from_dataframe(gdf, use_index=False, silence_warnings=True)
    wq.transform = "r"
    return wq


def cal_gvf(df, val_col="VHb", clu_col="cluster", verbose=True):
    """Calculate the goodness of variance fit for a given dataframe."""
    temp = df.copy()
    temp["mean_all"] = temp[val_col].mean()
    temp["mean_cluster"] = temp.groupby(clu_col)[val_col].transform("mean")
    temp["square_deviation_all"] = (temp[val_col] - temp["mean_all"]) ** 2
    temp["square_deviation_cluster"] = (temp[val_col] - temp["mean_cluster"]) ** 2
    sdam = temp["square_deviation_all"].sum()
    sdcm = temp["square_deviation_cluster"].sum()
    gvf = (sdam - sdcm) / sdam
    if verbose:
        print(f"- Sum of Squared Deviations for Array Mean (SDAM): {sdam:,.2f}")
        print(f"- Sum of Squared Deviations for Cluster Means (SDCM): {sdcm:,.2f}")
        print(f"- Goodness of Variance Fit (GVF): {gvf:,.2f}")

    return gvf


def get_clusters_FJ(df, wq, k=5):
    df = fill_missing_VHb_surrounding_counties(df, wq, verbose=False)
    VHb_stats = df["VHb"].describe()
    df["VHb_lag"] = lps.weights.lag_spatial(wq, df["VHb"])
    df["VHb"] = df["VHb"].clip(
        lower=VHb_stats["mean"] - 3 * VHb_stats["std"],
        upper=VHb_stats["mean"] + 3 * VHb_stats["std"],
    )

    VHb_lag_stats = df["VHb_lag"].describe()
    df["VHb_lag"] = df["VHb_lag"].clip(
        lower=VHb_lag_stats["mean"] - 3 * VHb_lag_stats["std"],
        upper=VHb_lag_stats["mean"] + 3 * VHb_lag_stats["std"],
    )

    classifier_normal = mc.FisherJenks(df["VHb"], k=k)
    classifier_lag = mc.FisherJenks(df["VHb_lag"], k=k)
    df["cluster"] = classifier_normal.yb
    df["cluster_lag"] = classifier_lag.yb
    return df


# Load the datasets
counties = gpd.read_file(f"{data_folder}/county_shapes.geojson", dtype={"FIPS": str})
wq = get_wq(counties)

vh_df = pd.read_csv(
    f"{data_folder}/fig2_data.csv",
    usecols=["fips", "VHb"],
    dtype={"fips": str},
)

# Extract the data for the given week
plot_df = pd.merge(
    counties[["fips", "geometry", "state", "county"]],
    vh_df[["fips", "VHb"]],
    on="fips",
    how="left",
)

if __name__ == "__main__":
    start_time = time.time()
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.5), width_ratios=[1, 1.5, 3])
    ax1, ax2, ax3 = axes

    ######## First Subplot ########
    # Calculate GVF for different number of clusters
    xs, ys = [], []
    for k in range(2, 15):
        cluster_df = get_clusters_FJ(plot_df, wq, k=k)
        GVF = cal_gvf(cluster_df, val_col="VHb", clu_col="cluster", verbose=False)
        xs.append(k)
        ys.append(GVF)

    ax1.axvline(x=5, color="red", linestyle="--", lw=1)
    ax1.plot(xs, ys, "ko-", mfc="white", mec="k", ms=4, lw=1)
    ax1.set_xlabel("Number of Clusters ($k$)", color="black")
    ax1.set_xticks([2, 4, 5, 6, 8, 10, 12, 14])
    ax1.set_xticklabels(["2", "4", "5", "6", "8", "10", "12", "14"], color="black")
    xticks = ax1.get_xticklabels()
    for i, xtick in enumerate(xticks):
        if i == 2:
            color, weight, size = "red", "bold", 10
        else:
            color, weight, size = "k", "normal", 10
        xtick.set_color(color)
        xtick.set_fontweight(weight)

    ax1.set_title(r"\textbf{a)}")
    ax1.set_ylabel("Goodness of Variance Fit", color="black")
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    ax1.xaxis.set_tick_params(width=1, length=4)
    ax1.yaxis.set_tick_params(width=1, length=4)
    ax1.set_ylim([0.65, 1.05])
    # add_grid(ax1)

    ######## Second Subplot ########
    n, bins, patches = ax2.hist(
        x=plot_df["VHb"].values,
        bins=50,
        density=False,
        color=colors[0],
        align="mid",
        ec="k",
        lw=0.4,
        alpha=0.8,
    )

    classifier = mc.FisherJenks(plot_df["VHb"], k=5)
    bins = np.insert(classifier.bins, 0, plot_df["VHb"].min(), axis=0)

    # Add vertical lines for the bins in the second subplot
    for bin in bins:
        ax2.axvline(x=bin, color="red", linestyle="--", linewidth=1)
        ax2.annotate(
            text=f"{bin:.2f}",
            xy=(bin, 220),
            textcoords="offset points",
            xytext=(2, 0),
            ha="left",
        )

    ax2.set_title(r"\textbf{b)}")
    ax2.set_xlabel("VH$^b$", color="black")
    ax2.set_ylabel("Count", color="black")
    ax2.xaxis.set_ticks_position("bottom")
    ax2.set_xticks([0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.00])
    ax2.set_xticklabels(["$\leq$0.86", "0.88", "0.90", "0.92", "0.94", "0.96", "0.98", "1.00"], color="black")
    ax2.set_ylim([0, 240])
    ax2.yaxis.set_ticks_position("left")
    ax2.xaxis.set_tick_params(width=1, length=4, gridOn=False)
    ax2.yaxis.set_tick_params(width=1, length=4)
    # add_grid(ax2)

    ######## Third Subplot - Map ########
    plot_df.plot(
        column="VHb",
        cmap="coolwarm",
        scheme="fisherjenks",
        k=5,
        linewidth=0.2,
        ax=ax3,
        edgecolor="black",
        legend=True,
        legend_kwds={
            "loc": "lower right",
            "interval": True,
            "fancybox": True,
            "facecolor": "#FAF7F7",
            "ncols": 3,
            "bbox_to_anchor": (0.95, -0.15),
            "fontsize": 10,
        },
    )
    legends = ax3.get_legend()
    legend_texts = legends.get_texts()
    for i, text in enumerate(legend_texts):
        text.set_text(f"C{i+1}: {text.get_text()}")

    ax3.set_title(r"\textbf{c)}")
    ax3.axis("off")

    # Export the figure
    # fig.tight_layout()
    plt.savefig(f"{image_folder}/GVF_map_v2.png", dpi=300, bbox_inches="tight")
    print(f"--- Finished exporting figure  2, took {time.time() - start_time:,.2f} seconds ---")