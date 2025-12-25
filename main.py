from turtledemo.penrose import start

import pygame
import random
import copy

# Utility Functions
def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    """Check to determine which directions are valid from current cell"""
    validdirections = []
    if x != minX: validdirections.append((x-1, y))
    if x != minX and y != minY: validdirections.append((x-1, y-1))
    if x != minX and y != maxY: validdirections.append((x-1, y+1))

    if x!= maxX: validdirections.append((x+1, y))
    if x != maxX and y != minY: validdirections.append((x+1, y-1))
    if x != maxX and y != maxY: validdirections.append((x+1, y+1))

    if y != minY: validdirections.append((x, y-1))
    if y != maxY: validdirections.append((x, y+1))

    return validdirections


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
                    validCells = self.grid.findAvailableMoves(self.grid.gridLogic, self.currentPlayer)
                    if not validCells:
                        pass
                    else:
                        if (y, x) in validCells:
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

        availableMoves = self.findAvailableMoves(self.gridLogic, self.GAME.currentPlayer)
        for move in availableMoves:
            pygame.draw.circle(window, 'White', (60 + (move[1]*60) + 30, 60 + (move[0]*60) + 30), 10, 5)


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

    def findValidCells(self, grid, curPlayer):
        """Preforms a check to find all empty cells that are adjacent to the opposing player"""
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                DIRECTIONS = directions(gridX, gridY, 0, 0, self.x-1, self.y-1) # might be self.y -1, self.x -1

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue

                    if (gridX, gridY) in validCellToClick:
                        continue

                    validCellToClick.append((gridX,gridY))

        return validCellToClick

    def flankableDiscs(self, x, y, grid, player):
        surroundCells = directions(x, y, 0, 0, self.x-1, self.y-1) # might be self.y -1, self.x -1
        if len(surroundCells) == 0:
            return []

        flankableDiscs = []

        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []

            RUN = True
            while RUN:
                if grid[checkX][checkY] == player *-1:
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == player:
                    RUN = False
                    break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    RUN = False
                checkX += difX
                checkY += difY

                if checkX < 0 or checkX > self.x-1 or checkY < 0 or checkY > self.y-1:
                    currentLine.clear()
                    RUN = False

            if len(currentLine) > 0:
                flankableDiscs.extend(currentLine)

        return flankableDiscs


    def findAvailableMoves(self, grid, currentPlayer):
        """Takes the list of available cells and checks each to see if they are playable"""
        validCells = self.findValidCells(grid,currentPlayer)
        playableCells = []

        for cell in validCells:
            x,y = cell
            if cell in playableCells:
                continue

            outflankDiscs = self.flankableDiscs(x, y, grid, currentPlayer)

            # if len(outflankDiscs) > 0 and cell not in playableCells:
            if len(outflankDiscs) > 0:
                playableCells.append(cell)

        return playableCells

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