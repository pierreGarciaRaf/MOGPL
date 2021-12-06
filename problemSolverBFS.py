from numpy.core.fromnumeric import argmin
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


def getGraphGeneratedVertices(g, mgVertex):
    V,_ = g
    toRet = []
    for v in V:
        if v[0] == mgVertex:
            toRet.append(v)
    return toRet

def removeHighestVertices(g, vertexName, toSortWith, numberToKeep):
    V,E = g
    verticesToFilterId = []
    for id,v in enumerate(V):
        if v[0] == vertexName:
            verticesToFilterId.append(id)
    verticesToFilterId = sorted(verticesToFilterId, key = lambda i : toSortWith(V[i][1]))

    if numberToKeep > len(verticesToFilterId):
        return (" ",-1),[]
    verticesToRemove = []
    for i in range(numberToKeep, len(verticesToFilterId)):
        verticesToRemove.append(verticesToFilterId[i])
    
    return V[verticesToFilterId[numberToKeep-1]],genWithoutVertices(g, verticesToRemove)


def generateForBfs(g, startVertexName, endVertexName, type):
    if type <1 or type > 3:
        raise Exception("bfs can only resolve 1,2 & 3 problems, not %d"%type)
    if type == 1:
        f = lambda x : x
        toKeep = 1
        ev,toAdd = removeHighestVertices(g, endVertexName, f, 1)
        startVertices = getGraphGeneratedVertices(g,startVertexName)
        sv = min(startVertices, key = lambda v : v[1])
        gs = []
        while len(toAdd) > 0:
            gs.append((sv,ev,toAdd))
            toKeep += 1
            ev,toAdd = removeHighestVertices(g,endVertexName,f, toKeep)
        
        
        return gs
    if type == 2:
        f = lambda x : -x
        toKeep = 1
        sv,toAdd = removeHighestVertices(g, startVertexName, f, 1)
        ev = max(getGraphGeneratedVertices(g,endVertexName))
        gs = []
        while len(toAdd) > 0:
            gs.append((sv,ev,toAdd))
            toKeep += 1
            sv,toAdd = removeHighestVertices(g,startVertexName,f, toKeep)
        return gs
    if type == 3:
        f1 = lambda x : -x
        f2 = lambda x : x
        toKeepStart = 1
        toKeepFinish = 1
        sv,toAdd = removeHighestVertices(g, startVertexName, f1, toKeepStart)
        ev,toAdd = removeHighestVertices(toAdd, endVertexName, f2, toKeepFinish)
        gs = []
        while len(toAdd) > 0:
            toKeepFinish += 1
            toKeepStart = 1
            sv,toAdd = removeHighestVertices(g, startVertexName, f1, toKeepStart)
            ev,toAdd = removeHighestVertices(toAdd, endVertexName, f2, toKeepFinish)
            while len(toAdd) > 0:
                gs.append((sv,ev,toAdd))
                toKeepStart += 1
                sv,toAdd = removeHighestVertices(g, startVertexName, f1, toKeepStart)
                if len(toAdd) == 0:
                    break
                ev,toAdd = removeHighestVertices(toAdd, endVertexName, f2, toKeepFinish)
        return gs

def solveBFS(g, startVertexName, endVertexName, type):
    for sv,ev,sg in generateForBfs(g,startVertexName,endVertexName, type):
        sol = gpc.bfs(sg, sv, ev)
        if len(sol) > 0:
            return sol
    return []