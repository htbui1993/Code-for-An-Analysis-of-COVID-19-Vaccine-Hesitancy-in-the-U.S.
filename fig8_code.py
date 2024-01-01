import shap

from utils import *

plt.style.use("ggplot")
# plt.rcParams.update(
#     {
#         # "font.family": "Times New Roman",
#         "text.usetex": False,
#     }
# )

if __name__ == "__main__":
    start_time = time.time()

    # Read in the data
    shap_df = pd.read_csv(f"{data_folder}/fig8_data1.csv", index_col=0)
    value_df = pd.read_csv(f"{data_folder}/fig8_data2.csv")
    column_names_formatted = [textwrap.fill(text=i, width=40) for i in shap_df.columns]
    # Put \ in font of % and _ to avoid latex rendering
    column_names_formatted = [i.replace("%", "\\%").replace("_", "\\_") for i in column_names_formatted]

    fig = plt.figure(figsize=([35, 20]))

    gs = GridSpec(2, 6, wspace=40, hspace=0.2)

    ax1 = plt.subplot(gs[0, :2])
    shap.summary_plot(
        shap_df.loc["c1"].values,
        value_df.values,
        feature_names=column_names_formatted,
        cmap=plt.get_cmap("Spectral"),
        alpha=0.8,
        plot_size=None,
        show=False,
        max_display=15,
        color_bar=False,
    )

    ax2 = plt.subplot(gs[0, 2:4])
    shap.summary_plot(
        shap_df.loc["c2"].values,
        value_df.values,
        feature_names=column_names_formatted,
        cmap=plt.get_cmap("Spectral"),
        alpha=0.8,
        plot_size=None,
        show=False,
        max_display=15,
        color_bar=False,
    )

    ax3 = plt.subplot(gs[0, 4:6])
    shap.summary_plot(
        shap_df.loc["c3"].values,
        value_df.values,
        feature_names=column_names_formatted,
        cmap=plt.get_cmap("Spectral"),
        alpha=0.8,
        plot_size=None,
        show=False,
        max_display=15,
        color_bar=False,
    )

    ax4 = plt.subplot(gs[1, 1:3])
    shap.summary_plot(
        shap_df.loc["c4"].values,
        value_df.values,
        feature_names=column_names_formatted,
        cmap=plt.get_cmap("Spectral"),
        alpha=0.8,
        plot_size=None,
        show=False,
        max_display=15,
        color_bar=False,
    )

    ax5 = plt.subplot(gs[1, 3:5])
    shap.summary_plot(
        shap_df.loc["c5"].values,
        value_df.values,
        feature_names=column_names_formatted,
        cmap=plt.get_cmap("Spectral"),
        alpha=0.8,
        plot_size=None,
        show=False,
        max_display=15,
        color_bar=False,
    )

    # Set the labels
    for ax, title in zip(
        [ax1, ax2, ax3, ax4, ax5],
        [
            "a) Cluster 1",
            "b) Cluster 2",
            "c) Cluster 3",
            "d) Cluster 4",
            "e) Cluster 5",
        ],
    ):
        ax.set_xlabel("SHAP Value", labelpad=0, fontsize=24, color="black")
        ax.set_title(title, fontsize=30, color="black")
        ax.tick_params(axis="both", which="major", labelsize=24, color="black")
        ax.tick_params(axis="y", labelcolor="black", pad=2, length=0)

    cmap = mpl.cm.Spectral
    norm = mpl.colors.Normalize(vmin=0, vmax=1)

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.84, 0.12, 0.01, 0.76])
    cb = mpl.colorbar.ColorbarBase(ax=cbar_ax, cmap=cmap, norm=norm, orientation="vertical")
    cb.set_label("Scaled Feature Value", labelpad=5, fontsize=30, rotation=90, color="black")
    cb.set_ticks([0, 0.5, 1])
    cb.set_ticklabels(["0 (Low)", "0.5", "1 (High)"], color="black")
    cb.ax.tick_params(labelsize=24)
    cb.outline.set_color("black")
    cb.outline.set_linewidth(1)
    cbar_ax.yaxis.set_label_position("left")

    # Export the figure
    plt.savefig(
        f"{image_folder}/shap_values_all_clusters.png",
        dpi=300,
        bbox_inches="tight",
    )
    print(f"--- Finished exporting figure  8, took {time.time() - start_time:,.2f} seconds ---")
