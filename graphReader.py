import re
"""
Formal types definitions:
mgVertex := string (name)


mgEdge := mgVertex*mgVertex*int*int
0-Start vertex
1-End vertex
2-Start date
3-Edge duration

vertex := string*int
0-Name
1-Time


edge := vertex*vertex*int
0-Start vertex
1-End vertex
2-Cost

multigraph := dict(mgVertex->list(mgEdge)*list(mgEdge))
Each mgVertex has 2 list of edges.
First list : every multigraph edges (mgEdge) pointing to the mgVertex
Second list : every multigraph edges (mgEdge) starting from this mgVertex

in&out := dict(mgVertex->list(vertex)*list(vertex))
defined in the subject

graph := list(vertex)*list(edge)
"""

vertStrToVertName = re.compile("\S")

def getNonBlankLines(lines):
    nonBlankLines = []
    nonBlankLineRegExp = re.compile("\S+")
    for line in lines:
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


def createMultiGraphFromLineArray(lineArray):
    """
        list(string)->multigraph
        Reads the file written as specified in the paper.
        Creates a multigraph
    """
    nonBlankLines = getNonBlankLines(lineArray)
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
        toRet[vertName] = (ingoingList,outgoingList)
    return toRet


def generateInAndOut(multigraph):
    """
        multigraph->in&out
        generates in & out array as defined in the paper
    """
    inAndOut = {}
    for vertex in multigraph.keys():
        
        
        ingoing,outgoing = multigraph[vertex]
        vin = []
        for edge in ingoing:
            _,_,t,dt = edge
            if not (vertex,t+dt) in vin:
                vin.append((vertex,t+dt))
        
        vout =[]
        for edge in outgoing:
            _,_,t,_ = edge
            if not (vertex,t) in vout:
                vout.append((vertex,t))
        inAndOut[vertex] = vin,vout
    return inAndOut

def mergeSets(setA,setB):
    """
        list(a)*list(a)->list(a)

        merges the two lists with no repetition.
        (Assuming there is no repetition in both lists)
    """
    toRet = []
    for a in setA:
        toRet.append(a)
    for b in setB:
        if not b in setA:
            toRet.append(b)
    return toRet

def generateTildeGraph(multigraph, inAndOut):
    """
        multigraph*in&out->graph
        using the multigraph and it's inAndOut array, generates the associated pondered graph.
    """
    V = []
    E = []
    for mgVertex in inAndOut.keys():
        inSet,outSet = inAndOut[mgVertex]
        linkedSet = sorted(mergeSets(inSet,outSet), key = lambda x : x[1])
        for startVertIndex in range(len(linkedSet)-1):
            E.append((  linkedSet[startVertIndex],
                        linkedSet[startVertIndex+1],0))
        V+= linkedSet
        _,outgoing = multigraph[mgVertex]

        for _,endmgV,t,dt in outgoing:
            E.append(((mgVertex, t),(endmgV, t+dt), dt))
        
    return V,E



def createMultigraphAndGraphFromLineArray(lineArray):
    """
        list(string)->multigraph*graph
        creates a graph
    """
    mg = createMultiGraphFromLineArray(lineArray)
    iao = generateInAndOut(mg)
    V,E = generateTildeGraph(mg, iao)
    return mg, (V, E)

def createMultigraphAndGraphFromFile(filePath):
    return createMultigraphAndGraphFromLineArray(open(filePath,"r").readlines())


def createMultigraphAndGraphFromTerminal():
    vertNb = raw_input("enter the number of vertices of your graph : ")
    edgesNb = raw_input("enter the number of edges of your graph : ")
    print("now enter your vertices and edges, (begin with vertices)")
    lines = [vertNb, edgesNb]
    i = 0
    while i < int(vertNb)+int(edgesNb):
        inp = raw_input()
        if vertStrToVertName.match(inp):
            i += 1
        lines.append(inp)
    return createMultigraphAndGraphFromLineArray(lines)

mg, (V, E) = createMultigraphAndGraphFromFile("graphs/graphEx1.mg")

print("mg = ")
print(mg)
print("V = ")
print(V)
print("E = ")
print(E)
