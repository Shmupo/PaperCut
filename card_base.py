#This modules should only be used for testing is is used as a parent class for other card classes
import pygame as pg

class Card:
    def __init__(self, game, card_image, name='Base Card', description='This is a base card'):
        self.game = game
        self.screen = self.game.screen
        self.name = name
        self.description = description
        self.image = card_image
        # a list of what the card can interact with
        self.targets = []
        self.pos_x = 0
        self.pos_y = 0

        background = pg.image.load('images/background.png')

    # moves the card when the user drags it around
    def check_drag(self):
        pass

    # checks if the card was dropped on a target and if it is valid
    def check_target(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (self.pos_x, self.pos_y))

    def update(self):
        self.check_drag()
        self.check_target()
        self.draw()