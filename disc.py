class Disc:
    def __init__(self, player, gridX, gridY, image, main):
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.posX = 60 + (gridY * 60)
        self.posY = 60 + (gridX * 60)
        self.GAME = main

        self.image = image

    def transition(self, transitionImages, discImage):
        self.image = transitionImages
        self.GAME.draw()
        self.image = discImage

    def draw(self, window):
        window.blit(self.image, (self.posX, self.posY))