###### Import
import sys
from collections import defaultdict


##### Define
Well = 'W'
Start = 'S'
Goal = 'G'
Beyond = 'B'
Path = 'P'


####### Read from file to arry
def readFile(fileName):
    # Read from file par lane
    with open(fileName, "r") as f:
        maze = f.readlines()

    #Split lanes per char 
    maze = list(map(lambda lane: [char for char in lane], maze))
    #Delete '\n' from lanes
    maze=[lane[:len(lane)-1]if lane[-1] == '\n' else lane for lane in maze ]
    return maze


###### Write to file solution of maze arry format
def writeFile(fileName, maze):
    with open(fileName, 'w') as f:
        for item in maze:  
            f.write("%s\n" % item)


# This class represents a directed graph
# using adjacency list representation
class Graph:

    # Constructor
    def __init__(self):
        # default dictionary to store graph
        self.graph = defaultdict(set)

    # Method for print graph
    def __repr__(self):
        return str(self.graph)

    # Method  to add an vertice to graph
    def addVertice(self, u):
        self.graph[u]

    # Method  to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)

    # Method to get a bast path of graph
    def bfs_path(self, start, goal):
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            for next in self.graph[vertex] - set(path):
                if next == goal:
                    return path + [next]
                else:
                    queue.append((next, path + [next]))

# Function maping a maze to graph
def maping(maze):
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
                    raise ValueError('sorry,you have more one start point in maze')
                start = (i, j)
                graph.addVertice(start)
            elif maze[i][j] == Goal:
                if goal:
                    raise ValueError('sorry,you have more one start point in maze')
                goal = (i, j)
                graph.addVertice(goal)
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

#Function give a solution to maze 
def getPath(graph, maze): 
    graph, start, goal = graph[0], graph[1], graph[2]
    if not start:
        raise ValueError('sorry,missing a start point in maze')
    if not goal:
        raise ValueError('sorry,missing a goal point in maze')
    path = graph.bfs_path(start, goal)
    if not path:
        raise ValueError('sorry,can\'t find path solving this maze')
    for index in path:
        i, j = index[0], index[1]
        if maze[i][j] == Beyond:
            maze[i][j] = Path
    return maze

#Main function
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("sorry,missing args you need enter 2 args (input and output files)")
        print("example for bash :$ python maze.py input1.txt output.txt")
        exit(1)
    else:
        try:
            maze = readFile(sys.argv[1])
            graph = maping(maze)
            solution = getPath(graph, maze)
            writeFile(sys.argv[2], solution)
        except ValueError as error:
            print(repr(error))
            exit(1)

