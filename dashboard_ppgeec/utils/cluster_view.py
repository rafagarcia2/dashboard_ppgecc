import pandas as pd
import plotly.graph_objects as go
from utils.config_colors import colors
import streamlit as st


def cluster_plot(data, prof):

    df6 = data.loc[:, ["subject_areas", "professors", "citation_num", "title", "year"]]
    df6 = pd.get_dummies(data=df6, columns=["subject_areas"], prefix="", prefix_sep="")
    df6["subject_areas"] = data["subject_areas"]
    df6 = df6.groupby(
        by=["professors", "title", "subject_areas", "year"], as_index=False
    ).sum()
    # create the graph
    df7 = df6.loc[df6["professors"].isin(prof), :]
    df7["year"] = df7["year"].astype(int)
    df7 = df7.sort_values(by="year", ascending=True).reset_index()
    fig = go.Figure()
    color_number = 0
    for sub in df7["subject_areas"].unique():
        local_df = df7.loc[df7[sub] > 0, :]
        local_df["year"] = local_df["year"].astype(str)
        print(sub)
        fig.add_trace(
            go.Scatterpolargl(
                r=local_df["year"].sort_values(),
                theta=local_df["subject_areas"],
                marker=dict(size=local_df["citation_num"], color=colors[color_number]),
            )
        )
        color_number = color_number + 1

    fig.update_traces(mode="markers", marker=dict(line_color="white", opacity=0.7))
    fig.update_layout(
        title="cluster papers",
        font_size=15,
        showlegend=False,
        width=1350,
        height=800,
        paper_bgcolor="#E2E3E4",
        polar1=dict(
            bgcolor="rgb(255, 255, 255)",
            angularaxis=dict(
                linewidth=3,
                showline=True,
                showgrid=False,
                # linecolor='rgb(230, 23, 25)'
            ),
            radialaxis=dict(
                side="counterclockwise",
                showline=False,
                linewidth=2,
                showgrid=False,
                gridcolor="white",
                gridwidth=2,
                # linecolor='rgb(0, 23, 205)',
            ),
        ),
        # paper_bgcolor="rgb(250, 250, 250)",
    )

    return fig
