import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def mostra_qntd_linhas(dataframe: pd.DataFrame):
    """Função para mostrar a quantidade de linhas de um DataFrame.

    Args:
        dataframe (pd.DataFrame): dataframe com dados para visualizar.
    """

    max_linhas = min(100, len(dataframe))
    qntd_linhas = st.sidebar.slider(
        "Selecione a quantidade de linhas que deseja mostrar na tabela",
        min_value=10,
        max_value=max_linhas,
        step=10,
    )

    df_show = dataframe[["id", "title", "publication_date"]]
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

    fig, ax = plt.subplots(figsize=(8, 6))
    ax = sns.histplot(data=dataframe, x="publication_year")
    ax.set_title(f"Quantidade de Artigos por Ano", fontsize=16)
    ax.set_xlabel("Ano", fontsize=12)
    ax.tick_params(rotation=20, axis="x")
    ax.set_ylabel("Quantidade", fontsize=12)

    return fig


## articles per conference
def plot_articles_per_conference(dataframe):

    dados_plot = dataframe.publisher.value_counts().head(15).reset_index()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax = sns.barplot(x="index", y="publisher", data=dados_plot)
    ax.set_title(f"Quantidade em artigos por conferência", fontsize=16)
    ax.set_xlabel("Produtos", fontsize=12)
    ax.tick_params(rotation=20, axis="x")
    ax.set_ylabel("Quantidade", fontsize=12)

    return fig


# importando os dados
df_papers = pd.read_csv("data/papers_scopus.csv")

st.title("Análise da Produção Acadêmica do PPgEEC\n")
st.write(
    "Iremos desenvolver uma plataforma capaz de visualizar os dados de produção " +
    "acadêmica desenvolvida pelo Programa de Pós-graduação em Engenharia Elétrica (PPgECC)."
)

# indicators
number_articles = df_papers.id.nunique()
number_authors = df_papers.professors.nunique()

# get unique values
df_unique_papers = df_papers.drop_duplicates(["id"])

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

# Articles per year
df_unique_papers.publication_date = pd.to_datetime(df_unique_papers.publication_date)
df_unique_papers["publication_year"] = df_unique_papers.publication_date.dt.year

figura = plot_articles_per_conference(df_unique_papers)
st.pyplot(figura)

st.sidebar.markdown("## Filtro para a tabela")

years = list(df_unique_papers["publication_year"].unique())
years.insert(0, "Todos")

year = st.sidebar.selectbox("Selecione um ano para visualizar", options=years)

if year != "Todos":
    df_year = df_unique_papers.query("publication_year == @year")
    figura_articles = plot_artichles_per_year(df_year)
    st.pyplot(figura_articles)
    mostra_qntd_linhas(df_year)
else:
    figura_articles = plot_artichles_per_year(df_unique_papers)
    st.pyplot(figura_articles)
    mostra_qntd_linhas(df_unique_papers)
