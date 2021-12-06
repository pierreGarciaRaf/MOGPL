#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
import graphComputePath as gcp
import graphPathComputation as gpc
import graphReader as gr
import time
import networkx as nx
import toPLB

nv_time = {} # time against number of vertex
ne_time = {} # time against number of edges

def measure(graphs, ta, to, solver = gcp.type4_dijkstra):
    for g in graphs:
        num_vertex = len(g[0])
        num_edge = len(g[1])
        print("compute execution time for graph : (", num_vertex, " vertices and ", num_edge, " edges)")
        start = time.time()
        path = solver(g, '0', str(num_vertex-1), int(ta), int(to))
        end = time.time()
        t = end - start
        nv_time[num_vertex] = t
        ne_time[num_edge] = t

def create_graph(vertex = False, edges = False, prefix = "dijkstra"):
    x = np.array(list(nv_time.keys()))
    y = np.array(list(nv_time.values()))

    # création du graphe des temps en fonction du nombre de sommets
    plt.figure(figsize=(15,15))
    plt.grid(True, "both")
    plt.minorticks_on()
    plt.plot(x,y, c="blue")
    plt.legend(fontsize=15)
    if vertex:
        plt.title("Temps d'éxecution "+prefix+" sur chemin de type 4 en fonction du nombre de sommets")
        plt.xlabel("nombre de sommets")
    else:
        plt.title("Temps d'éxecution "+prefix+" sur chemin de type 4 en fonction du nombre d'arcs")
        plt.xlabel("nombre d'arcs")
    plt.ylabel("temps d'éxecution (sec)")
    if vertex:
        plt.savefig(prefix+"_perfs_vertex_count.png")
    else:
        plt.savefig(prefix+"_perfs_edges_count.png")

argLen = len(sys.argv)
ta = sys.argv[1]
to = sys.argv[2]
num_nodes_per_graph = sys.argv[3:]
graphs = []
for i in range(len(num_nodes_per_graph)):
    nodes = int(num_nodes_per_graph[i])
    tree = nx.random_tree(n=nodes, seed=0, create_using=nx.DiGraph)
    vertex_list = list(tree.nodes)
    edges_list = list(tree.edges)
    vlist = []
    elist = []
    for v in vertex_list:
        start_travel = len(nx.shortest_path(tree, source=0, target=v))
        vlist.append((str(v), start_travel))
    for e in edges_list:
        travel1 = len(nx.shortest_path(tree, source=0, target=e[0]))
        travel2 = len(nx.shortest_path(tree, source=0, target=e[1]))
        elist.append(((str(e[0]), travel1), (str(e[1]), travel2), 1))
    g = (vlist, elist)
    graphs.append(g)

measure(graphs, ta, to)
create_graph(True, False, "dijkstra")
create_graph(False, True, "dijkstra")

measure(graphs, ta, to, solver = toPLB.solveType4PL)
create_graph(True, False, "pl")
create_graph(False, True, "pl")


measure(graphs, ta, to, solver = gpc.solveType4DjikstraOptimized)
create_graph(True, False, "dijkstraOpt")
create_graph(False, True, "dijkstraOpt")
print(sys.argv[3:])
print(nv_time)