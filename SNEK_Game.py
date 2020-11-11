import random
import tkinter as tk
from constants import *
from elements import Snake, Cube, Grid
from algorithms import *
from client import SNEKClient
import threading

# For Zen Mode
ZEN_MODE = False

pygame.init()
pygame.mixer.init()

win: pygame.SurfaceType = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("SNEK Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(pygame.font.get_default_font(), 55)


def drawGrid(w, rows, surface):
    sizeBetween = w // rows

    x = 0
    y = 0
    for _ in range(rows):
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, WHITE, (x, 0), (x, w), 1)
        pygame.draw.line(surface, WHITE, (0, y), (w, y), 1)


def _drawObstacle(grid, weight, startEndEditable=True):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                grid.clickWall(pygame.mouse.get_pos(), weight)
            if pygame.mouse.get_pressed()[2]:
                grid.clickWall(pygame.mouse.get_pos())
        if event.type == KEYDOWN:
            if goToMainMenu(event.key):
                return

            if K_0 <= event.key <= K_9:
                weight = event.key - K_0
            elif startEndEditable:
                if event.key == K_s:
                    weight = -1
                elif event.key == K_e:
                    weight = -2
            else:
                return event.key

    return weight


def drawObstacle(grid):
    weight = 0

    while True:
        x = _drawObstacle(grid, weight)
        if x is None:
            return None
        elif -2 <= x <= 9:
            weight = x
        else:
            return x

        grid.visualise()


def redrawWindow(surface, grid=None):
    if grid:
        grid.visualise()
        snek.draw(surface)
        snac.draw(surface)
    else:
        surface.fill(PINK)
        snek.draw(surface)
        snac.draw(surface)
        drawGrid(WIDTH, ROWS, surface)

    pygame.display.update()


def randomPoint(rows=ROWS, cols=COLUMNS, snake=None, walls=()):
    positions = [i.pos for i in snake.body] if snake else []
    positions += list(walls)

    while True:
        x = random.randrange(cols)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    try:
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        root.destroy()
    except tk.TclError as e:
        print("(tkinter), ", e)
    except Exception as e:
        print(e)


