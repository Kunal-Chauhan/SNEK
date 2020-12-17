import pygame
import sys
from pygame.locals import *
from constants import *
from client import SNEKClient


class Cube:
    rows = ROWS
    w = WIDTH

    def __init__(self, start, dirX=1, dirY=0, cubeColor=DARK_BLUE):
        self.pos = start
        self.dirX = dirX
        self.dirY = dirY
        self.color = cubeColor

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

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

    def __iter__(self):
        try:
            return iter(tuple(cube.pos for cube in self.body[1:]))
        except IndexError:
            pass

    def move(self, key=None):
        if not key:
            pass
        elif key == K_LEFT:
            if not (self.dirX == 1 and self.dirY == 0):
                self.dirX = -1
                self.dirY = 0
                self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif key == K_RIGHT:
            if not (self.dirX == -1 and self.dirY == 0):
                self.dirX = 1
                self.dirY = 0
                self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif key == K_UP:
            if not (self.dirX == 0 and self.dirY == 1):
                self.dirX = 0
                self.dirY = -1
                self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        elif key == K_DOWN:
            if not (self.dirX == 0 and self.dirY == -1):
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

    def moveTo(self, point):
        if pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        x, y = point
        dirX = self.dirX = x - self.head.x
        dirY = self.dirY = y - self.head.y
        self.turns[tuple(self.head.pos[:])] = [dirX, dirY]

        for i, c in enumerate(self.body):
            p = tuple(c.pos[:])
            if p in self.turns:
                turn = self.turns[p]
                c.move(*turn)
                if i == len(self.body)-1:
                    self.turns.pop(p)
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

    def removeCube(self, collision_index):
        # self.body.pop(len(self.body)-1)
        i = len(self.body)-1
        while i > collision_index:
            self.body.pop(i)
            i = i-1


class Spot:
    def __init__(self, position):
        self.x, self.y = position
        self.f, self.g, self.h = 0, 0, 0
        self.weight = 1
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        self.offset = 0

    def __call__(self, *args, **kwargs):
        return self.weight

    def __repr__(self):
        return f'{self.x, self.y}, w: {self.weight}'

    @property
    def position(self):
        return self.x, self.y

    def show(self, win, clr, shape=1):
        if self.wall:
            clr = BLACK
        elif clr == PINK:
            clr = (int((11-self.weight) * 0.1 * 255), 203, 203)

        if shape == 1:
            pygame.draw.rect(win, clr, (self.x * W, self.y * H, W - 1, H - 1))
        else:
            pygame.draw.circle(win, clr, (self.x * W + W // 2, self.y * H + H // 2), W // 3)

    def add_neighbors(self, grid, rows=ROWS, columns=COLUMNS):
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < columns - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        # Add Diagonals
        # if self.x < rows - 1 and self.y < columns - 1:
        #     self.neighbors.append(grid[self.x + 1][self.y + 1])
        # if self.x < rows - 1 and self.y > 0:
        #     self.neighbors.append(grid[self.x + 1][self.y - 1])
        # if self.x > 0 and self.y < columns - 1:
        #     self.neighbors.append(grid[self.x - 1][self.y + 1])
        # if self.x > 0 and self.y > 0:
        #     self.neighbors.append(grid[self.x - 1][self.y - 1])

    def reset(self, retainWeight=False, retainWall=False):
        self.f, self.g, self.h = 0, 0, 0
        self.prev = None
        self.visited = False

        if not retainWall:
            self.wall = False
        if not retainWeight:
            self.weight = 1


class Grid:
    def __init__(self, window, start=None, end=None, rows=ROWS, columns=COLUMNS):
        self.win = window
        self.rows = rows
        self.columns = columns

        self.queue = []  # set of open nodes
        self.visited = []  # set of visited nodes
        self.path = []  # shortest path nodes
        self.grid: List[List[Spot]] = []  # all nodes in the grid
        self.snakeBody = []  # for making snake body as walls in CPU mode
        self.walls = []     # spots with infinite weight

        self.weightLimit = -1

        self.start: Spot = start
        self.end: Spot = end

        self._offset = 0

        self.newGrid(start, end)

    def __call__(self, *args, **kwargs):
        grid = tuple([tuple([self.grid[i][j]() for j in range(self.columns)]) for i in range(self.rows)])
        info = {
            "grid": grid,
            "walls": self.walls,
            "snake": self.snakeBody,
            "start": self.start.position,
            "end": self.end.position
        }
        return info

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, new):
        self._offset = new
        for spots in self.grid:
            for spot in spots:
                spot.offset = new

    def newGrid(self, start, end):
        queue = self.queue = []
        grid = self.grid = []
        self.visited = []
        self.path = []

        for i in range(self.rows):
            arr = []
            for j in range(self.columns):
                arr.append(Spot((i, j)))
            self.grid.append(arr)

        for i in range(self.rows):
            for j in range(self.columns):
                grid[i][j].add_neighbors(grid, self.rows, self.columns)

        if start:
            startX, startY = start
            self.start = grid[startX][startY]
            self.start.visited = True
            queue.append(self.start)

        if end:
            endX, endY = end
            self.end = grid[endX][endY]

    def reset(self, start=None, end=None, obstacles=None, retainWeights=False, retainWalls=False):
        self.visited = []
        self.path = []
        self.queue = []
        self.snakeBody = []

        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j].reset(retainWeights, retainWalls)

        if start:
            startX, startY = start
            self.start = self.grid[startX][startY]
            self.start.visited = True

        if end:
            endX, endY = end
            self.end = self.grid[endX][endY]

        if obstacles:
            self.snakeBody = obstacles

        self.queue.append(self.start)

    def visualise(self, updateScreen=True):
        self.win.fill(WHITE)
        start = self.start
        end = self.end

        for i in range(self.rows):
            for j in range(self.columns):
                spot = self.grid[i][j]
                spot.show(self.win, PINK)

                if spot in self.path:
                    spot.show(self.win, LIGHT_BLUE)
                elif spot.visited:
                    spot.show(self.win, GOLDEN)
                if spot in self.queue:
                    spot.show(self.win, CREAM)
                    spot.show(self.win, CREAM, 0)

                # start and end point
                start.show(self.win, DARK_BLUE) if start else ...
                end.show(self.win, RED) if end else ...

        pygame.display.flip() if updateScreen else ...

    def hasStartAndEnd(self):
        return True if self.start and self.end else False

    def clickWall(self, pos, weight=1):
        i = pos[0] // W
        j = (pos[1] - self.offset) // H

        # if j < 0 or self.weightLimit == -1
        if j < 0:
            return

        try:
            if weight == -2:
                self.end = self.grid[i][j]
            elif weight == -1:
                if self.start:
                    self.start.visited = False
                    self.queue.pop()
                self.start = self.grid[i][j]
                self.start.visited = True
                self.queue.append(self.start)
            else:
                if weight == 0:
                    if not self.grid[i][j].wall:
                        self.grid[i][j].wall = True
                        self.walls.append((i, j))
                elif self.grid[i][j].wall:
                    self.grid[i][j].wall = False
                    self.walls.remove((i, j))
                self.grid[i][j].weight = weight
        except IndexError:
            pass


class Multiplayer(SNEKClient):
    def __init__(self, players):
        super(Multiplayer, self).__init__(players)
        self.hp = 20
        self.distance = 0
        self.snakes: Tuple[Snake, ...] = tuple([Snake(GREEN, player["start"]) for player in players])
        self.snacks = tuple([Cube(player["end"], cubeColor=RED) for player in players])

    def run(self):
        pass