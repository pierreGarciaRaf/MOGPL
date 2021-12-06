#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
import graphComputePath as gcp
import graphReader as gr
import time

nv_time = {} # time against number of vertex
ne_time = {} # time against number of edges

def measure(files, ta, to):
    for f in files:
        mg,g = gr.createMultigraphAndGraphFromFile(f)
        num_vertex = len(g[0])
        num_edge = len(g[1])
        print("compute execution time for graph : ", f, ", (", num_vertex, " vertices and ", num_edge, " edges)")
        start = time.time()
        path = gcp.type4_dijkstra(g, 'a', 'f', int(ta), int(to))
        end = time.time()
        t = end - start
        nv_time[num_vertex] = t
        ne_time[num_edge] = t

def create_graph(vertex = False, edges = False):
    x = np.array(list(nv_time.keys()))
    y = np.array(list(nv_time.values()))

    # création du graphe des temps en fonction du nombre de sommets
    plt.figure(figsize=(15,15))
    plt.grid(True, "both")
    plt.minorticks_on()
    plt.plot(x,y, c="blue")
    plt.legend(fontsize=15)
    if vertex:
        plt.title("Temps d'éxecution Dijkstra sur chemin de type 4 en fonction du nombre de sommets")
        plt.xlabel("nombre de sommets")
    else:
        plt.title("Temps d'éxecution Dijkstra sur chemin de type 4 en fonction du nombre d'arcs")
        plt.xlabel("nombre d'arcs")
    plt.ylabel("temps d'éxecution (sec)")
    if vertex:
        plt.savefig("perfs_vertex_count.png")
    else:
        plt.savefig("perfs_edges_count.png")

argLen = len(sys.argv)
ta = sys.argv[1]
to = sys.argv[2]
graphs = sys.argv[3:]
measure(graphs, ta, to)
create_graph(True, False)
create_graph(False, True)
