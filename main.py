import graphDisplay
import graphReader
import graphPathComputation as gpc
mg,g = graphReader.createMultigraphAndGraphFromFile("graphs/graphEx2.mg")
print(gpc.djikstra(g, ("a",1), ("g",8)))