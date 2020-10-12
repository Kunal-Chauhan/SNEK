import pygame
import sys
from pygame.locals import *
from tkinter import messagebox, Tk


def DFS_BFS(G, index):
    queue = G.queue
    path = G.path
    end = G.end

    while True:
        if pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        if len(queue) > 0:
            current = queue.pop(-index)

            if current == end:
                temp = current
                while temp.prev:
                    path.append(temp.prev)
                    temp = temp.prev

                G.visualise()
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

        G.visualise()

    while not pygame.event.get(KEYDOWN):
        if pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()


def aStar(G):
    heuristics = lambda a, b: abs(a.x - b.x) + abs(a.y - b.y)

    queue = G.queue
    path = G.path
    end = G.end
    visited = G.visited

    while True:
        if pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        if len(queue) > 0:
            winner = queue[0]
            for i in queue:
                if i.f < winner.f:
                    winner = i

            current = winner

            if current == end:
                temp = current
                while temp.prev:
                    path.append(temp.prev)
                    temp = temp.prev

                G.visualise()
                print("Done")
                break

            queue.remove(current)
            visited.append(current)
            current.visited = True

            for neighbor in current.neighbors:
                if neighbor in visited or neighbor.wall:
                    continue
                tempG = current.g + 1

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
            if sys.platform != 'darwin':
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There was no solution")
            print("no solution")
            break

        G.visualise()

    while not pygame.event.get(KEYDOWN):
        if pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
