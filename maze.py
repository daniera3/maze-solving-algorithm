###### Import
import sys
from collections import defaultdict


##### Define
Wall = 'W'
Start = 'S'
Goal = 'G'
Beyond = 'B'
Path = 'P'


####### Read from file to array
def readFile(fileName):
    # Read from file per line
    with open(fileName, "r") as f:
        maze = f.readlines()

    #Split lines by char 
    maze = list(map(lambda line: [char for char in line], maze))
    #Delete '\n' from lines
    maze=[line[:len(line)-1]if line[-1] == '\n' else line for line in maze ]
    return maze


###### Write to file the solution of the maze in an array format
def writeFile(fileName, maze):
    with open(fileName, 'w') as f:
        for item in maze:  
            f.write("%s\n" % item)


# This class represents a directed graph
# using adjacency list representation
class Graph:

    # Constructor
    def __init__(self):
        # default dictionary to store the graph
        self.graph = defaultdict(set)

    # Method to print the graph
    def __repr__(self):
        return str(self.graph)

    # Method  to add a vertex to the graph
    def addvertex(self, u):
        self.graph[u]

    # Method  to add an edge to the graph
    def addEdge(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)

    # Method to get the best path in the graph
    def bfs_path(self, start, goal):
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            for next in self.graph[vertex] - set(path):
                if next == goal:
                    return path + [next]
                else:
                    queue.append((next, path + [next]))

# Function to map the maze into a graph
def mapping(maze):
    graph = Graph()
    start = None
    goal = None
    lastRow = len(maze)-1
    if maze:
        lastCol = len(maze[0])-1
    for i in range(lastRow+1):
        for j in range(lastCol+1):
            if maze[i][j] == Start:
                if start:
                    raise ValueError('Sorry,you have more than one starting point in the maze')
                start = (i, j)
                graph.addvertex(start)
            elif maze[i][j] == Goal:
                if goal:
                    raise ValueError('Sorry,you have more than one starting point in the maze')
                goal = (i, j)
                graph.addvertex(goal)
            elif maze[i][j] == Beyond:
                if i > 0 and (maze[i-1][j] == Beyond or maze[i-1][j] == Goal or maze[i-1][j] == Start):
                    graph.addEdge((i, j), (i-1, j))
                if i < lastRow and (maze[i+1][j] == Beyond or maze[i+1][j] == Goal or maze[i+1][j] == Start):
                    graph.addEdge((i, j), (i+1, j))
                if j > 0 and (maze[i][j-1] == Beyond or maze[i][j-1] == Goal or maze[i][j-1] == Start):
                    graph.addEdge((i, j), (i, j-1))
                if j < lastCol and (maze[i][j+1] == Beyond or maze[i][j+1] == Goal or maze[i][j+1] == Start):
                    graph.addEdge((i, j), (i, j+1))
    return(graph, start, goal)

#Function to solve the maze 
def getPath(graph, maze): 
    graph, start, goal = graph[0], graph[1], graph[2]
    if not start:
        raise ValueError('Sorry,missing a starting point in the maze')
    if not goal:
        raise ValueError('Sorry,missing a goal point in the maze')
    path = graph.bfs_path(start, goal)
    if not path:
        raise ValueError('Sorry,can\'t find a path to solve this maze')
    for index in path:
        i, j = index[0], index[1]
        if maze[i][j] == Beyond:
            maze[i][j] = Path
    return maze

#Main function
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Sorry,missing arguments. You need to enter 2 arguments (input and output files)")
        print("Example for bash :$ python maze.py input1.txt output.txt")
        exit(1)
    else:
        try:
            maze = readFile(sys.argv[1])
            graph = mapping(maze)
            solution = getPath(graph, maze)
            writeFile(sys.argv[2], solution)
        except ValueError as error:
            print(repr(error))
            exit(1)

