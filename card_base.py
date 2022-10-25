#This modules should only be used for testing is is used as a parent class for other card classes
import pygame as pg

class Card:
    def __init__(self, game, card_image, name='Base Card', description='This is a base card'):
        self.game = game
        self.screen = self.game.screen
        self.name = name
        self.description = description
        self.image = card_image
        self.rect = self.image.get_rect()
        # a list of what the card can interact with
        self.targets = []
        self.last_pos = (0, 0)

        background = pg.image.load('images/background.png')

    # moves the card when the user drags it around
    def check_drag(self):
        if self.rect.x < pg.mouse.get_pos()[0] < self.rect.x + self.rect.width and self.rect.y < pg.mouse.get_pos()[1] < self.rect.y + self.rect.height:
            if pg.mouse.get_pressed()[0]:
                self.rect.center = pg.mouse.get_pos()

    # checks if the card was dropped on a target and if it is valid
    def check_target(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.check_drag()
        #self.check_target()
        self.draw()