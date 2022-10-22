# Starting menu

import pygame as pg

class Menu():
    def __init__(self, game):
        self.screen = game.screen
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.ng_image = pg.transform.scale(pg.image.load(f'images/NewGameCard.png'), self.card_size)
        self.cont_image = pg.transform.scale(pg.image.load(f'images/ContinueCard.png'), self.card_size)
        self.exit_image = pg.transform.scale(pg.image.load(f'images/ExitCard.png'), self.card_size)
        self.ng_rect = self.ng_image.get_rect()
        self.cont_rect = self.cont_image.get_rect()
        self.exit_rect = self.exit_image.get_rect()
        self.ng_rect.x = 300
        self.cont_rect.x = 500
        self.exit_rect.x = 700
        self.ng_rect.y = self.cont_rect.y = self.exit_rect.y = 400
        self.running = True

        self.font = pg.font.Font('fonts/chalkduster.ttf', 108)
        self.text = self.font.render('PaperCut', True, self.settings.font_color)
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.settings.window_x // 2, self.settings.window_y // 4)

    def select_option(self):
        for event in pg.event.get():
            if(event.type == pg.MOUSEBUTTONUP):
                x, y = pg.mouse.get_pos()
                if self.ng_rect.collidepoint(x, y):
                   self.new_game()
                elif self.cont_rect.collidepoint(x, y):
                    self.load_save()
                elif self.exit_rect.collidepoint(x, y):
                    self.exit_game()

    def load_save(self):
        self.running = False

    def new_game(self):
        self.running = False

    def exit_game(self):
        pg.quit()
        quit()

    def in_menu(self):
        while self.running:
            self.update()

    def update(self):
        self.select_option()
        self.draw()
    
    def draw(self):
        self.screen.blit(self.ng_image, (self.ng_rect.x, self.ng_rect.y))
        self.screen.blit(self.cont_image, (self.cont_rect.x, self.cont_rect.y))
        self.screen.blit(self.exit_image, (self.exit_rect.x, self.exit_rect.y))
        self.screen.blit(self.text, self.textRect)
        pg.display.update()
