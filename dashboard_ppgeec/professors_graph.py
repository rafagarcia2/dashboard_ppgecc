from numpy import greater
import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.graph_objects import scatterpolargl

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
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "dashboard_ppgeec/credentials/spheric-algebra-344319-2ca8235bd861.json"
    papers = bigquery_select.select_table_from_bigquery(
        project_name="spheric-algebra-344319",
        database_name="ppgeec_datalake",
        table_name="papers_scopus",
    )
    # pd.read_csv(
    #     "/mnt/c/Users/diego/Desktop/TCC/dashboard_ppgecc/data/scopus_professors.csv"
    # )
    data = bigquery_select.select_table_from_bigquery(
        project_name="spheric-algebra-344319",
        database_name="ppgeec_datalake",
        table_name="scopus_professors",
    )
    # pd.read_csv(
    #     "/mnt/c/Users/diego/Desktop/TCC/dashboard_ppgecc/data/papers_scopus.csv"
    # )
    return data, papers


# set the page layout to full screen
st.set_page_config(
    layout="wide",
)


if check_password():
    # print(st.session_state)
    data, papers = loading_data()
    menu()
    if st.session_state.page == "home":
        show_principal(data=papers)
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

        df4 = data.copy()
        prof = st.multiselect(
            label="Professor a visualizar:", options=df4["professors"].unique()
        )
        if len(prof) > 0:
            try:
                fig = cluster_view.cluster_plot(data=df4, prof=prof)
                st.plotly_chart(fig)
            except:
                st.warning("Gráfico inválido")
