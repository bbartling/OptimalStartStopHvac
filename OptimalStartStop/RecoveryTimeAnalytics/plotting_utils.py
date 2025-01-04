import matplotlib.pyplot as plt
import seaborn as sns
import os


def plot_line_chart(subset_data, occupied_threshold, unoccupied_threshold, output_dir):
    line_plot_path = os.path.join(output_dir, "SpaceTemp_Plot.png")
    plt.figure(figsize=(15, 7))
    plt.plot(
        subset_data.index,
        subset_data["SpaceTemp"],
        label="SpaceTemp",
        color="blue",
        linewidth=1,
    )
    plt.scatter(
        subset_data[subset_data["Warm_Up_Active"] == 1].index,
        subset_data[subset_data["Warm_Up_Active"] == 1]["SpaceTemp"],
        color="red",
        label="Warm_Up_Active",
        zorder=5,
    )
    plt.axhline(
        occupied_threshold, color="purple", linestyle="--", label="Occupied Threshold"
    )
    plt.axhline(
        unoccupied_threshold, color="gray", linestyle="--", label="Unoccupied Threshold"
    )
    plt.fill_between(
        subset_data.index,
        unoccupied_threshold - 1,
        unoccupied_threshold + 1,
        color="gray",
        alpha=0.2,
        label="±1°F Unoccupied Range",
    )
    plt.fill_between(
        subset_data.index,
        occupied_threshold - 1,
        occupied_threshold + 1,
        color="purple",
        alpha=0.2,
        label="±1°F Occupied Range",
    )
    plt.title("SpaceTemp with Warm_Up_Active", fontsize=16)
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Temperature (°F)", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(line_plot_path)
    plt.close()
    print(f"Line plot saved to {line_plot_path}")


def plot_bar_chart(results, output_dir):
    bar_plot_path = os.path.join(output_dir, "Warm_Up_Bar_Plot.png")
    fig, ax1 = plt.subplots(figsize=(15, 7))

    ax1.bar(
        results.index,
        results["Warm_Up_Duration (minutes)"],
        color="skyblue",
        label="Warm-Up Duration (minutes)",
        alpha=0.8,
    )
    ax1.set_ylabel("Warm-Up Duration (minutes)", fontsize=12)
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_title("Warm-Up Duration with 4AM Temperatures", fontsize=16)
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.scatter(
        results.index,
        results["4AM OaTemp"],
        color="red",
        label="4AM OaTemp",
        zorder=5,
    )
    ax2.scatter(
        results.index,
        results["4AM SpaceTemp"],
        color="green",
        label="4AM SpaceTemp",
        zorder=5,
    )
    ax2.set_ylabel("Temperature (°F)", fontsize=12)

    fig.legend(
        loc="upper right", bbox_to_anchor=(1, 0.95), bbox_transform=ax1.transAxes
    )
    plt.tight_layout()
    plt.savefig(bar_plot_path)
    plt.close()
    print(f"Bar plot with additional data saved to {bar_plot_path}")


def plot_temperature_distribution(subset_data, output_dir, label):
    # Simple Histogram Plot
    simple_hist_path = os.path.join(output_dir, f"Histogram.png")
    plt.figure(figsize=(12, 6))
    subset_data["SpaceTemp"].plot(kind="hist", bins=30, alpha=0.8, color="blue")
    plt.title(f"Temperature Histogram ({label})", fontsize=16)
    plt.xlabel("Space Temperature (°F)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(simple_hist_path)
    plt.close()
    print(f"Simple histogram plot saved to {simple_hist_path}")


def plot_degrees_per_hour(results, output_dir):
    line_plot_path = os.path.join(output_dir, "Degrees_Per_Hour.png")

    # Calculate Degrees per Hour
    data_to_plot = results["4AM SpaceTemp"] / (
        results["Warm_Up_Duration (minutes)"] / 60
    )

    # Handle inf and NaN values
    data_to_plot.replace([float("inf"), float("-inf")], float("nan"), inplace=True)
    data_to_plot.dropna(inplace=True)

    # Plot Degrees per Hour without x-axis labels
    plt.figure(figsize=(12, 6))
    plt.plot(data_to_plot, marker="o", color="blue", label="Degrees per Hour")
    plt.title("Degrees per Hour In Warmups", fontsize=16)
    plt.ylabel("Degrees per Hour (°F/hr)", fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(line_plot_path)
    plt.close()
    print(f"Line plot saved to {line_plot_path}")



def plot_relationship_matrix(results, output_dir):
    """
    Plot a pairplot to show relationships between warm-up duration, temperatures, and day of the week.
    """
    plot_path = os.path.join(output_dir, "Relationship_Matrix.png")

    # Convert Day_of_Week to the full day name for better visualization
    results["Day_of_Week"] = results.index.day_name()

    # Select relevant columns
    data_to_plot = results[
        ["Warm_Up_Duration (minutes)", "4AM OaTemp", "4AM HwsTemp", "Day_of_Week"]
    ]

    # Pairplot with hue as Day_of_Week
    sns.set(style="ticks")
    pairplot = sns.pairplot(
        data_to_plot,
        hue="Day_of_Week",
        palette="viridis",
        diag_kind="kde",
        plot_kws={"alpha": 0.6},
    )
    pairplot.fig.suptitle("Relationships Between Warm-Up Duration, Temperatures, and Day of the Week", y=1.02)

    # Save the plot
    pairplot.savefig(plot_path)
    plt.close()
    print(f"Relationship matrix plot saved to {plot_path}")

