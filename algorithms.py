import pygame
import sys
from pygame.locals import *
from tkinter import messagebox, Tk


def DFS_BFS(G, index, visualisePath=False, visualiseEnd=False):
    queue = G.queue
    path = G.path
    end = G.end

    while True:
        if not pygame.display.get_active():
            return
        elif pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        if len(queue) > 0:
            current = queue.pop(-index)

            if current == end:
                temp = current
                while temp.prev:
                    path.append(temp.prev)
                    temp = temp.prev

                G.visualise() if visualiseEnd else ...
                print("Done")
                break

            for i in current.neighbors:
                if not i.visited and not i.wall:
                    i.visited = True
                    i.prev = current
                    queue.append(i)
        else:
            if sys.platform != 'darwin':
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There was no solution")
            print("no solution")
            break

        G.visualise() if visualisePath else ...


def aStar(G, visualisePath=False, visualiseEnd=False):
    def heuristics(a, b): return abs(a.x - b.x) + abs(a.y - b.y)

    queue = G.queue
    path = G.path
    end = G.end
    visited = G.visited
    snakeBody = G.snakeBody

    while True:
        if not pygame.display.get_active():
            return
        elif pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        if len(queue) > 0:
            winner = queue[0]
            for i in queue:
                if i.f < winner.f:
                    winner = i

            current = winner

            if current == end:
                while current.prev:
                    path.append(current)
                    current = current.prev

                path.reverse()
                G.visualise() if visualiseEnd else ...
                break

            queue.remove(current)
            visited.append(current)
            current.visited = True

            for neighbor in current.neighbors:
                if neighbor.visited or neighbor.wall or neighbor.position in snakeBody:
                    continue
                tempG = current.g + neighbor.weight

                newPath = False
                if neighbor in queue:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                        newPath = True
                else:
                    neighbor.g = tempG
                    newPath = True
                    queue.append(neighbor)

                if newPath:
                    neighbor.H = heuristics(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.H
                    neighbor.prev = current

        else:
            return False
            """if sys.platform != 'darwin':
                print("NO SOLUTION FOUND")
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There was no solution")
            break"""

        G.visualise() if visualisePath else ...
