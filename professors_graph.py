from numpy import greater
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.graph_objects import scatterpolargl
from config_colors import colors
from login_template import check_password
import graph_view
import cluster_view

# set the page layout to full screen
st.set_page_config(
    layout="wide",
)

if check_password():

    prof = graph_view.plot_graph()

    if len(prof) > 0:
        fig = cluster_view.cluster_plot(prof)
        st.plotly_chart(fig)
