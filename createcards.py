# create cards here

import pygame as pg
from cards import *

class Cards:
    def __init__(self,game):
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size

        self.card_image = pg.image.load('images/playercard.png')
        self.card_image = pg.transform.scale(self.card_image, self.card_size)
        self.test_card = Card(self.game, self.card_image)
        self.game.update_card_list.append(self.test_card)

        self.shack_image = pg.image.load('images/ShackCard.png')
        self.shack_image = pg.transform.scale(self.shack_image, self.card_size)
        self.shack_card = SettingCard(self.game, self.shack_image)
        self.game.update_card_list.append(self.shack_card)


        