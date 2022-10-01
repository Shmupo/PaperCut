# Software Engineering Project : PaperCut

import pygame as pg
from settings import Settings

# The entirety of the game will mostly run here
class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.window_x, self.settings.window_y
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Papercut")

    # this is the video game loop where everything should be updated
    def play(self):
        while True:
            self.screen.fill((0 ,0 ,0))

            # there is an image that is off-screen but is still loaded and
            # needs to be switched with the current screen
            pg.display.flip()






# this should be left alone
def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()