import graphDisplay
import graphReader
import graphPathComputation as gpc
import graphComputePath

mg,g = graphReader.createMultigraphAndGraphFromFile("graphs/graphEx2.mg")
print(gpc.djikstra(g, ("a",1), ("g",8)))

#path_type_1 = graphComputePath.type1_dijkstra(g, 'a', 'f', 2, 7)
#path_type_2 = graphComputePath.type2_dijkstra(g, 'a', 'f', 2, 7)
#path_type_3 = graphComputePath.type3_dijkstra(g, 'a', 'f', 2, 7)
path_type_4 = graphComputePath.type4_dijkstra(g, 'a', 'f', 2, 7)
#print(path_type_1)
#print(path_type_2)
#print(path_type_3)
print(path_type_4)
