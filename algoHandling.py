from algorithms import *
from Elements import Grid
from constants import *


pygame.init()

win = pygame.display.set_mode(SIZE)
pygame.display.set_caption("DFS's Visual")
clock = pygame.time.Clock()


def main():
    grid = Grid(win, (0, 0), (ROWS // 2, COLUMNS // 2))

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
                if event.key == K_b:
                    DFS_BFS(grid, BFS, visualisePath=False, visualiseEnd=True)
                elif event.key == K_d:
                    DFS_BFS(grid, DFS, False, True)
                elif event.key == K_a:
                    aStar(grid, False, True)
                else:
                    continue

                grid.newGrid((0, 0), (ROWS // 2, COLUMNS // 2))
                while not pygame.event.get(KEYDOWN):
                    if pygame.event.get(QUIT):
                        pygame.quit()
                        sys.exit()

        grid.visualise()


main()
