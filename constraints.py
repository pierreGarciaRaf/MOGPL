def apply_constraints(g, a, b, ta, to):
    v = g[0]
    e = g[1]
    new_v = []
    del_v = []
    new_e = []
    for vertex in v:
        if vertex[0] == a and vertex[1] >= ta:
            new_v.append(vertex)
        elif vertex[0] == b and vertex[1] <= to:
            new_v.append(vertex)
        elif vertex[0] != a and vertex[0] != b:
            new_v.append(vertex)
        else:
            del_v.append(vertex)
    for edge in e:
        if edge[0] in del_v or edge[1] in del_v:
            continue
        new_e.append(edge)
    g = (new_v, new_e)
    return g
