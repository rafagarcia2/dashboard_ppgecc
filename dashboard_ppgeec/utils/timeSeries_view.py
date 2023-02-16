import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from utils.config_colors import colors
import streamlit as st


def plot_timeSeries_scopus(data: pd.DataFrame, areas=None):
    data = data.loc[data["year"] != "['2013', '11', '18']", :]
    st.markdown(
        "<h1 style='text-align: center; color: #0F2D9F;font-size: 14 px ;'> Bem vindo à sessão de Séries temporais </h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h2 style='text-align: center; color: #000000;font-size: 12 px ;'> Selecione as informações que deseja visualizar </h2>",
        unsafe_allow_html=True,
    )
    options = ["Professores", "Temas"]
    viz_type = st.selectbox(
        "Selecione o campo que se deseja visualizar", options=options
    )
    fields = {
        "Professores": "professors",
        "Papers": "title",
        "Temas": "subject_areas",
        "Conferencia": "conference_name",
    }
    field1 = fields[viz_type]
    df = data.loc[
        :, [str(field1), "year", "title"]  # "professors", "citation_num", "title",
    ]
    df = df.sort_values(by="year", ascending=True).reset_index()
    options_time = df["year"].unique()
    col1, col2 = st.columns(2)
    with col1:
        option1 = st.selectbox("Ano de inicio", options=options_time)
    with col2:
        option2 = st.selectbox("Ano final", options=options_time)
    if int(option1) > int(option2):
        st.warning(
            "Mantenha o valor final maior que o inicial, ou igual quando valor único."
        )
    else:
        df = df.loc[
            (df["year"].astype(int) >= int(option1))
            & (df["year"].astype(int) <= int(option2)),
            :,  # "professors", "citation_num", "title",
        ]
        df = df.sort_values(by="year", ascending=True).reset_index()
        df = pd.get_dummies(data=df, columns=[str(field1)], prefix="", prefix_sep="")
        # df["subject_areas"] = data["subject_areas"]
        df = df.groupby(
            by=["title", "year"],
            as_index=False,  # "professors", "title", "subject_areas",
        ).sum()
        citations = data.loc[:, [str(field1), "title", "citation_num"]]
        citations = citations.drop_duplicates()
        df = df.merge(citations, on="title", how="left")
        df = df.groupby(
            by=[str(field1), "year"],
            as_index=False,  # "professors", "title", "subject_areas",
        ).count()

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            subplot_titles=[
                field1 + " ao longo dos anos",
                "citações ao longo dos anos",
            ],
        )
        prof = st.multiselect(
            label=str(option1) + " a visualizar:",
            options=data[field1].dropna().unique(),
        )
        color_number = 0
        for i in prof:
            df2 = df.loc[df[field1] == i, :]
            try:
                fig.add_trace(
                    go.Scatter(
                        x=df2["year"],
                        y=df2[i],
                        mode="lines+markers",
                        line=dict(color=colors[color_number], width=1),
                        name=i,
                    ),
                    1,
                    1,
                )
                df1 = df2.loc[df[i] > 0, :]
                fig.add_trace(
                    go.Bar(
                        x=df1["year"],
                        y=df1["citation_num"],
                        name=i,
                        marker=dict(color=colors[color_number]),
                    ),
                    2,
                    1,
                )
                del df1
                del df2
                color_number = color_number + 1
            except:
                st.warning("Intervalo de anos inválido para as opções escolhidas")
        fig.update_layout(
            showlegend=True,
            hovermode="x unified",
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=False,
            width=1400,
            height=800,
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


def plot_timeSeries_scival(data):
    data = data
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
