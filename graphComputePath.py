import constraints
import numpy as np

def get_argmin(l):
    v = np.Infinity
    r = 0
    for i in range(len(l)):
        if l[r] <= v:
            v = l[r]
    for i in range(len(l)):
        if l[i] == v:
            return i

def neighbors(g, vertex):
    e = g[1]
    N = []
    for edge in e:
        start = edge[0]
        if vertex == start:
            N.append(edge[1])
    return N

def get_cost(g, a, b):
    e = g[1]
    for edge in e:
        if edge[0] == a and edge[1] == b:
            return edge[2]
    return np.Infinity

def type1_dijkstra(g, a, b, ta, to): # arrivée au plus tôt
    g = constraints.apply_constraints(g, a, b, ta, to)
    v = g[0]
    e = g[1]
    new_e = []

    # poids des arcs nuls
    for i in range(len(e)):
        new_e.append((e[i][0], e[i][1], 0))
    
    # ajout du noeud source
    v.append(("start"))
    
    # ajout des arcs partant de la source
    for vertex in v:
        if vertex[0] == a:
            new_e.append((("start"), vertex, 0))

    # arcs entre les noeuds de fin et le noeud de fin ayant le temps d'arrivé le + petit
    end_nodes = []
    tmin = np.Infinity
    tmin_index = -1
    for vertex in v:
        if vertex[0] == b:
            end_nodes.append(vertex)
            if tmin > vertex[1]:
                tmin = vertex[1]
                tmin_index += 1
    for i in range(len(end_nodes)):
        if i != tmin_index:
            new_e.append((end_nodes[i], end_nodes[tmin_index], end_nodes[i][1]-end_nodes[tmin_index][1]))
    
    # nouveau graph
    gt = (v, new_e)
    
    # noeuds de départ
    starting_nodes = []
    for vertex in v:
        if vertex[0] == a:
            starting_nodes.append(vertex)

    cost = {}
    path = {}
    for vertex in v:
        if vertex in starting_nodes:
            cost[vertex] = 0
        else:
            cost[vertex] = np.Infinity
    
    # get current source
    keys = list(cost.keys())
    argmin = min(range(len(list(cost.values()))), key=list(cost.values()).__getitem__)
    source = keys[argmin]

    # get neighbors of current source
    N = neighbors(gt, source)

    # update cost
    for nb in N:
        cost[nb] = get_cost(gt, source, nb)
        # update path
        if nb not in path:
            path[(nb)] = source
    del cost[source]

    while len(cost) > 0:
        # get current source
        keys = list(cost.keys())
        argmin = min(range(len(list(cost.values()))), key=list(cost.values()).__getitem__)
        source = keys[argmin]

        # get neighbors of current source
        N = neighbors(gt, source)

        # update cost
        for nb in N:
            if nb not in cost.keys():
                continue
            c = get_cost(gt, source, nb)
            if cost[nb] != np.Infinity and (cost[source] + c) < cost[nb]:
                cost[nb] = cost[source] + c
                path[(nb)] = source
            else:
                cost[nb] = c
            # update path
            if nb not in path:
                path[(nb)] = source
        del cost[source]

    # backtrack
    res = []
    node = end_nodes[tmin_index]
    
    while path[node] not in starting_nodes:
        res.append(node)
        node = path[node]
    res.append(node)
    if node not in starting_nodes:
        res.append(path[node])
    res.reverse()
    return res

def type2_dijkstra(g, a, b, ta, to): # départ au plus tard
    g = constraints.apply_constraints(g, a, b, ta, to)
    v = g[0]
    e = g[1]
    
    # arcs entre le noeud le + tardif et les autres noeuds de départ
    starting_nodes = []
    tmax = -1
    tmax_index = -1
    for vertex in v:
        if vertex[0] == a:
            starting_nodes.append(vertex)
            if tmax < vertex[1]:
                tmax = vertex[1]
                tmax_index += 1
    for i in range(len(starting_nodes)):
        if i != tmax_index:
            e.append((starting_nodes[tmax_index], starting_nodes[i], starting_nodes[tmax_index][1]-starting_nodes[i][1]))

    cost = {}
    path = {}
    for vertex in v:
        if vertex == starting_nodes[tmax_index]:
            cost[vertex] = 0
        else:
            cost[vertex] = np.Infinity
    
    # get current source
    keys = list(cost.keys())
    argmin = min(range(len(list(cost.values()))), key=list(cost.values()).__getitem__)
    source = keys[argmin]
    # get neighbors of current source
    N = neighbors(g, source)

    # update cost
    for nb in N:
        cost[nb] = get_cost(g, source, nb)
        # update path
        if nb not in path:
            path[(nb)] = source
    del cost[source]

    while len(cost) > 0:
        # get current source
        keys = list(cost.keys())
        argmin = min(range(len(list(cost.values()))), key=list(cost.values()).__getitem__)
        source = keys[argmin]

        # get neighbors of current source
        N = neighbors(g, source)

        # update cost
        for nb in N:
            if nb not in cost.keys():
                continue
            c = get_cost(g, source, nb)
            if cost[nb] != np.Infinity and (cost[source] + c) < cost[nb]:
                cost[nb] = cost[source] + c
                path[(nb)] = source
            else:
                cost[nb] = c
            # update path
            if nb not in path:
                path[(nb)] = source
        del cost[source]
    
    # backtrack
    end_nodes = []
    for vertex in v:
        if vertex[0] == b:
            end_nodes.append(vertex)
    res = []
    for node in end_nodes:
        sub_res = []
        while path[node] != starting_nodes[tmax_index]:
            sub_res.append(node)
            node = path[node]
        sub_res.append(node)
        if node not in starting_nodes:
            sub_res.append(path[node])
        sub_res.reverse()
        res.append(sub_res)
    tmax = -1
    index_max = -1
    for r in range(len(res)):
        if tmax < res[r][0][1]:
            tmax = res[r][0][1]
            index_max = r
    return res[index_max]

