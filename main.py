import pygame
from othello import Othello
from minimax import init_ai_vs_ai

if __name__ == "__main__":
    game = Othello(4)

    # Initialize AI vs AI mode
    init_ai_vs_ai(game)

    # Start the GUI loop
    game.run()

    pygame.quit()
