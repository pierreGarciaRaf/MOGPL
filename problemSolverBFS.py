import graphPathComputation as gpc
"""
vertex := string*int
0-Name
1-Time


edge := vertex*vertex*int
0-Start vertex
1-End vertex
2-Cost

graph := list(vertex)*list(edge)
"""
def genWithoutVertices(g, toRemoveId):
    V,E = g
    newG = V.copy(),E.copy()
    removedVertices = []
    for i in range(len(toRemoveId)):
        removedVertices.append(newG[0].pop(toRemoveId[i]))
    for e in E:
        fr,to,_ = e
        if fr in removedVertices or to in removedVertices:
            newG[1].remove(e)
    return newG


def removeHighestVertices(g, vertexName, toSortWith, numberToKeep):
    V,E = g
    verticesToFilterId = []
    for id,v in enumerate(V):
        if v[0] == vertexName:
            verticesToFilterId.append(id)
    verticesToFilterId = sorted(verticesToFilterId, key = lambda i : toSortWith(V[i][1]))
    
    if numberToKeep > len(verticesToFilterId):
        return False
    verticesToRemove = []
    for i in range(numberToKeep, len(verticesToFilterId)):
        verticesToRemove.append(verticesToFilterId[i])
    return genWithoutVertices(g, verticesToRemove)


def generateForBfs(g, startVertex, endVertex, type):
    if type <1 or type > 3:
        raise Exception("bfs can only resolve 1,2 & 3 problems, not %d"%type)
    if type == 1:
        toKeep = 1
        toAdd = removeHighestVertices(g, endVertex, lambda x : -x, 1)
        gs = []
        while toAdd != False:
            gs.append(toAdd)
            toKeep += 1
            toAdd = removeHighestVertices(g,endVertex,lambda x : -x, toKeep)
        return gs
    if type == 2:
        toKeep = 1
        toAdd = removeHighestVertices(g, startVertex, lambda x : x, 1)
        gs = []
        while toAdd != False:
            gs.append(toAdd)
            toKeep += 1
            toAdd = removeHighestVertices(g,startVertex,lambda x : x, toKeep)
        return gs
    if type == 3:
        toKeepStart = 1
        toKeepFinish = 1
        toAdd = removeHighestVertices(\
                removeHighestVertices(g, startVertex, lambda x : x, toKeepStart)\
                                       , endVertex, lambda x: -x, toKeepFinish)

        gs = []
        while toAdd != False:
            toKeepFinish += 1
            toKeepStart = 1
            toAdd = removeHighestVertices(\
                removeHighestVertices(g, startVertex, lambda x : x, toKeepStart)\
                                       , endVertex, lambda x: -x, toKeepFinish)
            while toAdd != False:
                gs.append(toAdd)
                toKeepStart += 1
                toAdd = removeHighestVertices(\
                removeHighestVertices(g, startVertex, lambda x : x, toKeepStart)\
                                       , endVertex, lambda x: -x, toKeepFinish)
        return gs

def solveBFS(modifiedGraphs, startVertex, endVertex):
    for g in modifiedGraphs:
        sol = gpc.bfs(g,startVertex, endVertex)
        if len(sol) > 0:
            return sol
    return []