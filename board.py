from disc import Disc
from utilitly import *

class Board:
    def __init__(self, length, size, main):
        self.GAME = main
        self.l = length
        self.size = size
        self.whitedisc = loadImages('assets/WhiteDisc.png', size)
        self.blackdisc = loadImages('assets/BlackDisc.png', size)
        self.transition = loadImages('assets/Transition.png', size)
        self.bg = self.loadBackgroundImages()

        self.discs = {}

        self.gridBg = self.createbgimg()

        self.gridLogic = self.regenGrid(self.l, self.l)

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
        for y in range(self.l+2):
            row = []
            for x in range(self.l + 2):
                if y == 0:
                    if x == 0:
                        row.append('B2')
                    elif x == self.l +1:
                        row.append('D2')
                    else:
                        row.append(f'{alpha[x-1]}0')
                elif y == self.l +1:
                    if x == 0:
                        row.append('C2')
                    elif x == self.l +1:
                        row.append('F2')
                    else:
                        row.append('G2')
                else:
                    if x == 0:
                        row.append(f'{alpha[y-1]}1')
                    elif x == self.l +1:
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
        if self.GAME.currentPlayer == 1:
            for move in availableMoves:
                pygame.draw.circle(window, 'White', (60 + (move[1]*60) + 30, 60 + (move[0]*60) + 30), 10, 5)
        else:
            for move in availableMoves:
                pygame.draw.circle(window, 'Black', (60 + (move[1] * 60) + 30, 60 + (move[0] * 60) + 30), 10, 5)

    def regenGrid(self, rows, columns):
        """Generate an empty grid for logic use"""
        grid = [[0 for x in range(columns)] for y in range(rows)]
        self.insertDisc(grid, 1, self.l//2 - 1,self.l//2 -1)
        self.insertDisc(grid, -1, self.l//2 -1,self.l//2)
        self.insertDisc(grid, 1, self.l//2,self.l//2)
        self.insertDisc(grid, -1, self.l//2,self.l//2 -1)

        return grid

    def printGameLogicBoard(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        print(end='  | ')
        print(*letters[0:self.l], sep=' | ', end=' |\n')
        for i, row in enumerate(self.gridLogic):
            line = f'{i+1} |'.ljust(3, " ")
            for item in row:
                if item == -1:
                    item = '●'
                elif item == 1:
                    item = '○'
                else:
                    item = ' '
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
                DIRECTIONS = directions(gridX, gridY, 0, 0, self.l-1, self.l-1)

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
        surroundCells = directions(x, y, 0, 0, self.l-1, self.l-1)
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

                if checkX < 0 or checkX > self.l-1 or checkY < 0 or checkY > self.l-1:
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

    def animateTransitions(self, cell, player):
        if player == 1:
            self.discs[(cell[0], cell[1])].transition(self.transition, self.whitedisc)
        else:
            self.discs[(cell[0], cell[1])].transition(self.transition, self.blackdisc)
