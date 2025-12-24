import pygame
import random
import copy

# Utility Functions
def loadImages(path, size):
    """Load an image into the game, and scale the image"""

    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, size)

    return img

# Classes
class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100,800)) # find a more optimal screen size
        pygame.display.set_caption('Othello')

        self.columns = 8
        self.rows = 8

        self.grid = Board(self.rows, self.columns, (80, 80), self)

        self.RUN = True

    def run(self):
        while self.RUN:
            self.input()
            self.update()
            self.draw()

    def input(self): # overwriting an in-built function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.printGameLogicBoard()


    def update(self):
        pass

    def draw(self):
        self.screen.fill((0,0,0))

        pygame.display.update()

class Board:
    def __init__(self, rows , columns, size, main):
        self.GAME = main
        self.y = rows
        self.x = columns
        self.size = size
        self.whitedisc = loadImages('assets/WhiteDisc.png', size)
        self.blackdisc = loadImages('assets/BlackDisc.png', size)
        self.transition = loadImages('assets/Transition.png', size)

        self.gridLogic = self.regenGrid(self.y, self.x)

    def regenGrid(self, rows, columns):
        """Generate an empty grid for logic use"""
        grid = [[0 for x in range(columns)] for y in range(rows)]

        return grid

    def printGameLogicBoard(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        print(end='  | ')
        print(*letters[0:self.x], sep=' | ', end=' |\n')
        for i, row in enumerate(self.gridLogic):
            print(i + 1, end=' | ')
            for item in row:
                print(item, end=' | ')
            print()
        print()


if __name__ == '__main__':
    game = Othello()
    game.run()
    pygame.quit()