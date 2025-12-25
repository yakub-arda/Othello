from turtledemo.penrose import start

import pygame
import random
import copy

# Utility Functions
def loadImages(path, size):
    """Load an image into the game, and scale the image"""

    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, size)

    return img

def loadSpriteSheet(sheet, row, col, newSize, size):
    """Creates an empty surface, loads a portion of the spritesheet onto the surface, then return that surface as img"""
    image = pygame.Surface((256,256)).convert_alpha()
    image.blit(sheet,(0,0), (row*size[0], col*size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image


# Classes
class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000,600)) # found a more optimal screen size
        pygame.display.set_caption('Othello')

        self.player1 = 1
        self.player2 = -1

        self.currentPlayer = 1

        self.columns = 8
        self.rows = 8

        self.grid = Board(self.rows, self.columns, (60, 60), self)

        self.RUN = True

    def run(self):
        while self.RUN:
            self.input()
            self.update()
            self.draw()

    def input(self): # overwriting an in-built function, not used for now
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.printGameLogicBoard()

                if event.button == 1:
                    x,y = pygame.mouse.get_pos()
                    x,y = (x-60)//60 , (y-60)//60

                    self.grid.insertDisc(self.grid.gridLogic, self.currentPlayer, y, x)
                    self.currentPlayer *= -1


    def update(self):
        pass

    def draw(self):
        self.screen.fill((0,0,0))

        self.grid.drawBoard(self.screen)

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
        self.bg = self.loadBackgroundImages()

        self.discs = {}

        self.gridBg = self.createbgimg()

        self.gridLogic = self.regenGrid(self.y, self.x)

    def loadBackgroundImages(self):
        alpha = 'ABCDEFGH'
        spriteSheet = pygame.image.load('assets/SpriteSheet.png').convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(8):
                imageDict[alpha[j]+ str(i)] = loadSpriteSheet(spriteSheet, j, i, self.size, (256,256))
        return imageDict

    def createbgimg(self):
        alpha = 'ABCDEFGH'
        gridBg = []
        for y in range(self.y+2):
            row = []
            for x in range(self.x + 2):
                if y == 0:
                    if x == 0:
                        row.append('B2')
                    elif x == self.x +1:
                        row.append('D2')
                    else:
                        row.append(f'{alpha[x-1]}0')
                elif y == self.y +1:
                    if x == 0:
                        row.append('C2')
                    elif x == self.x +1:
                        row.append('F2')
                    else:
                        row.append('G2')
                else:
                    if x == 0:
                        row.append(f'{alpha[y-1]}1')
                    elif x == self.x +1:
                        row.append('E2')
                    else:
                        row.append('A2')
            gridBg.append(row)

        image = pygame.Surface((720,720))
        for j, row in enumerate(gridBg):
            for i, img in enumerate(row):
                image.blit(self.bg[img],(i*self.size[0], j*self.size[1]))

        return image

    def drawBoard(self, window):
        window.blit(self.gridBg, (0,0))

        for disc in self.discs.values():
            disc.draw(window)


    def regenGrid(self, rows, columns):
        """Generate an empty grid for logic use"""
        grid = [[0 for x in range(columns)] for y in range(rows)]
        self.insertDisc(grid, 1, 3,3)
        self.insertDisc(grid, -1, 3,4)
        self.insertDisc(grid, 1, 4,4)
        self.insertDisc(grid, -1, 4,3)

        return grid

    def printGameLogicBoard(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        print(end='  | ')
        print(*letters[0:self.x], sep=' | ', end=' |\n')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()

    def insertDisc(self, grid, curplayer, y, x):
        discImage = self.whitedisc if curplayer == 1 else self.blackdisc
        self.discs[(y,x)] = Disc(curplayer, y, x, discImage, self.GAME)
        grid[y][x] = self.discs[(y,x)].player


class Disc:
    def __init__(self, player, gridX, gridY, image, main):
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.posX = 60 + (gridY * 60)
        self.posY = 60 + (gridX * 60)
        self.GAME = main

        self.image = image

    def transition(self):
        pass

    def draw(self, window):
        window.blit(self.image, (self.posX, self.posY))


if __name__ == '__main__':
    game = Othello()
    game.run()
    pygame.quit()