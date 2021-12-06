import gurobipy as grb
import problemSolverBFS as psb
import graphReader

def getIncomingEdges(E,vertex):
    toRet = []
    for e in E:
        if e[1] == vertex:
            toRet.append(e)
    return toRet

def getFlowInSum(E,vertex,edgeToVar):
    return sum(edgeToVar[e] for e in getIncomingEdges(E,vertex))

def getExcitingEdges(E,vertex):
    toRet = []
    for e in E:
        if e[0] == vertex:
            toRet.append(e)
    return toRet


def getFlowOutSum(E,vertex,edgeToVar):
    return sum(edgeToVar[e] for e in getExcitingEdges(E,vertex))

def edgeToStr(e):
    fr,to,cs = e
    return fr[0]+str(fr[1])+" "+to[0]+str(to[1])+" @"+str(cs)


def writeLpType4(g, startVertexName, endVertexName):
    m = grb.Model("graphSolver")
    V,E = g
    edgeToVar = {}

    #       First we declare the variables:
    #is this edge used var declaration:
    for e in E:
        edgeToVar[e] = m.addVar(vtype = grb.GRB.BINARY, name = edgeToStr(e))
    
    #       Secondly the constraints :
    #start constaint:
    startVert = min(psb.getGraphGeneratedVertices(g,startVertexName), key = lambda v : v[1])
    m.addConstr(getFlowOutSum(E,startVert,edgeToVar) - getFlowInSum(E,startVert,edgeToVar)== 1)
    #end constraint:
    endVert = min(psb.getGraphGeneratedVertices(g,endVertexName), key = lambda v : -v[1])
    m.addConstr(getFlowOutSum(E,endVert,edgeToVar) - getFlowInSum(E,endVert,edgeToVar)== -1)
    #other vertex constraints:
    for v in V:
        if v == startVert or v == endVert:
            continue
        m.addConstr(getFlowOutSum(E,v,edgeToVar) - getFlowInSum(E,v,edgeToVar)== 0)
    
    #       Then we declare the objective function:
    obj = grb.LinExpr()
    for e in E:
        if e[2] >0:
            obj += edgeToVar[e]*e[2]
    m.setObjective(obj, grb.GRB.MINIMIZE)

    m.update()
    return m,edgeToVar


def resolvePL(model,edgeToVar):
    model.optimize()
    path = []
    cost = 0
    for edge in sorted(edgeToVar.keys(), key = lambda e : e[0][1]):
        if edgeToVar[edge].x:
            path.append(edge[0])
            cost += edge[2]
    return path,cost
    

