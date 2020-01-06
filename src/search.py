import queue
import sys
import config
import heapq

from math import sqrt
from dataclasses import dataclass

# Each cell in the grid represented by a node
@dataclass
class Node:
    color: str = "W"
    parent: tuple = (0, 0)
    g: int = sys.maxsize  # Cost var
    h: int = 0  # Heuristic var
    f: int = 0  # Combined g + h


class Search:
    def __init__(self, object, rows, cols, start, goal):
        self.gridQ = object
        self.goalFound = False
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.matrix = [[Node() for i in range(rows)] for j in range(cols)]

    def setCell(self, x, y, color):
        """Sets cell to a wall in matrix"""
        self.matrix[x][y].g = sys.maxsize
        self.matrix[x][y].color = color

    def in_bounds(self, cur):
        """Check if cell is within bounds of grid and isn't a wall"""
        i, j = cur
        if 0 <= i < self.rows and 0 <= j < self.cols:
            return True
        else:
            return False

    def get_neighbors(self, cur, directions):
        """Returns visitable neighbors as a list"""
        i, j = cur
        if directions == 8:
            #fmt: off
            adj = [(i-1, j), (i-1, j+1), (i, j + 1), (i + 1, j + 1), (i+1, j), (i+1, j-1), (i, j-1), (i-1, j-1),]
        elif directions == 4:
            adj = [(i, j + 1), (i + 1, j), (i, j - 1), (i - 1, j)]

        adj = filter(self.in_bounds, adj)
        return adj

    def get_cost(self, cur, to):
        """Returns cost from one cell to another. Different values for diagonal or straight movement"""
        i1, j1 = cur
        i2, j2 = to
        if abs(i1 - i2) + (j1 - j2) == 1:
            return 1
        else:
            return 1.414

    def bfs(self):
        # Initialize parents of each cell to itself
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j].parent = (i, j)

        # Declare new queue to determine which direction to travel
        bfsQ = queue.Queue()
        bfsQ.put(self.start)
        self.goalFound = False

        # Set start cell to visited. g member variable is being used as an indicator of visited
        # or not visited
        self.matrix[self.start[0]][self.start[1]].g = 0

        while not bfsQ.empty():
            cur = bfsQ.get()

            if cur == self.goal:
                break

            for v in self.get_neighbors(cur, 4):
                i, j = v

                if self.matrix[i][j].color == 'B':
                    continue

                # If g is still maxsize, it hasn't been visited so add this cell to the queue
                if self.matrix[i][j].g == sys.maxsize:
                    bfsQ.put(v)
                    self.matrix[i][j].g = self.matrix[cur[0]][cur[1]].g + 1
                    self.matrix[i][j].parent = cur
                    self.gridQ.put((v[0], v[1], config.green))
                else:
                    self.gridQ.put((v[0], v[1], config.red))

        # Print out path taken to find the goal
        self.backtrack(self.goal)

    def dfs(self):

        # New stack to search via depth first. Start with start node
        dfsStack = queue.LifoQueue()
        dfsStack.put(self.start)
        self.goalFound = False

        # While there are still nodes to process and the goal hasn't been found do
        while not dfsStack.empty() and self.goalFound == False:
            i, j = dfsStack.get()

            # Skip cells that are walls
            if self.matrix[i][j].color == "B":
                continue

            # Set color to processing for entry node
            self.matrix[i][j].color = "G"
            self.gridQ.put((i, j, config.green))

            # Look at each neighbor of current cell
            for v in self.get_neighbors((i, j), 4):
                row = v[0]
                col = v[1]

                # Only add nodes to the stack that haven't been visited yet
                if self.matrix[row][col].color == "W":
                    self.matrix[row][col].parent = (i, j)
                    dfsStack.put((row, col))

                    # Exit early if goal has been found
                    if (row, col) == self.goal:
                        self.goalFound = True
                        break

        self.backtrack(self.goal)

    def a_star(self):
        # New priority queue will be used as open list for A* search. Add start node to queue and declare
        # empty dic for closed list
        priQ = []
        heapq.heapify(priQ)
        heapq.heappush(priQ, (0, self.start))
        closed = {}

        s_i, s_j = self.start
        self.matrix[s_i][s_j].g = 0

        # While the priority queue still has elements to process
        while not len(priQ) == 0:

            # Get the value with the lowest 'f' value and add it to the closed list
            i, j = heapq.heappop(priQ)[1]
            closed[(i, j)] = True

            # Add this node to be colored in on pygame grid
            self.gridQ.put((i, j, config.red))

            # Exit if goal node found
            if (i, j) == self.goal:
                self.goalFound = True
                break

            # Visit 8-directions from current cell (within boundaries)
            for v in self.get_neighbors((i, j), 8):
                row = v[0]
                col = v[1]

                # Skip cell if already processed in closed list or marked as wall
                if (row, col) in closed or self.matrix[row][col].color == "B":
                    continue

                # Calculate the new cost from current cell to next
                n_cost = self.matrix[i][j].g + self.get_cost((i, j), v)
                cur_cost = self.matrix[row][col].g

                # Calculate h and f if not visited yet or new cost is less then the current cost
                if cur_cost == sys.maxsize or n_cost < cur_cost:

                    # Update cost of current cell and calculate h and f
                    self.matrix[row][col].g = n_cost
                    h = self.heuristic((row, col), self.goal)
                    f = n_cost + h

                    # Push this cell onto the priority queue with f as its priority and set parent
                    heapq.heappush(priQ, (f, (row, col)))
                    self.matrix[row][col].parent = (i, j)

                    # Color in cell as being processed
                    self.gridQ.put((row, col, config.green))

        # After A* algorithm has completed, backtrack to the start to highlight the path taken
        self.backtrack(self.goal)

    def heuristic(self, cur, goal):
        # Heuristic for 8-directional diagonal movements
        non_diag = 1
        diag = 1.414
        dx = abs(cur[0] - goal[0])
        dy = abs(cur[1] - goal[1])
        return min(dx, dy) * diag + abs(dx - dy)

    def backtrack(self, cur):
        self.gridQ.put((cur[0], cur[1], config.yellow))
        while cur != self.start:
            cur = self.matrix[cur[0]][cur[1]].parent
            self.gridQ.put((cur[0], cur[1], config.blue))
        self.gridQ.put((cur[0], cur[1], config.yellow))

