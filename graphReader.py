import re
"""
Formal types definitions:
a vertex is a string (name)


an edge is (string*string*int*int)
0-Start vertex
1-End vertex
2-Start date
3-Edge duration
"""

vertStrToVertName = re.compile("\S")

def getNonBlankLines(f):
    nonBlankLines = []
    nonBlankLineRegExp = re.compile("\S+")
    for line in f.readlines():
        if nonBlankLineRegExp.match(line):
            nonBlankLines.append(line)
    return nonBlankLines

def getVertexLines(vertexNumber, nonBlankLines):
    vertexLines = []
    for i in range(2,2+vertexNumber):
        vertexLines.append(nonBlankLines[i])
    return vertexLines

def getEdgeLines(vertexNumber, edgeNumber, nonBlankLines):
    edgesLines = []
    for i in range(2+vertexNumber,2+vertexNumber+edgeNumber):
        edgesLines.append(nonBlankLines[i])
    return edgesLines


def strToEdge(toConvert):
    vals = toConvert.split(",")
    if len(vals) != 4:
        print(vals)
        raise Exception("each edge line must contain 3 ',', here the line is", toConvert)
    return vals[0].strip(),vals[1].strip(),int(vals[2]),int(vals[3])


def createMultiGraphFromFile(filepath):
    """
        string->dict(vertex->list(edge)*list(edge))
        Reads the file written as specified in the paper.
        Creates a multigraph dictionnary giving all vertices
        with corresponding outgoing (first list) edges & ingoing (second list) edges.
    """
    nonBlankLines = getNonBlankLines(open(filepath, "r"))
    vertexNb = int(nonBlankLines[0])
    edgeNb = int(nonBlankLines[1])
    
    vertexLines = getVertexLines(vertexNb, nonBlankLines)
    edgesLines = getEdgeLines(vertexNb, edgeNb , nonBlankLines)
    
    #generating edges array
    edges = []
    for edgeLine in edgesLines:
        edges.append(strToEdge(edgeLine))

    #creating the multigraph dictionary
    toRet = {}
    for vertLine in vertexLines:
        vertName = vertStrToVertName.match(vertLine).group()
        outgoingList = []
        ingoingList = []
        for edge in edges:
            if edge[0] == vertName:
                outgoingList.append(edge)
            elif edge[1] == vertName:
                ingoingList.append(edge)
        toRet[vertName] = (outgoingList,ingoingList)
    return toRet




print(createMultiGraphFromFile("graphs/graphEx2.mg"))