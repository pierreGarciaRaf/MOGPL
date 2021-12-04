import graphDisplay
import graphReader
import graphPathComputation as gpc
mg,g = graphReader.createMultigraphAndGraphFromFile("graphs/graphEx2.mg")
print(gpc.bfs(g, ("a",1), ("c",3)))