def type3_dijkstra(g, a, b, ta, to): # chemin le plus rapide
    g = constraints.apply_constraints(g, a, b, ta, to)
    v = g[0]
    e = g[1]
    
    # arcs entre le noeud le + tardif et les autres noeuds de départ
    starting_nodes = []
    tmax = -1
    tmax_index = -1
    for vertex in v:
        if vertex[0] == a:
            starting_nodes.append(vertex)
            if tmax < vertex[1]:
                tmax = vertex[1]
                tmax_index += 1
    for i in range(len(starting_nodes)):
        if i != tmax_index:
            e.append((starting_nodes[tmax_index], starting_nodes[i], starting_nodes[tmax_index][1]))

    # arcs entre les noeuds de fin et le noeud de fin ayant le temps d'arrivé le + petit
    end_nodes = []
    tmin = np.Infinity
    tmin_index = -1
    for vertex in v:
        if vertex[0] == b:
            end_nodes.append(vertex)
            if tmin > vertex[1]:
                tmin = vertex[1]
                tmin_index += 1
    for i in range(len(end_nodes)):
        if i != tmin_index:
            e.append((end_nodes[i], end_nodes[tmin_index], end_nodes[i][1]))

    cost = {}
    path = {}
    for vertex in v:
        if vertex == starting_nodes[tmax_index]:
            cost[vertex] = 0
        else:
            cost[vertex] = np.Infinity
    
    # get current source
    keys = list(cost.keys())
    argmin = min(range(len(list(cost.values()))), key=list(cost.values()).__getitem__)
    source = keys[argmin]

    # get neighbors of current source
    N = neighbors(g, source)

    # update cost
    for nb in N:
        cost[nb] = get_cost(g, source, nb)
        # update path
        if nb not in path:
            path[(nb)] = source
    del cost[source]

    while len(cost) > 0:
        # get current source
        keys = list(cost.keys())
        argmin = min(range(len(list(cost.values()))), key=list(cost.values()).__getitem__)
        source = keys[argmin]

        # get neighbors of current source
        N = neighbors(g, source)

        # update cost
        for nb in N:
            if nb not in cost.keys():
                continue
            c = get_cost(g, source, nb)
            if cost[nb] != np.Infinity and (cost[source] + c) < cost[nb]:
                cost[nb] = cost[source] + c
                path[(nb)] = source
            else:
                cost[nb] = c
            # update path
            if nb not in path:
                path[(nb)] = source
        del cost[source]

    # backtrack
    res = []
    for node in end_nodes:
        sub_res = []
        while path[node] != starting_nodes[tmax_index]:
            sub_res.append(node)
            node = path[node]
        sub_res.append(node)
        if node not in starting_nodes:
            sub_res.append(path[node])
        sub_res.reverse()
        res.append(sub_res)
    d = []
    for r in res:
        duration = r[len(r)-1][1] - r[0][1]
        d.append(duration)
    return res[np.argmin(d)]

def type4_dijkstra(g, a, b, ta, to): # plus court chemin
    g = constraints.apply_constraints(g, a, b, ta, to)
    v = g[0]
    e = g[1]
    # ajout du noeud source et du noeud terminal
    v.append(("start"))
    v.append(("end"))
    # ajout des arcs partant de la source, et ceux arrivant vers le noeud terminal
    for vertex in v:
        if vertex[0] == a:
            e.append((("start"), vertex, 0))
        elif vertex[0] == b:
            e.append((vertex, ("end"), 0))
    
    cost = {}
    path = {}
    for vertex in v:
        if vertex == "start":
            cost[vertex] = 0
        else:
            cost[vertex] = np.Infinity
    
    # get current source
    keys = list(cost.keys())
    argmin = min(range(len(list(cost.values()))), key=list(cost.values()).__getitem__)
    source = keys[argmin]
        
    # get neighbors of current source
    N = neighbors(g, source)

    # update cost
    for nb in N:
        cost[nb] = get_cost(g, source, nb)
        # update path
        if nb not in path:
            path[(nb)] = "start"
    del cost[source]

    while len(cost) > 0:
        # get current source
        keys = list(cost.keys())
        argmin = min(range(len(list(cost.values()))), key=list(cost.values()).__getitem__)
        source = keys[argmin]
        
        # get neighbors of current source
        N = neighbors(g, source)
        
        # update cost
        for nb in N:
            if nb not in cost.keys():
                continue
            c = get_cost(g, source, nb)
            if cost[nb] != np.Infinity and (cost[source] + c) < cost[nb]:
                cost[nb] = cost[source] + c
                path[(nb)] = source
            else:
                cost[nb] = c
            # update path
            if nb not in path:
                path[(nb)] = source
        del cost[source]

    # backtrack
    res = []
    node = ("end")
    while path[node] != "start":
        res.append(node)
        node = path[node]
    res.append(node)
    res.reverse()
    res = res[0:-1]
    
    return res
