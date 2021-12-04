import graphDisplay
import graphReader

mg,g = graphReader.createMultigraphAndGraphFromFile("graphs/graphEx2.mg")
graphDisplay.displayGraph(g, "graphEx2.png")