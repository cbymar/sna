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

logging.getLogger("urllib3").setLevel(logging.WARNING)

#### Ch 3

g = nx.Graph()

g.add_edge("a", "b")
g.add_edge("b", "c")
g.add_edge("c", "a")

nx.draw(g)
g["a"]["b"]["weight"] = 2
g["a"]["b"]

def read_lj_friends(g, name):
    http = urllib3.PoolManager()
    response = http.request("GET", "https://www.livejournal.com/misc/fdata.bml?user=" + name)

    for line in response.data.decode("utf-8").split("\n"):
        if line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) == 0:
            continue
        if parts[0] == "<":
            g.add_edge(parts[1], name)
        else:
            g.add_edge(name, parts[1])

g = nx.Graph()
read_lj_friends(g, "valerois")
g.number_of_nodes()
nx.draw(g)

#### Snowball sample
def snowball_sampling(g, center, max_depth=1, current_depth=0, taboo_list=[]):
    print(center, current_depth, max_depth, taboo_list)
    if current_depth == max_depth:
        print("out of depth")
        return taboo_list
    if center in taboo_list:
        return taboo_list
    else:
        taboo_list.append(center)

    read_lj_friends(g, center)
    for node in g.neighbors(center):
        taboo_list = snowball_sampling(g, center, max_depth=max_depth,
                                       current_depth=current_depth+1,
                                       taboo_list=[])
    return taboo_list

g = nx.Graph()
snowball_sampling(g, "kozel_na_sakse")
g.number_of_nodes()

nx.write_pajek(g, "./ignoreland/lj_fsnowball.net")

#### Download data from internet:
url = "https://raw.githubusercontent.com/maksim2042/SNABook/master/chapter3/russians.net"
pathout = "./ignoreland/russians.net"
http = urllib3.PoolManager()

with http.request("GET", url, preload_content=False) as r:
    with open(pathout, "wb") as out_file:
        shutil.copyfileobj(r, out_file)

g = nx.read_pajek(pathout)
g.number_of_nodes()
len(g)
degrees_of_graph = dict(nx.degree(g))
type(degrees_of_graph)
degrees_of_graph["valerois"]


#### Create a generator for iterating through the nodes
def show_degrees(g,listnodes):
    deg = nx.degree(g)
    for _ in listnodes:
        yield (_, deg(_))

degrees = show_degrees(g, g.nodes())
degreeslist = list(degrees)  # create list of tuples from the generator
sys.getsizeof(degreeslist)
#### create sorted degree list


def sorted_map(mapping):
    """takes an arbitrary map object, returns descending-value sorted list of tuples"""
    if isinstance(mapping, dict):
        working = [(k, v) for k, v in mapping.items()]
    else:
        working = mapping
    ms = sorted(working, key=lambda x: (-x[1], x[0]))
    return ms

# Test case
type(degreeslist)
msd_fromlist = sorted_map(degreeslist)
type(msd_fromlist)
msd_fromlist[0:9]
degreeslistdict = {k:v for (k, v) in degreeslist}
type(degreeslistdict)
msd_fromdict = sorted_map(degreeslist)
type(msd_fromdict)
msd_fromdict[0:9]
msd_fromlist == msd_fromdict


#### Trim graph to those with at least 2 connections
def graph_trimmed(g, mindegree=2):
    """Takes a graph object, returns separate object filtered to mindegree or more"""
    gout = g.copy()
    d = nx.degree(gout)
    removallist = []
    for _ in gout.nodes():
        if d[_] < mindegree:
            removallist.append(_)
    gout.remove_nodes_from(removallist)
    return gout

g_sub2 = graph_trimmed(g,mindegree=2)

g_sub2.number_of_nodes()
g.number_of_nodes()
# in 2021, we need to convert the nx.degree(graph) to a dict to get a values() attr
min(degrees_of_graph.values())
min(dict(nx.degree(g_sub2)).values())

g_sub20 = graph_trimmed(g,mindegree=20)

cc = nx.closeness_centrality(g_sub20)
cc
cc_sorted = sorted_map(cc)
cc_sorted[0:9]





