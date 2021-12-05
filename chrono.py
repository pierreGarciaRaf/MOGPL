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

nv_time = {}
ne_time = {}

def measure(files):
    for f in files:
        mg,g = gr.createMultigraphAndGraphFromFile(f)
        num_vertex = len(g[0])
        num_edge = len(g[1])
        print("compute execution time for graph : ", f, ", (", num_vertex, " vertices and ", num_edge, " edges)")
        start = time.clock()
        path = gcp.type4_dijkstra(g, 'a', 'f')
        end = time.clock()
        t = end - start
        nv_time[num_vertex] = t
        ne_time[num_edge] = t

def create_graphs():
    x = np.array(list(nv_time.keys()))
    y = np.array(list(nv_time.values()))

    # création du graphe des temps
    plt.figure(figsize=(15,15))
    plt.grid(True, "both")
    plt.minorticks_on()
    plt.plot(x,y, c="blue")
    plt.legend(fontsize=15)
    plt.title("Temps d'éxecution Dijkstra sur chemin de type 4 en fonction du nombre de sommets")
    plt.xlabel("nombre de sommets")
    plt.ylabel("temps d'éxecution (sec)")
    plt.savefig("perfs.png")

argLen = len(sys.argv)
graphs = sys.argv[1:]
measure(graphs)
create_graphs()
