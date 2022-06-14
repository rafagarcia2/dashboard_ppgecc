import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from config_colors import colors


def plot_timeSeries_scopus(areas):
    data = pd.read_csv("data/scopus_professors.csv")
    df = pd.DataFrame(data.loc[df["subject_areas"].isin(areas), :])
    df = data.loc[
        :, ["subject_areas", "year", "title"]  # "professors", "citation_num", "title",
    ]
    df = pd.get_dummies(data=df, columns=["subject_areas"], prefix="", prefix_sep="")
    # df["subject_areas"] = data["subject_areas"]
    df = df.groupby(
        by=["title", "year"], as_index=False  # "professors", "title", "subject_areas",
    ).sum()
    citations = data.loc[:, ["title", "citation_num"]]
    citations = citations.drop_duplicates()
    df = df.merge(citations, on="title", how="left")
    df = df.groupby(
        by=["year"], as_index=False  # "professors", "title", "subject_areas",
    ).sum()

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=[
            "subjects on time",
            "citations on time",
        ],
    )

    # df["year"] = df["year"].astype(int)
    df = df.sort_values(by="year", ascending=True).reset_index()
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["Electrical and Electronic Engineering"],
            mode="lines+markers",
            line=dict(color="rgba(68,53,118,0.5)", width=1),
            name="Electrical and Electronic Engineering",
        ),
        1,
        1,
    )
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["Instrumentation"],
            mode="lines+markers",
            line=dict(color="rgba(35,172,134,0.5)", width=1),
            name="Instrumentation",
        ),
        1,
        1,
    )
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["Engineering (all)"],
            mode="lines+markers",
            line=dict(color="rgba(149,224,42,0.5)", width=1),
            name="Engineering (all)",
        ),
        1,
        1,
    )

    df1 = df.loc[df["Electrical and Electronic Engineering"] > 0, :]
    fig.add_trace(
        go.Bar(
            x=df["year"],
            y=df1["citation_num"],
            name="Electrical and Electronic Engineering",
            marker=dict(color="rgba(214,238,193,0.5)"),
        ),
        2,
        1,
    )

    df2 = df.loc[df["Instrumentation"] > 0, :]

    fig.add_trace(
        go.Bar(
            x=df["year"],
            y=df2["citation_num"],
            name="Instrumentation",
            marker=dict(color="rgba(141,15,162,0.5)"),
        ),
        2,
        1,
    )

    df3 = df.loc[df["Engineering (all)"] > 0, :]
    fig.add_trace(
        go.Bar(
            x=df["year"],
            y=df3["citation_num"],
            name="Engineering (all)",
            marker=dict(color="rgba(7,152,228,0.5)"),
        ),
        2,
        1,
    )

    fig.update_layout(
        showlegend=True,
        hovermode="x unified",
        xaxis_showticklabels=True,
        xaxis2_showticklabels=True,
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=False,
        width=1200,
        height=900,
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            showgrid=True,
            autorange=True,
            showline=True,
            linewidth=1,
            linecolor="black",
            gridcolor="gray",
            type="linear",
        ),
        yaxis=dict(showline=True, linewidth=1, linecolor="black", gridcolor="gray"),
        xaxis2=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            showgrid=True,
            autorange=True,
            showline=True,
            linewidth=1,
            linecolor="black",
            gridcolor="gray",
            rangeslider=dict(
                autorange=True,
            ),
            type="linear",
        ),
        yaxis2=dict(
            showline=True,
            linewidth=1,
            linecolor="black",
            autorange=True,
            gridcolor="gray",
        ),
    )
    return fig


def plot_timeSeries_scival():
    data = pd.read_csv("scival_asjc_norm.csv")
    df = data.loc[
        :,
        [
            "All Science Journal Classification (ASJC) field name",
            "Year",
            "Title",
        ],  # "professors", "citation_num", "title",
    ]
    df = pd.get_dummies(
        data=df,
        columns=["All Science Journal Classification (ASJC) field name"],
        prefix="",
        prefix_sep="",
    )
    # df["All Science Journal Classification (ASJC) field name"] = data["All Science Journal Classification (ASJC) field name"]
    df = df.groupby(
        by=["Title", "Year"], as_index=False  # "professors", "title", "subject_areas",
    ).sum()
    citations = data.loc[:, ["Title", "Citations"]]
    citations = citations.drop_duplicates()
    df = df.merge(citations, on="Title", how="left")
    df = df.groupby(
        by=["Year"], as_index=False  # "professors", "title", "subject_areas",
    ).sum()

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=[
            "subjects on time",
            "citations on time",
        ],
    )

    # df["year"] = df["year"].astype(int)
    df = df.sort_values(by="Year", ascending=True).reset_index()
    fig.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df[" Aerospace Engineering"],
            mode="lines+markers",
            line=dict(color="rgba(68,53,118,0.5)", width=1),
            name="Aerospace Engineering",
        ),
        1,
        1,
    )
    fig.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df[" Electronic, Optical and Magnetic Materials"],
            mode="lines+markers",
            line=dict(color="rgba(35,172,134,0.5)", width=1),
            name="Electronic, Optical and Magnetic Materials",
        ),
        1,
        1,
    )
    fig.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["Health, Toxicology and Mutagenesis"],
            mode="lines+markers",
            line=dict(color="rgba(149,224,42,0.5)", width=1),
            name="Health, Toxicology and Mutagenesis",
        ),
        1,
        1,
    )

    df1 = df.loc[df[" Aerospace Engineering"] > 0, :]
    fig.add_trace(
        go.Bar(
            x=df["Year"],
            y=df1["Citations"],
            name="Aerospace Engineering",
            marker=dict(color="rgba(214,238,193,0.5)"),
        ),
        2,
        1,
    )

    df2 = df.loc[df[" Electronic, Optical and Magnetic Materials"] > 0, :]

    fig.add_trace(
        go.Bar(
            x=df["Year"],
            y=df2["Citations"],
            name="Electronic, Optical and Magnetic Materials",
            marker=dict(color="rgba(141,15,162,0.5)"),
        ),
        2,
        1,
    )

    df3 = df.loc[df["Health, Toxicology and Mutagenesis"] > 0, :]
    fig.add_trace(
        go.Bar(
            x=df["Year"],
            y=df3["Citations"],
            name="Health, Toxicology and Mutagenesis",
            marker=dict(color="rgba(7,152,228,0.5)"),
        ),
        2,
        1,
    )

    fig.update_layout(
        showlegend=True,
        hovermode="x unified",
        xaxis_showticklabels=True,
        xaxis2_showticklabels=True,
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=False,
        width=1200,
        height=900,
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            showgrid=True,
            autorange=True,
            showline=True,
            linewidth=1,
            linecolor="black",
            gridcolor="gray",
            type="linear",
        ),
        yaxis=dict(showline=True, linewidth=1, linecolor="black", gridcolor="gray"),
        xaxis2=dict(
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            showgrid=True,
            autorange=True,
            showline=True,
            linewidth=1,
            linecolor="black",
            gridcolor="gray",
            rangeslider=dict(
                autorange=True,
            ),
            type="linear",
        ),
        yaxis2=dict(
            showline=True,
            linewidth=1,
            linecolor="black",
            autorange=True,
            gridcolor="gray",
        ),
    )
    fig.show()
