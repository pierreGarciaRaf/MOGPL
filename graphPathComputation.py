from operator import ne
import numpy as np
from numpy.core.numerictypes import ScalarType
import sys
import constraints
import problemSolverBFS
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
    return np.arange(len(connMat), dtype="uint")[connMat[vertexId]]

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
    while not targetVertexId in lastLayer and len(lastLayer) > 0:
        newLayer = np.zeros(0,"uint8") 
        for id in lastLayer:
            neighbors = getNeighbors(id, connMat)
            for layerIdx in range(len(layers)-1):
                neighbors = substractSets(neighbors, layers[layerIdx])
            neighbors = substractSets(neighbors,newLayer)
            newLayer = np.concatenate((newLayer,neighbors))
        layers.append(newLayer.astype("uint"))
        lastLayer = layers[len(layers)-1]
    if len(lastLayer) == 0:
        return []
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
    startVertexId = vertToIndex[startVertex]
    currentVertices = [startVertexId]
    distances = np.zeros(len(V), "uint") + sys.maxsize
    distances[startVertexId] = 0
    toVisitVertices = [startVertexId]
    targetVertexId = vertToIndex[targetVertex]
    while not targetVertexId in neverToVisitAsNeighborAgainVertices:
        currentVertices = toVisitVertices.copy()
        for currentVertex in currentVertices:
            neighbors = getNeighbors(currentVertex, connMat)
            if len(neighbors) == 0: #if there's no children or no children without fixed cost, it won't change
                toVisitVertices.remove(currentVertex) # so we don't need to visit the neighbors of this vertex again
                continue # note : a vertex must be in neverToVistiAsNeighborAgain for it to be removed from
            # toVisitVertices.
            for neighbor in neighbors:
                toVisitVertices.append(neighbor)
                distances[neighbor] = min(distances[currentVertex]\
                                            + costMat[currentVertex, neighbor],
                                            distances[neighbor])
                if currentVertex in neverToVisitAsNeighborAgainVertices:
                    edgeVisitMat[currentVertex, neighbor] = True
                    if (edgeVisitMat[:,neighbor]==connMat[:,neighbor]).all(): #if all parent's cost of this 
                        #vertex are locked, then :
                        neverToVisitAsNeighborAgainVertices.append(neighbor) #this vertex cost won't ever get lower
                        connMat[:,neighbor] = False #get neighbors doesn't need to yell this vertex again.
    pathId = djikstraBackTrack(distances, generateConnexityMatrix(g,vertToIndex), costMat, targetVertexId, startVertexId)
    return pathIdToPathVertex(pathId,V) 


def solveType4DjikstraOptimized(g,a,b,ta,to):
    g = constraints.apply_constraints(g,a,b,ta,to)
    a = min(problemSolverBFS.getGraphGeneratedVertices(g,a), key = lambda v : v[1])
    b = max(problemSolverBFS.getGraphGeneratedVertices(g, b), key = lambda v : v[1])
    return djikstra(g,a,b)