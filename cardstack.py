import pygame as pg
from cards import SettingCard
from cards import ConsumableCard
from cards import EnemyCard
from cards import PlayerCard
from time import time

# cards is the Cards() object for card management
# accepted cards are the same accepted cards of the base card of the stack , aka the first added card in stack[0]

class CardStack:
    # how much to move the next card in the stack down
    y_offset = 20

    def __init__(self, game, stack):
        self.game = game
        self.cards = game.cards
        self.stack = stack
        self.base_card = stack[0]
        self.accepted_cards = stack[0].accepted_cards
        self.rect = pg.Rect(self.base_card.rect.x, self.base_card.rect.y, self.base_card.rect.width, self.y_offset)
        self.stack_size = 2
        # used for fighting
        self.start_time = None

    def highlight(self):
        for card in self.stack:
            card.highlight()

    # moves the card when the user drags it around
    # this is used by the createcards class
    def drag(self):
        self.rect.center = pg.mouse.get_pos()
        self.rect.clamp_ip(self.game.settings.play_area_rect)

    # aligns the stack according to the first card in the list
    def align_stack(self):
        for card in self.stack:
            card.rect.x = self.rect.x
            card.rect.y = self.rect.y + self.y_offset * self.stack.index(card)

    # if the bottom card is dragged, remove it
    def remove_bottom(self):
        self.cards.update_list.append(self.stack[-1])
        self.stack.pop()
        self.rect.y - self.game.settings.card_size[1]

        if len(self.stack) < 2:
            self.convert_to_card()

    # adds card to stack, removing it from the update_list and making the drag box bigger
    def add(self, card):
        self.cards.update_list.remove(card)
        self.stack.append(card)
        self.rect.height += self.y_offset
        self.rect.clamp(card)

    # if only 1 card in stack, remove the CardStack object and put the single card into update list
    def convert_to_card(self):
        if type(self.base_card) == SettingCard:
            self.base_card.activate(False)
        self.cards.update_list.insert(-1, self.base_card)
        self.cards.update_list.pop(self.cards.update_list.index(self))

    # activates the base card if an accepted card is attatched
    def activate_cards(self):
        activate = False
        if type(self.base_card) == SettingCard:
            for card in self.stack:
                if card in self.accepted_cards:
                    activate = True
            self.base_card.activate(activate)
        
        elif type(self.base_card) == ConsumableCard:
            for card in self.stack:
                if card in self.accepted_cards:
                    self.base_card.consume(card)

        # if stack of enemy cards has player attached, fight
        # create a timer to slowly tick away damage/health
        elif type(self.base_card) == EnemyCard:
            if type(self.stack[-1]) == PlayerCard:
                #self.player_fight()
                pass

    def player_fight(self):
        if self.start_time == None: self.start_time = time.time()
        if self.start_time - time.time() >= 1:
            player = self.stack[-1]
            self.start_time = None
            player.health -= 1
            player.damage -= 1
            self.stack[-2].health -= 1
            self.stack[-2].damage -= 1
            

    def update(self):
        # for testing
        pg.draw.rect(self.cards.game.screen, (255, 255, 255), self.rect)
        # END
        self.activate_cards()
        for card in self.stack:
            card.update()
            if card != self.stack[0]:
                self.align_stack()
