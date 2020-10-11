from algorithms import *
from Grid import Grid
from comparisonConstants import *


pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("DFS's Visual")
clock = pygame.time.Clock()


def main():
    grid = Grid(win, (0, 0), (rows // 2, cols // 2))

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
                if event.key == pygame.K_RETURN:
                    aStar(grid)
                    grid.newGrid((0, 0), (rows // 2, cols // 2))

        grid.visualise()


main()