def text_on_screen(text, colour, x, y):
    x = (WIDTH // 2 - len(text) * 10) if not x else x
    screen_text = font.render(text, True, colour)
    win.blit(screen_text, (x, y))


snek = Snake(DARK_BLUE, randomPoint())
snac = Cube(randomPoint(snake=snek), cubeColor=RED)


def welcome():
    global ZEN_MODE

    # welcome screen loop
    while True:
        win.fill(PINK)
        text_on_screen("Welcome to SNEK", DARK_BLUE, 185, 200)
        # noinspection SpellCheckingInspection
        text_on_screen("Press 1 To Play", DARK_BLUE, 180, 400)
        text_on_screen("Press 2 for CPU", DARK_BLUE, 180, 450)
        text_on_screen("Press 3 for Algorithm Comparison", DARK_BLUE, 40, 500)
        text_on_screen("Press 4 for Zen Mode", DARK_BLUE, 130, 550)
        text_on_screen("Press 5 for Multiplayer Mode", DARK_BLUE, 60, 600)

        # tracking events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_1:
                    main()
                elif event.key == K_2:
                    CPU()
                elif event.key == K_3:
                    algoHandling()
                elif event.key == K_4:
                    ZEN_MODE = True
                    main()
                elif event.key == K_5:
                    multiplayer()

        pygame.display.update()


def goToMainMenu(key):
    def pause():
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.set_alpha(180)
        bg.fill(DARK_BLUE)
        win.blit(bg, bg.get_rect())

        text_on_screen("GAME PAUSED", PINK, 200, 200)
        text_on_screen("[Y] Exit to Main Menu", PINK, 150, 250)
        text_on_screen("[Q] Quit Program", PINK, 180, 300)
        text_on_screen("Any key to resume...", PINK, 165, 600)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    return event.key

    if key == K_p or key == K_ESCAPE:
        pauseKey = pause()
        while True:
            if pauseKey == K_y:
                snek.reset((10, 10))
                return True
            elif pauseKey == K_q:
                pygame.quit()
                sys.exit()
            else:
                break

    return False


def main():
    global snek, snac, ZEN_MODE

    # noinspection SpellCheckingInspection
    pygame.mixer.music.load('Popsoundeffectbottle.ogg')
    flag = True

    while flag:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if goToMainMenu(event.key):
                    return

                snek.move(event.key)
                flag = False

        if flag:
            snek.move()
        else:
            flag = True

        if snek.body[0].pos == snac.pos:
            snek.addCube()
            snac = Cube(randomPoint(ROWS, snek), cubeColor=RED)

        if ZEN_MODE:
            for x in range(len(snek.body)):
                if snek.body[x].pos in list(map(lambda z: z.pos, snek.body[x + 1:])):
                    snek.removeCube(
                        list(map(lambda z: z.pos, snek.body[x + 1:])).index(snek.body[x].pos))
                    break
        else:
            for x in range(len(snek.body)):
                if snek.body[x].pos in list(map(lambda z: z.pos, snek.body[x + 1:])):
                    win.fill(DARK_BLUE)

                    text_on_screen("Game Over! Your Score: " +
                                   str(len(snek.body)), PINK, 100, 200)
                    pygame.display.update()
                    pygame.mixer.music.play()

                    print('Score: ', len(snek.body))

                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_RETURN:
                                main()

                    if sys.platform != 'darwin':
                        message_box('You Lost!', 'Play again...')
                    print("You LOST!")

                    snek.reset((10, 10))
                    break

        redrawWindow(win)


def CPU():
    # noinspection SpellCheckingInspection
    pygame.mixer.music.load('Popsoundeffectbottle.ogg')
    global snek, snac

    grid = Grid(win, snek.head.pos, snac.pos)

    if drawObstacle(grid) is None:
        return

    while True:
        aStar(grid, visualisePath=False, visualiseEnd=False)
        path = tuple(spot.position for spot in grid.path)

        for p in path:
            clock.tick(50)

            snek.moveTo(p)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if goToMainMenu(event.key):
                        return

            if snek.head.pos == snac.pos:
                snek.addCube()
                snac = Cube(randomPoint(snake=snek, walls=grid.walls), cubeColor=RED)
                grid.reset(snek.head.pos, snac.pos, snek, True)
            redrawWindow(win, grid)


def algoHandling():
    grid = Grid(win)

    while True:
        key = drawObstacle(grid)

        if key is None:
            return

        if not grid.hasStartAndEnd():
            continue
        elif key == K_b:
            DFS_BFS(grid, BFS, visualisePath=True, visualiseEnd=True)
        elif key == K_d:
            DFS_BFS(grid, DFS, True, True)
        elif key == K_a:
            aStar(grid, True, True)
        elif key == K_q:
            grid.reset()
            return
        else:
            continue

        grid.reset(retainWalls=True, retainWeights=True)

        while not pygame.event.get(KEYDOWN) and not pygame.event.get(MOUSEBUTTONDOWN):
            if pygame.event.get(QUIT):
                pygame.quit()
                sys.exit()


def multiplayer():
    global snek, snac
    start = randomPoint(rows=ROWS // 2, snake=snek)
    end = randomPoint(rows=ROWS // 2, snake=snek, walls=(start,))

    surface = pygame.Surface((WIDTH, HEIGHT // 2))
    size: tuple[int, int] = surface.get_size()

    bg = surface, surface.copy()
    players = Grid(bg[0], start, end, columns=ROWS // 2), Grid(bg[1], start, end, columns=ROWS // 2)

    for surf in bg:
        surf.set_alpha(180)
        surf.fill(DARK_BLUE)

    client = SNEKClient([players[0](), players[1]()])
    playerID: int = client.playerID
    enemyID = (playerID+1) % 2

    # this array will decide the Y position of grid for every (in our case, two) player
    offset = 0, size[1]
    players[playerID].offset, players[enemyID].offset = offset[playerID], offset[enemyID]
    weight = 0

    def drawObstacleMultiplayer():
        nonlocal weight

        x = _drawObstacle(players[playerID], weight, startEndEditable=False)
        if x is None:
            return 0
        elif -2 <= x <= 9:
            weight = x

    def fetchData():
        while True:
            client.updatePlayers()
            grid = client.players[enemyID]["grid"]
            for m, spots in enumerate(players[enemyID].grid):
                for n, spot in enumerate(spots):
                    spot.weight = grid[m][n]

            players[enemyID].snakeBody = client.players[enemyID]["snake"]
            players[enemyID].walls = client.players[enemyID]["walls"]

    client.updatePlayers()
    start = client.players[enemyID]["start"]
    end = client.players[enemyID]["end"]

    for player in players:
        player.end = player.grid[end[0]][end[1]]
        player.start.visited = False
        player.queue.pop()
        player.start = player.grid[start[0]][start[1]]
        player.start.visited = True
        player.queue.append(player.start)

    thread = threading.Thread(target=fetchData)
    thread.daemon = True
    thread.start()

    while True:
        win.fill(PINK)

        if client.state[enemyID] != State.run:
            win.blit(bg[enemyID], (0, offset[enemyID]))
            text_on_screen(str(client.state[enemyID]), PINK, None, 150 + offset[enemyID])

        if client.state[playerID] == State.busy and client.state[enemyID] == State.busy:
            if drawObstacleMultiplayer():
                return

        players[playerID].visualise(False)
        win.blit(bg[playerID], (0, offset[playerID]))

        for i in range(2):
            # partition
            pygame.draw.line(win, WHITE, (0, offset[i]), (WIDTH, offset[i]), 3)

        pygame.display.flip()


welcome()
