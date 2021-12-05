import graphDisplay
import graphReader
import graphPathComputation as gpc
import graphComputePath
import problemSolverBFS as psb

mg,g = graphReader.createMultigraphAndGraphFromFile("graphs/graphEx2.mg")
g2 = psb.removeHighestVertices(g, "a", lambda x : x, 2)
graphDisplay.displayGraph(g2, "g2.png")