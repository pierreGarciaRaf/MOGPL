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

def pathIdToPathVertex(pathId, V):
    return [V[pathId[i]] for i in range(len(pathId))]

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
    return pathIdToPathVertex(path,V)

def genCostMat(connMat, vertexToIndexDict,g):
    """
        narray(int)*dict(vertex->int)*g->narray(int)
    """
    _,E = g
    toRet = np.zeros(connMat.shape, "uint") + sys.maxsize
    for fr,to,cost in E:
        toRet[vertexToIndexDict[fr],vertexToIndexDict[to]] = cost
    return toRet
    
def djikstraBackTrack(indexToDistance, connMat, costMat, targetVertexId, startVertexId):
    """
        narray(int)*narray(bool)*narray(int)*int->narray(int)

        0-distances from startVertexId calculated by djikstra on the graph

        1-connexity matrix

        2-cost matrix

        3-target vertex index

        3-start vertex index
    """
    vertexNb = len(connMat)
    rPath = [targetVertexId]
    rConnMat = np.transpose(connMat)
    while not startVertexId == rPath[len(rPath)-1]:
        currVert = rPath[len(rPath)-1]
        for edgeId in np.arange(vertexNb)[rConnMat[currVert]]:
            if costMat[edgeId,currVert] + indexToDistance[edgeId] == indexToDistance[currVert]:
                rPath.append(edgeId)
                break
    return np.flip(np.array(rPath))


def djikstra(g, startVertex, targetVertex):
    """
        graph*vertex*vertex -> list(vertex)
    """
    V,_ = g
    vertToIndex = genVertToIndexDict(V)
    connMat = generateConnexityMatrix(g,vertToIndex)
    costMat = genCostMat(connMat, vertToIndex, g)
    edgeVisitMat = np.zeros(connMat.shape, "bool")
    neverToVisitAsNeighborAgainVertices = [vertToIndex[startVertex]]
    S = [vertToIndex[startVertex]]
    currentVertices = [S[0]]
    distances = np.zeros(len(V), "uint") + sys.maxsize
    distances[S[0]] = 0
    toVisitVertices = S.copy()
    targetVertexId = vertToIndex[targetVertex]
    while not targetVertexId in neverToVisitAsNeighborAgainVertices:
        currentVertices = toVisitVertices.copy()
        for currentVertex in currentVertices:
            neighbors = getNeighbors(currentVertex, connMat)
            if len(neighbors) == 0:
                toVisitVertices.remove(currentVertex)
                continue
            for neighbor in neighbors:
                S.append(neighbor)
                toVisitVertices.append(neighbor)
                distances[neighbor] = min(distances[currentVertex]\
                                            + costMat[currentVertex, neighbor],
                                            distances[neighbor])
                if currentVertex in neverToVisitAsNeighborAgainVertices:
                    edgeVisitMat[currentVertex, neighbor] = True
                    if (edgeVisitMat[:,neighbor]==connMat[:,neighbor]).all():
                        neverToVisitAsNeighborAgainVertices.append(neighbor) #never to visit as a neighbor
                        connMat[:,neighbor] = False #so get neighbors doesn't yell this vertex again.
    pathId = djikstraBackTrack(distances, generateConnexityMatrix(g,vertToIndex), costMat, targetVertexId, vertToIndex[startVertex])
    return pathIdToPathVertex(pathId,V) 
