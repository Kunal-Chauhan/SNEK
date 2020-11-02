# under astar
print(snek.head.pos[0], snek.head.pos[1])
# in cpu if else
else:
            print("dance")
            x = snek.head.pos[0]
            y = snek.head.pos[1]
            clock.tick(50)

            if (x+1 < COLUMNS) and ((x+1, y) not in grid.snakeBody) and ((x+1, y) not in grid.walls):
                print("a")
                snek.moveTo((x+1, y))
                grid.reset(snek.head.pos, snack.pos, snek, True)

            elif (x-1 > -1) and ((x-1, y) not in grid.snakeBody) and ((x+1, y) not in grid.walls):
                print("b")
                snek.moveTo((x-1, y))
                grid.reset(snek.head.pos, snack.pos, snek, True)

            elif (y+1 < ROWS) and ((x, y+1) not in grid.snakeBody) and ((x+1, y) not in grid.walls):
                print("c")
                snek.moveTo((x, y+1))
                grid.reset(snek.head.pos, snack.pos, snek, True)

            elif (y-1 > -1) and ((x, y-1) not in grid.snakeBody) and ((x+1, y) not in grid.walls):
                print("d")
                snek.moveTo((x, y-1))
                grid.reset(snek.head.pos, snack.pos, snek, True)

            else:
                print("BREAKDOWN")
                break

            if pygame.event.get(KEYDOWN):
                keys = pygame.key.get_pressed()

                if goToMainMenu(keys):
                    return

            if snek.head.pos == snack.pos:
                snek.addCube()
                snack = Cube(randomSnack(
                    ROWS, snek, grid.walls), cubeColor=RED)
                grid.reset(snek.head.pos, snack.pos, snek, True)

            redrawWindow(win, grid)

# in ALGO
 else:
            return False
            """if sys.platform != 'darwin':
                print("NO SOLUTION FOUND")
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There was no solution")
            break"""
