import time
from typing import List
import pandas as pd
import plotly.graph_objs as go

from utils import data_folder, image_folder

colors = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"]


def plot_county_annotation(fig, df, rows, cols, axs, ays, xachors):
    name = df["county"].values[0]
    state = df["state"].values[0]
    x1 = df["hesitant"].values[0]
    x2 = df["PFV"].values[0]
    y = df["VHb"].values[0]
    fig.add_annotation(
        x=x1,
        y=y,
        text=f"{name}, {state}",
        showarrow=True,
        arrowsize=1,
        xanchor=xachors[0],
        ax=axs[0],
        ay=ays[0],
        arrowhead=1,
        row=rows[0],
        col=cols[0],
    )
    fig.add_annotation(
        x=x2,
        y=y,
        text=f"{name}, {state}",
        showarrow=True,
        arrowsize=1,
        xanchor=xachors[1],
        ax=axs[1],
        ay=ays[1],
        arrowhead=1,
        row=rows[1],
        col=cols[1],
    )
    return fig


if __name__ == "__main__":
    start_time = time.time()

    # Determine the states to highlight
    states: List[str] = ["OH", "CA"]

    # Read in the data
    plot_df = pd.read_csv(f"{data_folder}/fig5_data.csv")

    region_list = ["Northeast", "Midwest", "South", "West"]
    fig = go.Figure(
        layout=dict(
            template="ggplot2",
            margin=dict(l=0, r=0, b=0, t=20, pad=0),
            font=dict(family="Latin Modern Math", size=11, color="black"),
        )
    ).set_subplots(
        rows=2,
        cols=4,
        shared_xaxes=False,
        shared_yaxes=False,
        horizontal_spacing=0.05,
        vertical_spacing=0.2,
        row_heights=[0.7, 0.3],
        subplot_titles=[
            f"a) {region_list[0]}",
            f"b) {region_list[1]}",
            f"c) {region_list[2]}",
            f"d) {region_list[3]}",
            "e) Counties in OH &amp; CA",
            "f) Counties in OH &amp; CA",
        ],
        specs=[[{}, {}, {}, {}], [{"colspan": 2}, None, {"colspan": 2}, None]],
    )
    fig.update_annotations(font=dict(family="Latin Modern Math", size=12))

    for region, col in zip(region_list, [1, 2, 3, 4]):
        temp = plot_df[plot_df["region"] == region]
        temp_sorted = (
            temp.groupby("state")
            .agg({"hesitant": "median", "fips": "count"})
            .rename(columns={"fips": "num_counties"})
            .sort_values("hesitant", ascending=True)
            .reset_index()
        )
        for state in temp_sorted["state"].unique():
            temp_state = temp[temp["state"] == state]
            if state == states[0]:
                color, opacity = "#1F77B4", 1
            elif state == states[1]:
                color, opacity = "crimson", 1
            else:
                color, opacity = "black", 0.7
            fig.add_trace(
                go.Violin(
                    x=temp_state["hesitant"],
                    line=dict(width=1, color=color),
                    opacity=opacity,
                    name=state,
                    showlegend=False,
                ),
                row=1,
                col=col,
            )
    fig.update_traces(orientation="h", side="positive", width=1.8, points=False)

    for state, color, symbol in zip(states, ["#1F77B4", "crimson"], ["circle", "diamond"]):
        temp_df = plot_df[plot_df["state"] == state]
        fig.add_trace(
            go.Scatter(
                x=temp_df["hesitant"],
                y=temp_df["VHb"],
                mode="markers",
                marker=dict(
                    size=6,
                    color=color,
                    symbol=symbol,
                    opacity=0.7,
                    line=dict(width=0.5, color="black"),
                ),
                name=f"{state}",
                showlegend=True,
            ),
            row=2,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=temp_df["PFV"],
                y=temp_df["VHb"],
                mode="markers",
                marker=dict(
                    size=6,
                    color=color,
                    symbol=symbol,
                    opacity=0.7,
                    line=dict(width=0.5, color="black"),
                ),
                name=state,
                showlegend=False,
            ),
            row=2,
            col=3,
        )

    fig.update_layout(
        height=400,
        width=800,
        xaxis=dict(title="ASPE VH Estimate", title_standoff=5, title_font_size=12, range=[0, 0.3]),
        xaxis2=dict(title="ASPE VH Estimate", title_standoff=5, title_font_size=12, range=[0, 0.3]),
        xaxis3=dict(title="ASPE VH Estimate", title_standoff=5, title_font_size=12, range=[0, 0.3]),
        xaxis4=dict(title="ASPE VH Estimate", title_standoff=5, title_font_size=12, range=[0, 0.3]),
        xaxis5=dict(title="ASPE VH Estimate", title_standoff=5, title_font_size=12),
        xaxis6=dict(title="% of Residents Fully Vaccinated", title_standoff=5, title_font_size=12),
        yaxis=dict(
            title="State",
            showgrid=True,
            zeroline=False,
            ticksuffix=" ",
            tickfont_size=10,
            title_font_size=13,
            dtick=1,
        ),
        yaxis2=dict(showgrid=True, zeroline=False, ticksuffix=" ", tickfont_size=10, dtick=1),
        yaxis3=dict(showgrid=True, zeroline=False, ticksuffix=" ", tickfont_size=10, dtick=1),
        yaxis4=dict(showgrid=True, zeroline=False, ticksuffix=" ", tickfont_size=10, dtick=1),
        yaxis5=dict(title="VH<i><sup>b</sup></i> (week 23)", tickfont_size=10),
        yaxis6=dict(title="", showticklabels=False, ticks="", tickfont_size=1),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=0.01,
            xanchor="left",
            x=0.302,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
        ),
    )

    plot_1_df = plot_df[plot_df["state"] == states[0]]
    plot_2_df = plot_df[plot_df["state"] == states[1]]
    county_min = plot_2_df[plot_2_df["VHb"] == plot_2_df["VHb"].min()]
    county_max = plot_1_df[plot_1_df["VHb"] == plot_1_df["VHb"].max()]
    fig = plot_county_annotation(
        fig=fig,
        df=county_max,
        rows=[2, 2],
        cols=[1, 3],
        axs=[-20, 20],
        ays=[-15, -15],
        xachors=["right", "left"],
    )
    fig = plot_county_annotation(
        fig=fig,
        df=county_min,
        rows=[2, 2],
        cols=[1, 3],
        axs=[20, -20],
        ays=[15, 15],
        xachors=["left", "right"],
    )

    # Export the figure
    fig.write_image(f"{image_folder}/(fig5)hesitant_state.png", scale=4)
    print(f"--- Finished exporting figure  5, took {time.time() - start_time:,.2f} seconds ---")
