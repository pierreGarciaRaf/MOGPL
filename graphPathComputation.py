import numpy as np
from numpy.core.numerictypes import ScalarType
import sys
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

def genVertToIndexDict(V):
    """
        list(vertex) -> dict(vertex->int)
    """
    vertToIndex = {}
    for i,v in enumerate(V):
        vertToIndex[v] = i
    return vertToIndex


def generateConnexityMatrix(g, vertToIndex):
    """
        graph*dict(vertex->int) -> narray(bool)
    """
    V,E = g
    connMat = np.zeros((len(V),len(V)), "bool")

    for fr,to,_ in E:
        connMat[vertToIndex[fr],vertToIndex[to]] = True
    return connMat

def getNeighbors(vertexId, connMat):
    """
        int,narray(bool) -> narray(int)
    """
    return np.arange(len(connMat))[connMat[vertexId]]

def substractSets(setA,setB):
    """
        narray(a),narray(a) -> narray(a)
    """
    if len(setA) == 0:
        return []

    if len(setB) == 0:
        return setA
    toKeepFromA = np.ones(len(setA),"bool")
    for b in setB:
        toKeepFromA *= np.vectorize(lambda x : x != b)(setA)
    return setA[toKeepFromA]

def backtrackBfs(layers,connexityMat,endVertexIdx):
    """
        list(narray(int))*narray(bool)*int -> narray(int)
    """
    path = np.zeros(len(layers), "uint8")
    path[-1] = endVertexIdx
    for i in range(len(layers)-2,-1,-1):
        isPathPossible = connexityMat[layers[i],path[i+1]]
        
        pretedents = np.argmax(isPathPossible)
        if pretedents is np.array:
            path[i] = layers[i][pretedents[0]]
        else:
            path[i] = layers[i][pretedents]
    return path



def bfs(g, startVertex, targetVertex):
    """
        graph*vertex*vertex -> list(vertex)
    """
    V,E = g
    vertToIndex = genVertToIndexDict(V)
    connMat = generateConnexityMatrix(g,vertToIndex)
    layers = [np.array([vertToIndex[startVertex]])]
    targetVertexId = vertToIndex[targetVertex]
    lastLayer = layers[len(layers)-1]
    while not targetVertexId in lastLayer:
        newLayer = np.zeros(0,"uint8") 
        for id in lastLayer:
            neighbors = getNeighbors(id, connMat)            
            for layerIdx in range(len(layers)-1):
                neighbors = substractSets(neighbors, layers[layerIdx])
            neighbors = substractSets(neighbors,newLayer)
            newLayer = np.concatenate((newLayer,neighbors))
        layers.append(newLayer)
        lastLayer = layers[len(layers)-1]
    path = backtrackBfs(layers, connMat, targetVertexId)
    return [V[path[i]] for i in range(len(path))]

def genCostMat(connMat, vertexToIndexDict,g):
    """
        narray(int)*dict(vertex->int)*g->narray(int)
    """
    _,E = g
    toRet = np.zeros(connMat.shape, "uint") + sys.maxsize
    for fr,to,cost in E:
        toRet[vertexToIndexDict[fr],vertexToIndexDict[to]] = cost
    return toRet
    

def djikstra(g, startVertex, targetVertex):
    """
        graph*vertex*vertex -> list(vertex)
    """
    V,_ = g
    vertToIndex = genVertToIndexDict(V)
    connMat = generateConnexityMatrix(g,vertToIndex)
    costMat = genCostMat(connMat, vertToIndex, g)
    print(costMat)
    edgeVisitMat = np.zeros(connMat.shape, "bool")
    neverToVisitAgainVertices = [vertToIndex[startVertex]]
    S = [vertToIndex[startVertex]]
    currentVertices = [S[0]]
    distances = np.zeros(len(V), "uint") + sys.maxsize
    distances[S[0]] = 0
    while len(neverToVisitAgainVertices) != len(V):
        currentVertices = S.copy()
        for currentVertex in currentVertices:
            for neighbor in substractSets(  getNeighbors(currentVertex, connMat),
                                            np.array(neverToVisitAgainVertices)):

                S.append(neighbor)
                distances[neighbor] = min(distances[currentVertex]\
                                            + costMat[currentVertex, neighbor],
                                            distances[neighbor])
                print(distances[currentVertex], costMat[currentVertex, neighbor])
                if currentVertex in neverToVisitAgainVertices:
                    edgeVisitMat[currentVertex, neighbor] = True
                    if (edgeVisitMat[:,neighbor]==connMat[:,neighbor]).all():
                        neverToVisitAgainVertices.append(neighbor)
    return S, distances
