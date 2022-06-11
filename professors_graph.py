from turtle import bgcolor, color
import pandas as pd
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import plotly.graph_objects as go
from plotly.graph_objects import scatterpolargl
from config_colors import colors

# set the page layout to full screen
st.set_page_config(
    layout="wide",
)


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (st.session_state["username"] in st.secrets["passwords"]) and (
            st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            # del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        st.error("User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():

    df = pd.read_csv("data/graph_csv.csv")
    st.markdown(
        "<h1 style='text-align: center; color: #0F2D9A;font-size: 14 px ;'> Bem vindo à sessão de grafos e agrupamentos </h1>",
        unsafe_allow_html=True,
    )
    nodes = []
    edges = []
    # multiselect the professors in the list
    prof = st.multiselect(label="Professor a visualizar:", options=df["professors"])
    # filter the data by the professors selected
    df = pd.DataFrame(df.loc[df["professors"].isin(prof), :])

    # create the professor's nodes
    for i in prof:
        # set the node size by row sum without professors columns
        size = df.loc[df.professors == i, :].drop(columns="professors").iloc[0].sum()
        # use the professor name as node's id
        id = str(i)
        # append the node in the node's list
        nodes.append(Node(id=id, label=id, size=int(size), color="#222177"))

    # create the theme's nodes
    for i in df.drop(columns="professors").columns:
        # create the size by column's sum
        size = int(df[i].sum())
        # create the node if it has connections in the table
        if size > 0:
            # node id == theme's name
            nodes.append(Node(id=i, label=i, size=size, color="#4F62EE"))

    # link the nodes using the id's
    for i in prof:
        # filter the data without
        data = df.loc[df.professors == i, :].drop(columns=["professors"]).iloc[0]
        # set the source node name as the professor's node id
        source = i
        for j in data.keys():
            # checks if the columns has some value higher than 0
            if int(data[j]) > 0:
                # creates the edge relating the professor's node to the theme's nodes
                edges.append(
                    Edge(
                        source=str(source),
                        target=str(j),
                        width=data[j],
                        color="#CAD8F6",
                        type="CURVE_SMOOTH",  # type="STRAIGHT"
                    )
                )

    # set the graphs view config to the agraph component
    config = Config(
        width=1400,
        height=400,
        directed=False,
        onclick="focus",
        nodeHighlightBehavior=False,
        highlightColor="#F31234",  # or "blue"
        collapsible=True,
        node={"labelProperty": "label"},
        link={"labelProperty": "label", "renderLabel": True},
        graphviz_layout=None
        # **kwargs e.g. node_size=1000 or node_color="blue"
    )
    return_value = agraph(nodes=nodes, edges=edges, config=config)

    if len(prof) > 0:
        df4 = pd.read_csv("data/papers_scopus_subject_normalized.csv")
        df6 = df4.loc[:, ["subject_areas", "professors", "citation_num", "title"]]
        df6 = pd.get_dummies(
            data=df6, columns=["subject_areas"], prefix="", prefix_sep=""
        )
        df6["subject_areas"] = df4["subject_areas"]
        df6 = df6.groupby(
            by=["professors", "title", "subject_areas"], as_index=False
        ).sum()
        # create the graph
        df7 = df6.loc[df6["professors"].isin(prof), :]
        fig = go.Figure()
        color_number = 0
        for sub in df7["subject_areas"].unique():
            local_df = df7.loc[df7[sub] > 0, :]
            # print(colors[color_number])
            fig.add_trace(
                go.Scatterpolargl(
                    r=local_df[sub] * local_df["citation_num"],
                    theta=local_df["subject_areas"],
                    name=str(sub),
                    marker=dict(
                        size=local_df["citation_num"], color=colors[color_number]
                    ),
                )
            )
            color_number = color_number + 1

        fig.update_traces(mode="markers", marker=dict(line_color="white", opacity=0.7))
        fig.update_layout(
            title="cluster papers",
            font_size=15,
            showlegend=False,
            width=1350,
            height=800,
            paper_bgcolor="#E2E3E4",
            polar1=dict(
                bgcolor="rgb(255, 255, 255)",
                angularaxis=dict(
                    linewidth=3,
                    showline=True,
                    showgrid=False,
                    # linecolor='rgb(230, 23, 25)'
                ),
                radialaxis=dict(
                    side="counterclockwise",
                    showline=False,
                    linewidth=2,
                    showgrid=False,
                    gridcolor="white",
                    gridwidth=2,
                    # linecolor='rgb(0, 23, 205)',
                ),
            ),
            # paper_bgcolor="rgb(250, 250, 250)",
        )

        st.plotly_chart(fig)
