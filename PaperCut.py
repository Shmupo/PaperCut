# Software Engineering Project : PaperCut

import pygame as pg
from settings import Settings
from managecards import Cards
from menu import Menu
from score import Score

# The entirety of the game will mostly run here
class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.size = self.settings.window_x, self.settings.window_y
        self.screen = pg.display.set_mode(size=self.size)
        self.screen.fill(self.settings.menu_color)
        pg.display.set_caption("Papercut")

        background = pg.image.load('images/background.png')
        self.background = pg.transform.scale(background, self.size)
        
        self.cards = Cards(self)

        self.menu = Menu(self)

        self.scoreboard = None

        #In game Clock
        self.clock = pg.time.Clock()        
        self.frame_count = 0
        self.frame_rate = 60
        self.start_time = 90
        self.font = pg.font.Font('fonts/Pixeloid.ttf', 15)

    # this is the video game loop where everything should be updated
    def play(self):
        self.menu.in_menu()

        self.scoreboard = Score(self)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            self.screen.blit(self.background, (0, 0))
                # there is an image that is off-screen but is still loaded and
                # needs to be switched with the current screen using pg.display.update
            
            #update clock and display
            self.total_seconds = self.frame_count // self.frame_rate
            self.minutes = self.total_seconds // 60
            self.seconds = self.total_seconds % 60

            self.output_string = "Time: {0:02}:{1:02}".format(self.minutes, self.seconds)
 
            self.text = self.font.render(self.output_string, True, self.settings.font_color)
            self.screen.blit(self.text, [950,25])
            self.frame_count += 1
            self.clock.tick(self.frame_rate)

            if self.minutes == 2 and self.seconds == 0 :
                self.cards.update_list.append(self.cards.serpent_card)
                self.cards.all_cards.append(self.cards.serpent_card)
                self.cards.serpent_card.rect.x = 500
                self.cards.serpent_card.rect.y = 350
            
            self.cards.update()
            self.scoreboard.update()
            
            pg.display.update()

# this should be left alone
def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()