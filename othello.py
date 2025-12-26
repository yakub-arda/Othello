import pygame
from board import Board
import copy


class Othello:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('Othello')

        self.player1 = -1
        self.player2 = 1
        self.currentPlayer = -1
        self.time = 0
        self.size = size
        self.grid = Board(self.size, (60, 60), self)
        self.RUN = True
        self.gameOver = False
        self.winner = None

        # Move history
        self.moveHistory = []  # List of tuples: (blackMove, whiteMove or None)
        self.gridHistory = []
        self.playerHistory = []
        self.currentHistoryIndex = 0
        self.viewingHistory = False
        self.consoleScroll = 0

        # Store initial state
        self.gridHistory.append(copy.deepcopy(self.grid.gridLogic))
        self.playerHistory.append(self.currentPlayer)

        # UI elements
        self.prevButton = pygame.Rect(750, 500, 100, 40)
        self.nextButton = pygame.Rect(870, 500, 100, 40)
        self.consoleBox = pygame.Rect(750, 230, 230, 250)

    def run(self):
        while self.RUN:
            self.input()
            self.update()
            self.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.printGameLogicBoard()

                if event.button == 1:
                    # Check button clicks
                    if self.prevButton.collidepoint(event.pos):
                        if self.currentHistoryIndex > 0:
                            self.currentHistoryIndex -= 1
                            self.viewingHistory = (self.currentHistoryIndex < len(self.gridHistory) - 1)
                            self.updateBoardDisplay()
                            self.updateConsoleScroll()
                    elif self.nextButton.collidepoint(event.pos):
                        if self.currentHistoryIndex < len(self.gridHistory) - 1:
                            self.currentHistoryIndex += 1
                            self.viewingHistory = (self.currentHistoryIndex < len(self.gridHistory) - 1)
                            self.updateBoardDisplay()
                            self.updateConsoleScroll()
                    else:
                        # Game moves
                        if not self.gameOver and not self.viewingHistory:
                            x, y = pygame.mouse.get_pos()
                            x, y = (x - 60) // 60, (y - 60) // 60
                            validCells = self.grid.findAvailableMoves(self.grid.gridLogic, self.currentPlayer)
                            if (y, x) in validCells:
                                self.grid.insertDisc(self.grid.gridLogic, self.currentPlayer, y, x)
                                flankableDiscs = self.grid.flankableDiscs(y, x, self.grid.gridLogic, self.currentPlayer)
                                for disc in flankableDiscs:
                                    self.grid.animateTransitions(disc, self.currentPlayer)
                                    self.grid.gridLogic[disc[0]][disc[1]] *= -1

                                # Record move
                                alpha = 'ABCDEFGH'
                                moveNotation = f"{alpha[x]}{y+1}"

                                # Store moves in pairs
                                if self.currentPlayer == -1:  # Black's turn
                                    self.moveHistory.append([moveNotation, None])
                                else:  # White's turn
                                    if self.moveHistory:
                                        self.moveHistory[-1][1] = moveNotation
                                    else:
                                        self.moveHistory.append([None, moveNotation])

                                self.currentPlayer *= -1
                                self.gridHistory.append(copy.deepcopy(self.grid.gridLogic))
                                self.playerHistory.append(self.currentPlayer)
                                self.currentHistoryIndex = len(self.gridHistory) - 1
                                self.updateConsoleScroll()

                                self.time = pygame.time.get_ticks()

    def updateConsoleScroll(self):
        """Auto-scroll console to keep current move visible"""
        maxVisibleMoves = 8
        highlightMoveIndex = (self.currentHistoryIndex - 1) // 2

        # Calculate total moves that should be visible
        totalMovesToShow = min(len(self.moveHistory), (self.currentHistoryIndex + 1) // 2 + 1)

        # If highlighted move is below visible area, scroll down
        if highlightMoveIndex >= self.consoleScroll + maxVisibleMoves:
            self.consoleScroll = highlightMoveIndex - maxVisibleMoves + 1

        # If highlighted move is above visible area, scroll up
        if highlightMoveIndex < self.consoleScroll:
            self.consoleScroll = highlightMoveIndex

        # Ensure scroll doesn't go negative
        self.consoleScroll = max(0, self.consoleScroll)

    def updateBoardDisplay(self):
        """Update the visual board to match the history state"""
        targetGrid = self.gridHistory[self.currentHistoryIndex]

        # Update grid logic
        for i in range(self.grid.l):
            for j in range(self.grid.l):
                self.grid.gridLogic[i][j] = targetGrid[i][j]

        # Update disc visuals
        self.grid.discs.clear()
        for i in range(self.grid.l):
            for j in range(self.grid.l):
                if targetGrid[i][j] != 0:
                    player = targetGrid[i][j]
                    discImage = self.grid.whitedisc if player == 1 else self.grid.blackdisc
                    from disc import Disc
                    self.grid.discs[(i, j)] = Disc(player, i, j, discImage, self)

    def update(self):
        if self.gameOver or self.viewingHistory:
            return

        validCells = self.grid.findAvailableMoves(self.grid.gridLogic, self.currentPlayer)
        if not validCells:
            self.currentPlayer *= -1
            opponentValidCells = self.grid.findAvailableMoves(self.grid.gridLogic, self.currentPlayer)
            if not opponentValidCells:
                self.determineWinner()

        boardFull = all(self.grid.gridLogic[i][j] != 0
                        for i in range(self.grid.l)
                        for j in range(self.grid.l))
        if boardFull:
            self.determineWinner()

    def determineWinner(self):
        player1Count = sum(row.count(1) for row in self.grid.gridLogic)
        player2Count = sum(row.count(-1) for row in self.grid.gridLogic)

        if player1Count > player2Count:
            self.winner = 'White is the winner.'
        elif player2Count > player1Count:
            self.winner = 'Black is the winner.'
        else:
            self.winner = 'It\'s a tie!'

        self.gameOver = True

    def drawUI(self):
        # Get current grid to display
        displayGrid = self.gridHistory[self.currentHistoryIndex]

        # Count pieces
        blackCount = sum(row.count(-1) for row in displayGrid)
        whiteCount = sum(row.count(1) for row in displayGrid)

        # Fonts
        font = pygame.font.Font(None, 36)
        smallFont = pygame.font.Font(None, 24)

        # Score display
        scoreText = font.render(f"Black: {blackCount} - White: {whiteCount}", True, (255, 255, 255))
        self.screen.blit(scoreText, (750, 50))

        # Winner display
        if self.gameOver and not self.viewingHistory:
            winnerText = font.render(self.winner, True, (255, 255, 0))
            self.screen.blit(winnerText, (750, 100))

        # Console label
        consoleLabel = smallFont.render("Console:", True, (255, 255, 255))
        self.screen.blit(consoleLabel, (750, 200))

        # Console box
        pygame.draw.rect(self.screen, (50, 50, 50), self.consoleBox)
        pygame.draw.rect(self.screen, (255, 255, 255), self.consoleBox, 2)

        # Show moves with scrolling
        highlightMoveIndex = (self.currentHistoryIndex - 1) // 2
        maxVisibleMoves = 8

        y_offset = 240
        endIdx = min(self.consoleScroll + maxVisibleMoves, len(self.moveHistory))

        for i in range(self.consoleScroll, endIdx):
            # Only show completed moves and current partial move
            if i * 2 + 1 > self.currentHistoryIndex:
                break

            blackMove = self.moveHistory[i][0] or "---"
            whiteMove = self.moveHistory[i][1] or "---"
            moveText = f"{i + 1}. {blackMove} - {whiteMove}"

            # Highlight the move pair we're currently viewing
            color = (255, 255, 0) if i == highlightMoveIndex else (255, 255, 255)
            text = smallFont.render(moveText, True, color)
            self.screen.blit(text, (760, y_offset))
            y_offset += 28

        # Navigation buttons
        pygame.draw.rect(self.screen, (100, 100, 100), self.prevButton)
        pygame.draw.rect(self.screen, (255, 255, 255), self.prevButton, 2)
        prevText = smallFont.render("Previous", True, (255, 255, 255))
        self.screen.blit(prevText, (self.prevButton.x + 15, self.prevButton.y + 10))

        pygame.draw.rect(self.screen, (100, 100, 100), self.nextButton)
        pygame.draw.rect(self.screen, (255, 255, 255), self.nextButton, 2)
        nextText = smallFont.render("Next", True, (255, 255, 255))
        self.screen.blit(nextText, (self.nextButton.x + 25, self.nextButton.y + 10))

        # Show if viewing history
        if self.viewingHistory:
            historyText = smallFont.render(f"Viewing state {self.currentHistoryIndex}/{len(self.gridHistory) - 1}",
                                           True, (255, 255, 0))
            self.screen.blit(historyText, (750, 555))

    def draw(self):
        self.screen.fill((0, 0, 0))

        # If viewing history, show available moves for the player whose turn it is in that state
        if self.viewingHistory:
            currentPlayer = self.playerHistory[self.currentHistoryIndex]
            availableMoves = self.grid.findAvailableMoves(self.gridHistory[self.currentHistoryIndex], currentPlayer)

            # Draw board without normal available moves
            self.screen.blit(self.grid.gridBg, (0, 0))
            for disc in self.grid.discs.values():
                disc.draw(self.screen)

            # Draw historical available moves
            if currentPlayer == 1:
                for move in availableMoves:
                    pygame.draw.circle(self.screen, 'White', (60 + (move[1] * 60) + 30, 60 + (move[0] * 60) + 30), 10,
                                       5)
            else:
                for move in availableMoves:
                    pygame.draw.circle(self.screen, 'Black', (60 + (move[1] * 60) + 30, 60 + (move[0] * 60) + 30), 10,
                                       5)
        else:
            self.grid.drawBoard(self.screen)

        self.drawUI()
        pygame.display.update()