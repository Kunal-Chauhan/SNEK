import random
import pygame
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox
import sys
from constants import *
from Elements import Snake, Cube


pygame.init()
pygame.mixer.init()

win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("SNEK Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(pygame.font.get_default_font(), 55)

snek: Snake
snack: Cube


def drawGrid(w, rows, surface):
    sizeBetween = w // rows

    x = 0
    y = 0
    for _ in range(rows):
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, WHITE, (x, 0), (x, w), 1)
        pygame.draw.line(surface, WHITE, (0, y), (w, y), 1)


def redrawWindow(surface):
    surface.fill(PINK)
    snek.draw(surface)
    snack.draw(surface)
    drawGrid(WIDTH, ROWS, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

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


def welcome():
    # loading and playing music
    pygame.mixer.music.load('progressivehouse2.ogg')
    pygame.mixer.music.play()

    # welcome screen loop
    while True:
        win.fill(PINK)
        text_on_screen("Welcome to SNEK", BLUE, 185, 200)
        text_on_screen("Press Spacebar To Play", BLUE, 140, 500)
        # tracking events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    main()

        pygame.display.update()


def main():
    global snek, snack

    snek = Snake(BLUE, (10, 10))
    snack = Cube(randomSnack(ROWS, snek), cubeColor=RED)

    pygame.mixer.music.load('Popsoundeffectbottle.ogg')
    flag = True

    while flag:
        clock.tick(10)

        snek.move()

        if snek.body[0].pos == snack.pos:
            snek.addCube()
            snack = Cube(randomSnack(ROWS, snek), cubeColor=RED)

        for x in range(len(snek.body)):
            if snek.body[x].pos in list(map(lambda z: z.pos, snek.body[x + 1:])):
                win.fill(BLUE)

                text_on_screen("Game Over! Your Score: " + str(len(snek.body)), PINK, 100, 200)
                pygame.display.update()
                pygame.mixer.music.play()

                print('Score: ', len(snek.body))

                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            main()

                message_box('You Lost!', 'Play again...')

                snek.reset((10, 10))
                break

        redrawWindow(win)


welcome()
