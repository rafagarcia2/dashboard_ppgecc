from cProfile import label
from turtle import title
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


def mostra_qntd_linhas(dataframe: pd.DataFrame):
    """Função para mostrar a quantidade de linhas de um DataFrame.

    Args:
        dataframe (pd.DataFrame): dataframe com dados para visualizar.
    """

    st.markdown("## Filtro para a tabela")
    max_linhas = min(100, len(dataframe))
    qntd_linhas = st.slider(
        "Selecione a quantidade de linhas que deseja mostrar na tabela",
        min_value=10,
        max_value=max_linhas,
        step=10,
    )

    df_show = dataframe[["id", "title", "publication_date"]].reset_index(drop=["index"])
    st.write(df_show.head(qntd_linhas))


def plot_artichles_per_year(dataframe, year=None):
    """Responsável por apresentar o gráfico de artigos por ano.

    Args:
        dataframe (_type_): DataFrame com os dados.
        year (_type_, optional): O ano que deseja apresentar os dados.
            Defaults to None.

    Returns:
        _type_: graph.
    """

    if year is not None:
        dataframe = dataframe.query("publication_year == @year")
    fig = px.histogram(
        dataframe,
        x="publication_date",
        title="Quantidade de Artigos por Ano",
        labels={"x": "Ano", "y": "Quantidade"},
    )

    fig.update_layout(
        showlegend=True,
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=False,
        bargap=0.2,
        width=1200,
        height=500,
    )
    return fig


# articles per conference
def plot_articles_per_subject(dataframe):

    dados_plot = dataframe.subject_areas.values
    df6 = pd.get_dummies(data=dados_plot, columns=["subject_areas"], prefix="", prefix_sep="")
    df6["subject_areas"] = data["subject_areas"]
    dados_plot
    fig = px.bar(
        dados_plot,
        x="index",
        y="subject_areas",
        title="Quantidade em artigos por Assunto",
        labels={"x": "conferência", "y": "Quantidade de artigos"},
        color="index",
    )

    fig.update_layout(
        showlegend=True,
        hovermode="x unified",
        xaxis_showticklabels=True,
        plot_bgcolor="rgba(0,0,0,0)",
        autosize=False,
        width=1200,
        height=500,
    )
    return fig


def show_professors_page(data):
    # importando os dados
    df_papers = data
    st.markdown(
        "<h1 style='text-align: center; color: #0F2D9F;font-size: 14 px ;'>Análise da Produção Acadêmica do PPgEEC</h1>",
        unsafe_allow_html=True,
    )

    st.write(
        " Esta página dá um breve overview sobre as produções acadêmicas de forma iterativa com relação ao"
        + " ano dos papers, a presença dos trabalhos em congressos no Brasil e no restante do mundo."
    )

    # get unique values
    df_unique_papers = df_papers.drop_duplicates(["id"])

    # Articles per year
    df_unique_papers.publication_date = pd.to_datetime(
        df_unique_papers.publication_date
    )

    df_unique_papers["publication_year"] = df_unique_papers.publication_date.dt.year

    years = list(df_unique_papers["publication_year"].unique())
    years.insert(0, "Todos")

    professors = list(df_unique_papers["professors"].unique())
    professors.insert(0, "Todos")

    year = st.selectbox("Selecione um ano para visualizar", options=years)
    professor = st.selectbox("Selecione um professor", options=professors)

    if year != "Todos":
        df_unique_papers = df_unique_papers.query("publication_year == @year")
    if professor != "Todos":
        df_unique_papers = df_unique_papers.query("professors == @professor")

    # indicators
    number_articles = df_unique_papers.id.nunique()
    number_authors = df_unique_papers.professors.nunique()
    number_citations = int(df_unique_papers.citation_num.sum())
    number_publications = df_unique_papers[~df_unique_papers.publisher.isna()].shape[0]

    col1, col2, col3, col4 = st.columns(4)
    # show indicators
    with col1:
        st.metric(label="Artigos", value=number_articles)
    with col2:
        st.metric(label="Professores", value=number_authors)
    with col3:
        st.metric(label="Publicações", value=number_publications)
    with col4:
        st.metric(label="Citações", value=number_citations)

    figura = plot_articles_per_subject(df_unique_papers)
    st.plotly_chart(figura)

    figura_articles = plot_artichles_per_year(df_unique_papers)
    st.plotly_chart(figura_articles)
    mostra_qntd_linhas(df_unique_papers)
