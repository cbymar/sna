import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import itertools
import math
import random

# DFS
g = nx.erdos_renyi_graph(25, 0.3, seed=867, directed=False)
g.number_of_edges() # vs (n ** 2 - nß)/2
{print(k, v) for k, v in g.adjacency()}
adjacencydict = dict((x, g.neighbors(x)) for x in g.nodes())
adjacencydict.items()
g.number_of_nodes()
g.edges()  # returns list of tuples
# to get an adjacency dict:


# draw with matplotlib/pylab
plt.figure(figsize=(8, 8))
# with nodes colored by degree sized by population
node_color = [float(g.degree(v)) for v in g]
edge_cmap = [float(g.get_edge_data(u, v)["weight"]) for u,v in g.edges()]
nx.draw(
    g,
    node_color=node_color,
    with_labels=True,
    edge_color=edge_cmap,
)

plt.show()
plt.savefig("./ignoreland/firstgraphdrawn.png")

"""Depth-first search"""
# we can keep track of edges traversed as well as nodes

def DFSnodes(graph, node, visited=[]):
    """returns the nodes visited"""
    visited.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            DFSnodes(graph, neighbor, visited)
    return visited


def DFSedges(graph, node, visited=[], edges=[]):
    """returns the edges spanned"""
    visited.append(node)
    for ni in graph[node]:
        if ni not in visited:
            edges.append((node, ni))  # add the spanned edge
            DFSedges(graph, ni, visited, edges)
    return edges

DFSnodes(g, 1, visited=[])
DFSedges(g, 2, visited=[], edges=[])

edgestraversed_a = []
for _ in nx.traversal.dfs_edges(g):
    edgestraversed_a.append(_)


edgestraversed = []
for k, v in nx.traversal.dfs_successors(g).items():
    edgestraversed.append((k, v[0]))
edgestraversed
edgestraversed == edgestraversed_a  # not equal because the dict contains lists as the values

#### traversing a graph results in a directed graph
directedtree = nx.traversal.dfs_tree(g)

directedtree.succ  # this is an adjacency dict.

#### Breadth-first search.  Cannot be done recursively.

def BFSnodes(graph, node, Q=[]):
    """returns the nodes visited"""
    d = dict()
    d[node] = 0
    Q.insert(0, node)
    while len(Q) != 0:
        newnode = Q.pop()
        for ni in graph[newnode]:
            if ni not in d:
                d[ni] = d[newnode] + 1
                Q.insert(0, ni)
    return d

dd = BFSnodes(g, 1, Q=[])


def invertd(dict):
    """Inverts dict and groups keys by values"""
    outdict = defaultdict(list)
    for k, v in dict.items():
        outdict[v].append(k)
    return outdict

invertd(dd)

#########################################################
### Paths
nx.algorithms.shortest_path(g, 1, 21)
# Dijkstra's algo finds lowest-cost path
nx.algorithms.dijkstra_path(g, 1, 21)

list(itertools.combinations(g.nodes(),2))
nn = list(g.nodes())  # essentially a tuple
nn
# check out the iterable unpacking:
for pair in itertools.combinations(nn[:8], 2):
    print(nx.algorithms.shortest_path(g, *pair),
          nx.algorithms.dijkstra_path(g, *pair))

ee = list(g.edges())
## Add edge weights by appending a tuple of length 1 to each edge tuple
weighted_edges = [x + (random.choice(range(10)), ) for x in ee]
weighted_edges
g.clear()
g.add_weighted_edges_from(weighted_edges)
# Re-run the above, now with weight to take into account (paths may differ)
for pair in itertools.combinations(nn[:8], 2):
    print(pair,
          nx.algorithms.shortest_path(g, *pair),
          nx.algorithms.dijkstra_path(g, *pair),
          nx.path_weight(g, nx.algorithms.shortest_path(g, *pair), weight="weight"),
          nx.algorithms.dijkstra_path_length(g, *pair))


#### Dijkstra's algo





