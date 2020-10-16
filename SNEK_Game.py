import random
import tkinter as tk
from constants import *
from Elements import Snake, Cube, Grid
from algorithms import *

# For Zen Mode
ZEN_MODE = False

pygame.init()
pygame.mixer.init()

win = pygame.display.set_mode((WIDTH, WIDTH))
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


def drawObstacle(grid):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    grid.clickWall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed()[2]:
                    grid.clickWall(pygame.mouse.get_pos(), False)
            if event.type == KEYDOWN:
                return pygame.key.get_pressed()

        grid.visualise()


def redrawWindow(surface, grid=None):
    if grid:
        grid.visualise()
        snek.draw(surface)
        snack.draw(surface)
    else:
        surface.fill(PINK)
        snek.draw(surface)
        snack.draw(surface)
        drawGrid(WIDTH, ROWS, surface)

    pygame.display.update()


def randomSnack(rows, item, walls=()):
    positions = item.body + list(walls)

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return tuple([x, y])


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
    screen_text = font.render(text, True, colour)
    win.blit(screen_text, (x, y))


snek = Snake(DARK_BLUE, (10, 10))
snack = Cube(randomSnack(ROWS, snek), cubeColor=RED)


def welcome():
    global ZEN_MODE
    # loading and playing music
    # noinspection SpellCheckingInspection
    # pygame.mixer.music.load('progressivehouse2.ogg')
    # pygame.mixer.music.play()

    # welcome screen loop
    while True:
        win.fill(PINK)
        text_on_screen("Welcome to SNEK", DARK_BLUE, 185, 200)
        # noinspection SpellCheckingInspection
        text_on_screen("Press 1 To Play", DARK_BLUE, 180, 400)
        text_on_screen("Press 2 for CPU", DARK_BLUE, 180, 450)
        text_on_screen("Press 3 for Algorithm Comparison", DARK_BLUE, 40, 500)
        text_on_screen("Press 4 for Zen Mode", DARK_BLUE, 130, 550)

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

        pygame.display.update()


def isPaused(keys):
    if keys[K_p] or keys[K_ESCAPE]:
        pauseKeys = pause()
        while True:
            if pauseKeys[K_y]:
                snek.reset((10, 10))
                return
            elif pauseKeys[K_q]:
                pygame.quit()
                sys.exit()
            else:
                break


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
                return pygame.key.get_pressed()


def main():
    global snek, snack, ZEN_MODE

    # noinspection SpellCheckingInspection
    pygame.mixer.music.load('Popsoundeffectbottle.ogg')
    flag = True

    while flag:
        clock.tick(10)

        if pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()

        if pygame.event.get(KEYDOWN):
            keys = pygame.key.get_pressed()
            snek.move(keys)

            isPaused(keys)
        else:
            snek.move()

        if snek.body[0].pos == snack.pos:
            snek.addCube()
            snack = Cube(randomSnack(ROWS, snek), cubeColor=RED)

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
    global snek, snack

    snek = Snake(DARK_BLUE, (10, 10))
    snack = Cube(randomSnack(ROWS, snek), cubeColor=RED)

    grid = Grid(win, (10, 10), snack.pos)

    drawObstacle(grid)

    while True:
        aStar(grid, visualisePath=False, visualiseEnd=False)
        path = tuple(spot.position for spot in grid.path)

        for p in path:
            clock.tick(10)

            snek.moveTo(p)

            if pygame.event.get(KEYDOWN):
                keys = pygame.key.get_pressed()

                isPaused(keys)

            if snek.head.pos == snack.pos:
                snek.addCube()
                snack = Cube(randomSnack(ROWS, snek), cubeColor=RED)
                grid.reset(snek.head.pos, snack.pos, snek, True)
            redrawWindow(win, grid)


def algoHandling():
    grid = Grid(win, (0, 0), (ROWS // 2, COLUMNS // 2))

    while True:
        key = drawObstacle(grid)

        isPaused(key)

        if key[K_b]:
            DFS_BFS(grid, BFS, visualisePath=True, visualiseEnd=True)
        elif key[K_d]:
            DFS_BFS(grid, DFS, True, True)
        elif key[K_a]:
            aStar(grid, True, True)
        elif key[K_q]:
            grid.reset((0, 0), (ROWS // 2, COLUMNS // 2))
            return
        else:
            continue

        grid.reset((0, 0), (ROWS // 2, COLUMNS // 2))

        while not pygame.event.get(KEYDOWN) and not pygame.event.get(MOUSEBUTTONDOWN):
            if pygame.event.get(QUIT):
                pygame.quit()
                sys.exit()


welcome()
