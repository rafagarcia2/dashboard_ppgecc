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
    if st.sidebar.button(label="Home", key="home"):
        set_page("home")
    if st.sidebar.button(label="Clustering", key="cluster"):
        set_page("cluster")
    if st.sidebar.button(label="Net analisys", key="graph"):
        set_page("graph")
    if st.sidebar.button(label="Time analysis", key="time"):
        set_page("time")


def set_page(page):
    print(page)
    st.session_state["page"] = page
