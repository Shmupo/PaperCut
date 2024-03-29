# create cards here

# cards are stored in a list for updating
# card_to_drag is set to the card currently being dragged so that only 1 card
#   is dragged at a time

import pygame as pg
from cards import *

class Cards:
    def __init__(self,game):
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.update_list = []
        self.all_cards = []
        self.card_to_drag = None
        self.last_card_to_drag = None

        self.card_image = pg.image.load('images/playercard.png')
        self.card_image = pg.transform.scale(self.card_image, self.card_size)
        self.player_card = Card(self.game, self.card_image)
        self.update_list.append(self.player_card)
        self.all_cards.append(self.player_card)

        self.shack_image = pg.image.load('images/ShackCard.png')
        self.shack_image = pg.transform.scale(self.shack_image, self.card_size)
        self.shack_card = SettingCard(self.game, self.shack_image)
        self.update_list.append(self.shack_card)
        self.all_cards.append(self.shack_card)

    # sets the card to drag
    def set_card_to_drag(self):
        for event in pg.event.get():
            if self.card_to_drag == None:
                for card in self.all_cards:
                    if card.rect.x < pg.mouse.get_pos()[0] < card.rect.x + card.rect.width and card.rect.y < pg.mouse.get_pos()[1] < card.rect.y + card.rect.height:
                        if event.type == pg.MOUSEBUTTONDOWN:    
                            self.card_to_drag = card
            elif event.type == pg.MOUSEBUTTONUP: self.card_to_drag = None

    def update(self):
        self.set_card_to_drag()
        print(self.card_to_drag)
        
        # ensures only one card is being dragged at a time
        # put the card being drag to the top of the update list
        if self.card_to_drag != None:
            self.update_list.insert(0, self.update_list.pop(self.update_list.index(self.card_to_drag)))
            self.card_to_drag.drag()

        for card in self.update_list:   
            card.update()

        