# create cards here

# cards are stored in a list for updating
# card_to_drag is set to the card currently being dragged so that only 1 card
#   is dragged at a time

import pygame as pg
from cards import *


# Cards must always be added to the all_cards list even if not being updated
# all_cards is used to detect drags
# update_list is used to update cardss
# card_to+drag is the current selected card

class Cards:
    def __init__(self,game):
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.update_list = []
        self.all_cards = []
        self.card_to_drag = None

        self.card_image = pg.image.load('images/playercard.png')
        self.card_image = pg.transform.scale(self.card_image, self.card_size)
        self.player_card = Card(self.game, self.card_image)
        self.update_list.append(self.player_card)
        self.all_cards.append(self.player_card)

        # used to create copties in cards.py
        self.goblin_image = pg.image.load('images/GoblinCard.png')
        self.goblin_image = pg.transform.scale(self.goblin_image, self.game.settings.card_size)
        self.goblin_card = EnemyCard(self.game, self.goblin_image, name="Goblin", 
                                     description='He put his prize belongings on his back. Minds his own business. Likes other goblins.')

        self.shack_image = pg.image.load('images/ShackCard.png')
        self.shack_image = pg.transform.scale(self.shack_image, self.card_size)
        self.shack_card = SettingCard(self.game, self.shack_image, 'Shack', 
                                      'This is where gobo and his family lives', duration=5, 
                                      accepted_cards=self.player_card, event_cards=[self.goblin_card])
        self.update_list.append(self.shack_card)
        self.all_cards.append(self.shack_card)

    # checks whether the card being dragged is dropped upon another card
    def card_dragged_on_card(self):
        pass

    # sets the card to drag
    def set_card_to_drag(self):
        for event in pg.event.get():
            # if there is no card being dragged, drag one if mouse is on a card
            if self.card_to_drag == None:
                for card in self.update_list:
                        if card.rect.collidepoint(pg.mouse.get_pos()) and event.type == pg.MOUSEBUTTONDOWN:  
                            self.card_to_drag = card
            # release mouse
            elif event.type == pg.MOUSEBUTTONUP: 
                #card_dragged_on_card()
                self.card_to_drag = None

    def update(self):
        self.set_card_to_drag()
        print(self.card_to_drag)
        
        # ensures only one card is being dragged at a time
        # put the card being drag to the back of the update list
        if self.card_to_drag != None:
            self.update_list.insert(-1, self.update_list.pop(self.update_list.index(self.card_to_drag)))
            self.card_to_drag.drag()

        for card in self.update_list:   
            card.update()

        