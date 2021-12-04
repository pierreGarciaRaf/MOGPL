import pydot
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


def displayGraph(g, saveAs):
    """
        graph->()
        displays the graph given using pydot
    """
    display = pydot.Dot(graph_type='graph')
    _,E = g
    for (frName,frTime),(toName,toTime),cost in E:
        display.add_edge(pydot.Edge(frName + " " + str(frTime),\
                                    toName + " " + str(toTime),\
                                    label = cost))
    extension = saveAs.split(".")[len(saveAs.split("."))-1]
    if extension.upper() == "PNG":
        display.write_png(saveAs)
    else:
        raise Exception("You must save your graph display as a png!")

