import pandas as pd
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from config_colors import colors


def plot_graph():
    df = pd.read_csv("data/graph_csv_2.csv")
    # print(df)
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
        nodes.append(Node(id=id, label=id, size=10 * (int(size)), color="#222177"))

    # create the theme's nodes
    for i in df.drop(columns="professors").columns:
        # create the size by column's sum
        size = int(df[i].sum())
        # create the node if it has connections in the table
        if size > 0:
            # node id == theme's name
            nodes.append(Node(id=i, label=i, size=10 * (int(size)), color="#4F62EE"))

    # link the nodes using the id's
    for i in prof:
        # filter the data without
        data = (
            df.loc[df.professors == i, :]
            .drop(columns=["professors", "Unnamed: 1"])
            .iloc[0]
        )
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
                        width=int(data[j]),
                        color="#CAD8F6",
                        type="CURVE_SMOOTH",  # type="STRAIGHT"
                    )
                )

    # set the graphs view config to the agraph component
    config = Config(
        width=1400,
        height=500,
        directed=False,
        onclick="focus",
        nodeHighlightBehavior=False,
        highlightColor="#F31234",  # or "blue"
        collapsible=False,
        node={"labelProperty": "label"},
        link={"labelProperty": "label", "renderLabel": True},
        graphviz_layout=None
        # **kwargs e.g. node_size=1000 or node_color="blue"
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config)
    return prof
