import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# função para selecionar a quantidade de linhas do dataframe
def mostra_qntd_linhas(dataframe):

    qntd_linhas = st.sidebar.slider('Selecione a quantidade de linhas que deseja mostrar na tabela', min_value = 1, max_value = len(dataframe), step = 1)

    st.write(dataframe.head(qntd_linhas).style.format(subset = ['Valor'], formatter="{:.2f}"))

# função que cria o gráfico
def plot_artichles_per_year(dataframe, year=None):

    if year is not None:
        dataframe = dataframe.query('publication_year == @year')

    fig, ax = plt.subplots(figsize=(8,6))
    ax = sns.histplot(data = dataframe, x = 'publication_year')
    ax.set_title(f'Quantidade de Artigos por Ano', fontsize = 16)
    ax.set_xlabel('Ano', fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel('Quantidade', fontsize = 12)
  
    return fig

## articles per conference
def plot_articles_per_conference(dataframe):

    dados_plot = dataframe.publisher.value_counts().head(15).reset_index()

    fig, ax = plt.subplots(figsize=(8,6))
    ax = sns.barplot(x = 'index', y = 'publisher', data = dados_plot)
    ax.set_title(f'Quantidade em artigos por conferência', fontsize = 16)
    ax.set_xlabel('Produtos', fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel('Quantidade', fontsize = 12)
  
    return fig

# importando os dados
df_papers = pd.read_csv('data/papers_scopus.csv')

st.title('Análise da Produção Acadêmica do PPgEEC\n')
st.write('Iremos desenvolver uma plataforma capaz de visualizar os dados de produção acadêmica desenvolvida pelo Programa de Pós-graduação em Engenharia Elétrica (PPgECC).')

# indicators
number_articles = df_papers.id.nunique()
number_authors = df_papers.professors.nunique()

# get unique values
df_unique_papers = df_papers.drop_duplicates(["id"])

number_citations = df_unique_papers.citation_num.sum()
number_publications = df_unique_papers[~df_unique_papers.publisher.isna()].shape[0]

# show indicators
st.metric(label="Artigos", value=number_articles)
st.metric(label="Professores", value=number_authors)
st.metric(label="Publicações", value=number_publications)
st.metric(label="Citações", value=number_citations)

# Articles per year
df_unique_papers.publication_date = pd.to_datetime(df_unique_papers.publication_date)
df_unique_papers["publication_year"] = df_unique_papers.publication_date.dt.year

figura = plot_articles_per_conference(df_unique_papers)
st.pyplot(figura)

# filtros para a tabela
checkbox_mostrar_tabela = st.sidebar.checkbox('Mostrar tabela')

if checkbox_mostrar_tabela:

    st.sidebar.markdown('## Filtro para a tabela')

    # figura_articles = plot_artichles_per_year(df_unique_papers)
    # st.pyplot(figura_articles)

    years = list(df_unique_papers['publication_year'].unique())
    years.insert(0, 'Todos')

    year = st.sidebar.selectbox('Selecione um ano para visualizar', options = years)

    if year != 'Todos':
        df_year = df_unique_papers.query('publication_year == @year')
        figura_articles = plot_artichles_per_year(df_year)
    else:
        figura_articles = plot_artichles_per_year(df_unique_papers)
    st.pyplot(figura_articles)

# filtro para o gráfico
# st.sidebar.markdown('## Filtro para o gráfico')

# categoria_grafico = st.sidebar.selectbox('Selecione a categoria para apresentar no gráfico', options = df['Categoria'].unique())
# figura = plot_estoque(df, categoria_grafico)
# st.pyplot(figura)