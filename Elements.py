import pygame
import sys
from pygame.locals import *
from constants import *


class Cube:
    rows = ROWS
    w = WIDTH

    def __init__(self, start, dirX=1, dirY=0, cubeColor=BLUE):
        self.pos = start
        self.dirX = dirX
        self.dirY = dirY
        self.color = cubeColor

    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:
            centre = dis//2
            radius = 3

            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)

            pygame.draw.circle(surface, BLACK, circleMiddle, radius)
            pygame.draw.circle(surface, BLACK, circleMiddle2, radius)


class Snake:
    body = []
    turns = {}

    def __init__(self, snekColor, pos):
        self.color = snekColor
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirX = 0
        self.dirY = 1

    def move(self):
        if pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.dirX = -1
            self.dirY = 0
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif keys[K_RIGHT]:
            self.dirX = 1
            self.dirY = 0
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif keys[K_UP]:
            self.dirX = 0
            self.dirY = -1
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif keys[K_DOWN]:
            self.dirX = 0
            self.dirY = 1
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirX == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirX == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirY == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dirX, c.dirY)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirX = 0
        self.dirY = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirX, tail.dirY

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirX = dx
        self.body[-1].dirY = dy

    def draw(self, surface):
        self.body[0].draw(surface, True)

        for c in self.body[1:]:
            c.draw(surface)
