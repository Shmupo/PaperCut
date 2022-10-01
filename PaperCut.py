# Software Engineering Project : PaperCut

import pygame as pg
from settings import Settings
from card_base import Card

# The entirety of the game will mostly run here
class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.size = self.settings.window_x, self.settings.window_y
        self.screen = pg.display.set_mode(size=self.size)
        pg.display.set_caption("Papercut")

        background = pg.image.load('images/background.png')
        self.background = pg.transform.scale(background, self.size)
        
        card_image = pg.image.load('images/playercard.png')
        self.test_card = Card(self, card_image)

    # this is the video game loop where everything should be updated
    def play(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            # there is an image that is off-screen but is still loaded and
            # needs to be switched with the current screen
            self.test_card.update()
            pg.display.update()






# this should be left alone
def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()