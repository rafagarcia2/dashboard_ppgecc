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


## articles per conference
def plot_articles_per_conference(dataframe):

    dados_plot = dataframe.publisher.value_counts().head(15).reset_index()
    #    print(dados_plot.columns)
    fig = px.bar(
        dados_plot,
        x="index",
        y="publisher",
        title="Quantidade em artigos por conferência",
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


def show_principal(data):
    # importando os dados
    df_papers = data
    st.markdown(
        "<h1 style='text-align: center; color: #0F2D9F;font-size: 14 px ;'>Análise da Produção Acadêmica do PPgEEC</h1>",
        unsafe_allow_html=True,
    )

    st.write(
        "Esta plataforma tem por objetivo principal, permitir a visualização dos dados de produção "
        + "acadêmica desenvolvida pelo Programa de Pós-graduação em Engenharia Elétrica (PPgECC)."
        + "Permintindo que o usuário retire insights de como as produções acadêmicas tem ocorrido "
        + " na UFRN, de acordo com os dados de plataformas de produção ciêntifica como scopus e scival."
        + "Além do overview de quantidades de papers publicados, é possível ver como os assuntos de projetos foram "
        + "evoluindo com o decorrer do tempo, e dessa forma analisar como os artigos estão se adaptando ao mercado "
        + "de trabalho, como os assuntos estão evoluindo em concordância com a sociedade científica e onde a produção "
        + "dos papers se encaixa dentro dos objetivos de desenvolvimento sustentável(ods) propostos pela academia."
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

    year = st.selectbox("Selecione um ano para visualizar", options=years)

    if year != "Todos":
        df_unique_papers = df_unique_papers.query("publication_year == @year")

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

    figura = plot_articles_per_conference(df_unique_papers)
    st.plotly_chart(figura)

    figura_articles = plot_artichles_per_year(df_unique_papers)
    st.plotly_chart(figura_articles)
    mostra_qntd_linhas(df_unique_papers)
