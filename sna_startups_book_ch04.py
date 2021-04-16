import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import itertools
import logging
import math
import os
import random
import shutil
import sys
import time
import urllib3


#### import egypt retweets
url = "https://raw.githubusercontent.com/maksim2042/SNABook/master/chapter1/egypt_retweets.net"
pathout = "./ignoreland/egypt_retweets.net"
http = urllib3.PoolManager()

with http.request("GET", url, preload_content=False) as r:
    with open(pathout, "wb") as out_file:
        shutil.copyfileobj(r, out_file)

e = nx.read_pajek(pathout)
len(e)
len(nx.connected_components(e))

e_ccsg = (e.subgraph(_) for _ in nx.connected_components(e))
len(list(e_ccsg))
e_ccsg = (e.subgraph(_) for _ in nx.connected_components(e))
x = [len(_) for _ in e_ccsg if len(_) > 10]
x[:9]
plt.hist(x)

#### apply island method to scrub subgraph strength
def trim_edges(g, weight=1):
    """Builds graph from threshold-meeting edges of input graph"""
    g2 = nx.Graph()
    for fnode, tonode, edgedata in g.edges(data=True):
        if edgedata["weight"] > weight:
            g2.add_edge(fnode, tonode, **edgedata)
    return g2


def island_method(g, niters=6):
    """"""
    weights = [edgedata["weight"] for fnode, tonode, edgedata in g.edges(data=True)]

    minweight = int(min(weights))
    maxweight = int(max(weights))

    stepsize = int( (maxweight-minweight) / niters)

    return [ [weight, trim_edges(g, weight)] for weight in range(minweight, maxweight, stepsize)]

biggest_cs = next(e.subgraph(_) for _ in nx.connected_components(e))
len(biggest_cs)

islands = island_method(biggest_cs, niters=6)
for i in islands:
    print(i[0], len(i[1]), len([e.subgraph(_) for _ in nx.connected_components(i[1])]))


#### Examining some ego graphs
nx.ego_graph(biggest_cs, "justinbieber")
bieber = nx.Graph(nx.ego_graph(biggest_cs, "justinbieber", radius=2))
len(bieber)
nx.average_clustering(bieber)

#################
#### Documentation aside:
# https://networkx.org/documentation/stable/reference/classes/index.html#basic-graph-types
# Graph views can be chained/chain depth needs to be kept in mind (for performance)
# reverse_view() is useful for reversing edge directions
# Filters can be pretty custom
