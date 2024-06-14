import networkx as nx


class Thread(nx.Edge):
    """
    Thread class is an edge in the graph that represents a thread of object state
    with it's previous state in time.
    """
    