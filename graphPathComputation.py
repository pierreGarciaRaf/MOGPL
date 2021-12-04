import numpy as np
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
    toKeepFromA = np.zeros(len(setA),"bool")
    for b in setB:
        toKeepFromA += np.vectorize(lambda x : x == b)(setA)
    return setA[toKeepFromA]

def bfs(g, startVertex, targetVertex):
    """
        graph*vertex*vertex -> list(narray(int))
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
            print(neighbors)
            print(np.vectorize(lambda x : V[x])(neighbors))
            
            for layerIdx in range(len(layers)-1):
                neighbors = substractSets(neighbors, layers[layerIdx])
            print(neighbors)
            newLayer = np.concatenate(newLayer,neighbors)
        
        layers.append(newLayer)
        print(layers)
        lastLayer = layers[len(layers)-1]
        input()
    return layers


    