import pygame
from comparisonConstants import *


class Spot:
    def __init__(self, position):
        self.x, self.y = position
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False

    @property
    def position(self):
        return self.x, self.y

    def show(self, win, col, shape=1):
        if self.wall:
            col = black
        if shape == 1:
            pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
        else:
            pygame.draw.circle(win, col, (self.x * w + w // 2, self.y * h + h // 2), w // 3)

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        # Add Diagonals
        # if self.x < cols - 1 and self.y < rows - 1:
        #     self.neighbors.append(grid[self.x + 1][self.y + 1])
        # if self.x < cols - 1 and self.y > 0:
        #     self.neighbors.append(grid[self.x + 1][self.y - 1])
        # if self.x > 0 and self.y < rows - 1:
        #     self.neighbors.append(grid[self.x - 1][self.y + 1])
        # if self.x > 0 and self.y > 0:
        #     self.neighbors.append(grid[self.x - 1][self.y - 1])


class Grid:
    def __init__(self, window, start, end):
        self.win = window

        self.queue = []         # set of open nodes
        self.visited = []       # set of visited nodes
        self.path = []          # shortest path nodes
        self.grid = []          # all nodes in the grid

        self.start = self.end = None

        self.newGrid(start, end)
    
    def newGrid(self, start, end):
        queue = self.queue = []
        grid = self.grid = []
        self.visited = []
        self.path = []

        for i in range(cols):
            arr = []
            for j in range(rows):
                arr.append(Spot((i, j)))
            self.grid.append(arr)

        for i in range(cols):
            for j in range(rows):
                grid[i][j].add_neighbors(grid)

        startX, startY = start
        endX, endY = end

        self.start = grid[startX][startY]
        self.end = grid[endX][endY]

        self.start.visited = True

        queue.append(self.start)

    def visualise(self):
        self.win.fill(white)
        start = self.start
        end = self.end

        for i in range(cols):
            for j in range(rows):
                spot = self.grid[i][j]
                spot.show(self.win, pink)

                if spot in self.path:
                    spot.show(self.win, light_blue)
                elif spot.visited:
                    spot.show(self.win, green)
                if spot in self.queue:
                    spot.show(self.win, blue)
                    spot.show(self.win, dark_blue, 0)

                # start and end point
                start.show(self.win, dark_blue)
                end.show(self.win, red)

        pygame.display.flip()
    
    def clickWall(self, pos, state):
        i = pos[0] // w
        j = pos[1] // h
        self.grid[i][j].wall = state

