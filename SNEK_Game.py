import pygame
import random
import os

pygame.mixer.init()

pygame.init()

# screen dimentions
screen_width = 900
screen_height = 600

# creating window
GameWindow = pygame.display.set_mode((screen_width, screen_height))

# giving title
pygame.display.set_caption("Snake Game")
pygame.display.update()

# Colours
red = (238, 111, 87)
white = (255, 203, 203)
black = (0, 51, 78)
light_blue = (187, 225, 250)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_on_screen(text, colour, x, y):
    screen_text = font.render(text, True, colour)
    GameWindow.blit(screen_text, (x, y))


def plot_snake(GameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(GameWindow, black, [
            x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    pygame.mixer.music.load('progressivehouse2.mp3')
    pygame.mixer.music.play()
    while not exit_game:
        GameWindow.fill(white)
        text_on_screen("Welcome to SNEK", black, 285, 200)
        text_on_screen("Press Spacebar To Play", black, 240, 500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Game_loop()
        pygame.display.update()
        clock.tick(144)

# Game loop


def Game_loop():

    # gamespecific variable
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 15
    velocity_x = 0
    velocity_y = 0
    velocity_value = 2
    food_x = random.randint(20, screen_width/1.5)
    food_y = random.randint(20, screen_height/1.5)
    score = 0
    FPS = 144
    snk_list = []
    snk_length = 1
    pygame.mixer.music.load('Popsoundeffectbottle.mp3')

    if(not os.path.exists("Highscore.txt")):
        with open("Highscore.txt", "w") as f:
            f.write("0")
    with open("Highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:

        if game_over:
            with open("Highscore.txt", "w") as f:
                f.write(str(highscore))

            GameWindow.fill(black)
            text_on_screen("Game Over!Press Enter To Continue",
                           white, 100, 200)
            for event in pygame.event.get():

                # Quitting game event
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Game_loop()

        else:
            for event in pygame.event.get():

                # Quitting game event
                if event.type == pygame.QUIT:
                    exit_game = True

                # arrow key input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_y = 0
                        velocity_x = velocity_value
                    if event.key == pygame.K_LEFT:
                        velocity_y = 0
                        velocity_x = -velocity_value
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -velocity_value
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = velocity_value

            snake_x = snake_x+velocity_x
            snake_y = snake_y+velocity_y

            if abs(snake_x-food_x) < 15 and abs(snake_y-food_y) < 15:
                score = score+10
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snk_length += 15

                if score > int(highscore):
                    highscore = score

            GameWindow.fill(white)
            text_on_screen("Score: " + str(score) +
                           ", Highscore: "+str(highscore), light_blue, 5, 5)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.play()

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.play()

            plot_snake(GameWindow, black, snk_list, snake_size)
            pygame.draw.rect(GameWindow, red, [
                food_x, food_y, snake_size, snake_size])
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit
    quit()


welcome()
