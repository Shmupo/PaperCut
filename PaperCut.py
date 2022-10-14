# Software Engineering Project : PaperCut

import pygame as pg
from settings import Settings
from card_base import Card
from menu import Menu

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
        card_image = pg.transform.scale(card_image, (96, 128))
        self.test_card = Card(self, card_image)

        self.menu = Menu(self)

    # this is the video game loop where everything should be updated
    def play(self):
        self.menu.in_menu()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            self.screen.blit(self.background, (0, 0))
                # there is an image that is off-screen but is still loaded and
                # needs to be switched with the current screen using pg.display.update
            self.test_card.update()
            
            pg.display.update()






# this should be left alone
def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()