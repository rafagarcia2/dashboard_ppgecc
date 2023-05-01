import pandas as pd
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from utils.config_colors import colors


def plot_graph(data):
    df4 = data
    # print(df)

    st.markdown(
        "<h1 style='text-align: center; color: #0F2D9F;font-size: 14 px ;'> Bem vindo à sessão de grafos </h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h2 style='text-align: center; color: #000000;font-size: 12 px ;'> Selecione as informações que deseja visualizar </h2>",
        unsafe_allow_html=True,
    )
    options = ["Professores", "Papers", "Temas", "Conferencia"]
    col1, col2 = st.columns(2)
    with col1:
        option1 = st.selectbox("primeiro campo", options=options)
    with col2:
        option2 = st.selectbox("segundo campo", options=options)
    if option1 == option2:
        st.warning("Campos iguais, por favor selecione campos diferentes")
    else:
        fields = {
            "Professores": ["professors", "#222177"],
            "Papers": ["title", "#4F62EE"],
            "Temas": ["subject_areas", "#443576"],
            "Conferencia": ["conference_name", "#23AC86"],
        }
        field1 = fields[option1]
        field2 = fields[option2]
        nodes = []
        edges = []
        # multiselect the professors in the list
        prof = st.multiselect(
            label=str(option1) + " a visualizar:",
            options=df4[field1[0]].dropna().unique(),
        )
        # filter the data by the professors selected
        df4 = pd.DataFrame(df4.loc[df4[field1[0]].isin(prof), [field1[0], field2[0]]])

        df = pd.get_dummies(data=df4, columns=[field2[0]], prefix="", prefix_sep="")

        df = df.groupby(by=field1[0], as_index=False).sum()
        # create the professor's nodes
        for i in prof:
            # set the node size by row sum without professors columns
            size = df.loc[df[field1[0]] == i, :].drop(columns=field1[0]).iloc[0].sum()
            # use the professor name as node's id
            id = str(i)
            # append the node in the node's list
            nodes.append(Node(id=id, label=id, size=10 * (int(size)), color=field1[1]))

        # create the theme's nodes
        for i in df.drop(columns=field1[0]).columns:
            # create the size by column's sum
            size = int(df[i].sum())
            # create the node if it has connections in the table
            if size > 0:
                # node id == theme's name
                nodes.append(
                    Node(id=i, label=i, size=10 * (int(size)), color=field2[1])
                )

        # link the nodes using the id's
        for i in prof:
            # filter the data without
            data = (
                df.loc[df[field1[0]] == i, :]
                .drop(columns=[field1[0]])  # , "Unnamed: 1"
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
