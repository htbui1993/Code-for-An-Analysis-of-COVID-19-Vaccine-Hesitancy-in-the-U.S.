from utils import *

plt.style.use("ggplot")


if __name__ == "__main__":
    start_time = time.time()

    plot_df = pd.read_csv(f"{data_folder}/figS3_data.csv")
    plt.figure(figsize=(8, 2.5))
    bars = plt.bar(plot_df["internet_access_group"], plot_df["avg_tweet_count"], color=colors)

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
    access_ranges = ["$\leq 60\%$", "$> 60\%$  and $\leq 80\%$", "$> 80\%$"]
    for bar, access_range in zip(bars, access_ranges):
        plt.text(
            bar.get_x() + bar.get_width() / 2, 0, access_range, ha="center", va="bottom", fontsize=10, color="blue"
        )

    plt.title("Average Tweet Count by Internet Access Group", color="black")
    plt.xlabel("Internet Access Group", color="black")
    plt.ylabel("Average Tweet Count", color="black")
    plt.tight_layout()

    # Export the figure
    plt.savefig(f"{image_folder}/avg_tweet_count_by_internet_access_group.png", dpi=300, bbox_inches="tight")

    print(f"--- Finished exporting figure S3, took {time.time() - start_time:,.2f} seconds ---")
