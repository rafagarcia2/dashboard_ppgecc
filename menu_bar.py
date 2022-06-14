import streamlit as st


def menu():

    st.sidebar.markdown(
        "<h1 style='text-align: center; color: #2F1EFF;font-size: 14 px ;font-family: Times;'> PPGEEC Analitycs</h1>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        "<h2 style='text-align: center; color: #0F0F0F;font-size: 12 px ;font-family: Times'> Menu</h2>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")
    st.sidebar.button(label="Home")
    st.sidebar.button(label="Clustering")
    st.sidebar.button(label="Net analisys")
    st.sidebar.button(label="Time analysis")
