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
import time

class Cards:
    def __init__(self,game):
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.update_list = []
        self.all_cards = []
        self.card_to_drag = None
        
        # for displaying description
        self.last_card_at_mouse = None
        self.last_mouse_pos = None
        self.time_start = None
        self.counting = 0
        self.font = pg.font.Font('fonts/Pixeloid.ttf', 10)

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

        self.milk_image = pg.image.load('images/MilkCard.png')
        self.milk_image = pg.transform.scale(self.milk_image,self.card_size)
        self.milk_card = ConsumableCard(self.game, self.milk_image, 'Milk',
                                        description='Nothing like having a carton of milk after a hard days work.',
                                        accepted_cards=[self.player_card])
        self.update_list.append(self.milk_card)
        self.all_cards.append(self.milk_card)
#################################################################################################################

    # when dragging a card, highlight all other cards that can be interacted with
    def highlight_accepted_cards(self):
        if self.card_to_drag != None:
            for card in self.update_list:
                if card.accepted_cards != None:
                    if self.card_to_drag in card.accepted_cards:
                        card.highlight()

    # display card description if hovered over for more than 1 second
    # TODO also compare with mouse position - do not display when moving mouse
    def display_description(self):
        card = self.card_at_mouse()
        if card == self.last_card_at_mouse and not self.counting:
            self.time_start = time.time();
            self.counting = True
        elif self.counting and card != None:
            if self.last_mouse_pos == None: self.last_mouse_pos = pg.mouse.get_pos()
            if card != self.last_card_at_mouse or self.last_mouse_pos != pg.mouse.get_pos():
                self.last_mouse_pos = None
                self.last_card_at_mouse = card
                self.counting = False
                self.time_start = None
            elif time.time() - self.time_start > 1:
                text = self.font.render(card.description, True, (255, 255, 255), (0, 0, 0))
                rect = text.get_rect()
                rect.center = pg.mouse.get_pos()
                rect.x += rect.width / 2 + 25
                rect.y += 25
                self.game.screen.blit(text, rect)
        else: self.last_card_at_mouse = card

    # returns first card in update_list that the mouse is on that is not the card being dragged
    # reads the update list in reverse
    def card_at_mouse(self):
        for card in reversed(self.update_list):
            if type(card) == CardStack:
                for card_in_stack in reversed(card.stack):
                    if card_in_stack.rect.collidepoint(pg.mouse.get_pos()) and card_in_stack != self.card_to_drag:
                        return card_in_stack
            else: 
                if card.rect.collidepoint(pg.mouse.get_pos()) and card != self.card_to_drag:
                        return card
        else: return None

    # detecting whether a card is dragged on another card to create a stack or add to existing stack
    # target is the card being hovered over, card_to_drag is the dragged card
    def check_drag_card_on_card(self):
        target = self.card_at_mouse()
        if self.card_to_drag != None and type(self.card_to_drag) != CardStack:
            if type(target) == CardStack and self.card_to_drag in target.accepted_cards:
                target.add(self.card_to_drag)
            elif target and target.accepted_cards and self.card_to_drag in target.accepted_cards:
                stack = CardStack(self.game, [target, self.card_to_drag])
                self.update_list.remove(target)
                self.update_list.remove(self.card_to_drag)
                self.update_list.append(stack)

    # sets the card to drag
    def set_drag(self):
        # if there is no card being dragged, drag one if mouse is on a card
        if self.card_to_drag == None:
            for target in self.update_list:
                if pg.mouse.get_pressed()[0]:
                    pg.mixer.Channel(0).play(pg.mixer.Sound("sounds/select.wav"))
                    # if target is a stack of cards, check if user wants to drag the bottom off
                    if type(target) == CardStack:
                        if target.stack[-1].rect.collidepoint(pg.mouse.get_pos()):
                            target.remove_bottom()
                            self.card_to_drag = target.stack[-1]
                        elif target.rect.collidepoint(pg.mouse.get_pos()):
                                self.card_to_drag = target
                    elif target.rect.collidepoint(pg.mouse.get_pos()):
                            self.card_to_drag = target
        # release mouse
        elif not pg.mouse.get_pressed()[0]: 
            self.check_drag_card_on_card()
            self.card_to_drag = None

    def update(self):
        self.set_drag()
        self.highlight_accepted_cards()
        #print(self.card_to_drag)
        
        # ensures only one card is being dragged at a time
        # put the card being drag to the back of the update list
        if self.card_to_drag:
            self.update_list.append(self.update_list.pop(self.update_list.index(self.card_to_drag)))
            self.card_to_drag.drag()

        #print(self.update_list)

        # for card in self.all_cards:
        #     if card.delete == True:
        #         print(card)
        #         print("===========")
        #         self.all_cards.remove(card)
        #         self.update_list.remove(card)
                
        for card in self.update_list:
            card.update()
            
        self.display_description()
        #print(self.last_card_at_mouse)