
def get_graph(train, str_from="FROM", str_to="TO", directed=False):
    """
    Graph object from data frame
    """
    G = nx.DiGraph() if directed==True else nx.Graph()