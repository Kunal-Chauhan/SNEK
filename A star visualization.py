import pygame
import sys
import random
import math
from tkinter import messagebox, Tk

# Colours
red = (238, 111, 87)
white = (255, 203, 203)
black = (0, 51, 78)
light_blue = (187, 225, 250)

size = (width, height) = 700, 700

pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("a star visual")

clock = pygame.time.Clock()

cols, rows = 20, 20


grid = []
openSet, closeSet = [], []
path = []

w = width//cols
h = height//rows


class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True

    def show(self, win, col):
        if self.wall == True:
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        # Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1])


def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state


def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h


def heuristics(a, b):
    return (abs(a.x - b.x) + abs(a.y - b.y))


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

start = grid[0][0]
end = grid[cols//2][rows//2]

openSet.append(start)


def close():
    pygame.quit()
    sys.exit()


def main():
    flag = False
    noflag = True
    startflag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(0):
                    clickWall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed(2):
                    clickWall(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True

        if startflag:
            if len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f:
                        winner = i

                current = openSet[winner]

                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue

                if flag == False:
                    openSet.remove(current)
                    closeSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in closeSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor)

                        if newPath:
                            neighbor.h = heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current

            else:
                if noflag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution")
                    noflag = False

        win.fill((255, 255, 255))
        for i in range(cols):
            for j in range(rows):
                spot = grid[j][i]
                spot.show(win, white)
                if flag and spot in path:
                    spot.show(win, light_blue)
                elif spot in closeSet:
                    spot.show(win, (39, 174, 96))
                elif spot in openSet:
                    spot.show(win, (252, 166, 82))
                try:
                    if spot == end:
                        spot.show(win, red)
                    if spot == start:
                        spot.show(win, black)
                except Exception:
                    pass

        pygame.display.flip()


main()