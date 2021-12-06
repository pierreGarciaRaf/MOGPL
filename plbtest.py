import graphReader
from toPLB import *



mg,g = graphReader.createMultigraphAndGraphFromFile("graphs/graphEx2.mg")
model,edgeToVar = writeLpType4(g, "a", "f")
path, cost = resolvePL(model, edgeToVar)
print(path)
print(cost)