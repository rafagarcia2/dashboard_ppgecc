from numpy import greater
import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.graph_objects import scatterpolargl
from utils.professors import show_professors_page

from datalake_utils import bigquery_select
from utils.app import show_principal
import utils.cluster_view as cluster_view
from utils.config_colors import colors
import utils.graph_view as graph_view
from utils.login_template import check_password
from utils.menu_bar import menu
import utils.timeSeries_view as timeSeries_view


@st.cache(suppress_st_warning=True)
def loading_data():
    # os.environ[
    #     "GOOGLE_APPLICATION_CREDENTIALS"
    # ] = "dashboard_ppgeec/credentials/spheric-algebra-344319-2ca8235bd861.json"
    # papers = bigquery_select.select_table_from_bigquery(
    #     project_name="spheric-algebra-344319",
    #     database_name="ppgeec_datalake",
    #     table_name="papers_scopus",
    # )
    data = pd.read_csv(
        "dashboard_ppgeec/data/scopus_professors.csv"
    )
    # data = bigquery_select.select_table_from_bigquery(
    #     project_name="spheric-algebra-344319",
    #     database_name="ppgeec_datalake",
    #     table_name="scopus_professors",
    # )
    papers = pd.read_csv(
        "dashboard_ppgeec/data/papers_scopus.csv"
    )
    return data, papers


# set the page layout to full screen
st.set_page_config(
    layout="wide",
)

data, papers = loading_data()
menu()
print(st.session_state)
print(type(st.session_state))
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state.page == "home":
    print(type(st.session_state))
    show_principal(data=papers)
if st.session_state.page == "professors":
    show_professors_page(data=papers)
if st.session_state.page == "graph":
    prof = graph_view.plot_graph(data=data)
if st.session_state.page == "time":
    try:
        fig = timeSeries_view.plot_timeSeries_scopus(data=data)
        st.plotly_chart(fig)
    except:
        st.warning("Gráfico inválido")
if st.session_state.page == "cluster":
    st.markdown(
        "<h1 style='text-align: center; color: #0F2D9F;font-size: 14 px ;'> Bem vindo à sessão de visualização em cluster </h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style='color: #000000;font-size: 12 px ;'>  Nesta sessão o foco é a visualização clusterizada da produção cientifica dos professores 
            o usuario pode selecionar o discente do PPgEEC cujos dados deseja visualizar de maneira clusterizada.
            O posição da esfera que estamos visualizando é dada em coordenadas polares, o raio significa o ano em 
            que houveram trabalho com aquele assunto foi feita, enquanto que o ângulo indica o assunto abordado no trabalho. 
            Já o tamanho da esfera é referente à quantidade de citações que os trabalhos sobre daquele assunto receberam.
            Logo, a visualização tem por intuíto mostrar como os assuntos abordados foram relevantes com o decorrer dos anos,
            usando como parâmetro de medição o número de citações que os trabalhos daquele assunto tiveram com o decorrer dos anos.
            </p>""",
        unsafe_allow_html=True,
    )
    data = data.loc[data["year"] != "['2013', '11', '18']", :]
    df4 = data.copy()
    agree = st.checkbox("Customizar por professor")

    if agree:
        prof = st.multiselect(
            label="Professor a visualizar:", options=df4["professors"].unique()
        )
    else:
        prof = df4["professors"].unique()

    options_time = df4["year"].sort_values().unique()
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
        df4 = df4.loc[
            (df4["year"].astype(int) >= int(option1))
            & (df4["year"].astype(int) <= int(option2)),
            :,  # "professors", "citation_num", "title",
        ]
        if len(prof) > 0:
            try:
                fig = cluster_view.cluster_plot(data=df4, prof=prof)
                st.plotly_chart(fig)
            except:
                st.warning("Gráfico inválido")
