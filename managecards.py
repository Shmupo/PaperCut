# class for handling some card functionality / interactions
# card objects are created here

# cards are stored in a list for updating
# card_to_drag is set to the card currently being dragged so that only 1 card
#   is dragged at a time

# Cards must always be added to the all_cards list even if not being updated
# all_cards is used to detect drags
# update_list is used to update cards
# card_to_drag is the current selected card

# stacks of cards are represented as lists within update_list

import pygame as pg
from cards import *
from cardstack import CardStack

class Cards:
    def __init__(self,game):
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.update_list = []
        self.all_cards = []
        self.card_to_drag = None

# CREATE CARDS HERE #############################################################################################
        self.card_image = pg.image.load('images/playercard.png')
        self.card_image = pg.transform.scale(self.card_image, self.card_size)
        self.player_card = PlayerCard(self.game, self.card_image, 'Player', 
                                'Your best friend was a magical beetle. Now you wear his skull so that he is always with you. Rest in peace Moe.')
        self.update_list.append(self.player_card)
        self.all_cards.append(self.player_card)

        # used to create copies in cards.py
        self.goblin_image = pg.image.load('images/GoblinCard.png')
        self.goblin_image = pg.transform.scale(self.goblin_image, self.game.settings.card_size)
        self.goblin_card = EnemyCard(self.game, self.goblin_image, name="Goblin", 
                                     description='This goblin has mostly junk in his bag. Minds his own business. Likes other goblins.',
                                     accepted_cards=[self.player_card])

        self.shack_image = pg.image.load('images/ShackCard.png')
        self.shack_image = pg.transform.scale(self.shack_image, self.card_size)
        self.shack_card = SettingCard(self.game, self.shack_image, 'Shack', 
                                      'This is where gobo and his family lives. It ain\'t much, but it\'s home.', duration=5, 
                                      accepted_cards=[self.player_card], event_cards=[self.goblin_card])
        self.update_list.append(self.shack_card)
        self.all_cards.append(self.shack_card)
#################################################################################################################

    # when dragging a card, highlight all other cards that can be interacted with
    def highlight_accepted_cards(self):
        if self.card_to_drag != None:
            for card in self.update_list:
                if card.accepted_cards != None:
                    if self.card_to_drag in card.accepted_cards:
                        card.highlight()

    # returns first card in update_list that the mouse is on that is not the card being dragged
    def card_at_mouse(self):
        for card in self.update_list:
                if card.rect.collidepoint(pg.mouse.get_pos()) and card != self.card_to_drag:
                    return card
        else: return None

    # detecting whether a card is dragged on another card to create a stack or add to existing stack
    def check_drag_card_on_card(self):
        target = self.card_at_mouse()
        if self.card_to_drag != None:
            if type(target) == CardStack:
                target.add(self.card_to_drag)
            elif target:
                stack = CardStack(self.game, [target, self.card_to_drag])
                self.update_list.remove(target)
                self.update_list.remove(self.card_to_drag)
                self.update_list.append(stack)

    # sets the card to drag
    def set_drag(self):
        # if there is no card being dragged, drag one if mouse is on a card
        if self.card_to_drag == None:
            for card in self.update_list:
                if pg.mouse.get_pressed()[0]:
                    if card.rect.collidepoint(pg.mouse.get_pos()):
                        self.card_to_drag = card
        # release mouse
        elif not pg.mouse.get_pressed()[0]: 
            self.check_drag_card_on_card()
            self.card_to_drag = None

    def update(self):
        self.set_drag()
        self.highlight_accepted_cards()
        
        # ensures only one card is being dragged at a time
        # put the card being drag to the back of the update list
        if self.card_to_drag:
            self.update_list.append(self.update_list.pop(self.update_list.index(self.card_to_drag)))
            self.card_to_drag.drag()

        print(self.update_list)

        for card in self.update_list:
            card.update()