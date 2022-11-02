# class for handling some card functionality / interactions
# card objects are created here

# cards are stored in a list for updating
# card_to_drag is set to the card currently being dragged so that only 1 card
#   is dragged at a time

# Cards must always be added to the all_cards list even if not being updated
# all_cards is used to detect drags
# update_list is used to update cards
# card_to_drag is the current selected card

import pygame as pg
from cards import *

class Cards:
    def __init__(self,game):
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.update_list = []
        self.all_cards = []
        self.card_stacks = []
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

    # detecting whether a card is dragged on another card
    def drag_card_on_card(self):
        card_at_mouse = self.card_at_mouse()
        # check if card stack already exists
        if self.card_to_drag != None and card_at_mouse != None:
            self.stack_cards(card_at_mouse)

    # stacks dragged card or stack with card_at_mouse
    def stack_cards(self, card_at_mouse):
        # if adding to stack
        for stack in self.card_stacks:
            if card_at_mouse in stack and (stack != None or len(stack) != 0) and self.card_to_drag not in stack:
                stack.append(self.card_to_drag)
        # create own stack no stack made for cards
        else: 
            stacked = False
            for stack in self.card_stacks:
                if card_at_mouse in stack or self.card_to_drag in stack:
                    stacked = True
            if not stacked:
                self.card_stacks.append([card_at_mouse, self.card_to_drag])
                
        print(self.card_stacks, '\n')

    # aligns the cards in each stack within card_stacks
    def align_stacked_cards(self):
        pass

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
            self.drag_card_on_card()
            self.card_to_drag = None

    def update(self):
        self.set_drag()

        self.highlight_accepted_cards()
        
        # ensures only one card is being dragged at a time
        # put the card being drag to the back of the update list
        if self.card_to_drag != None:
            self.update_list.insert(-1, self.update_list.pop(self.update_list.index(self.card_to_drag)))
            self.card_to_drag.drag()

        for card in self.update_list:   
            card.update()