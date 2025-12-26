import pygame
from othello import Othello

if __name__ == '__main__':
    game = Othello(4)
    game.run()
    pygame.quit()