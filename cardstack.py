import pygame as pg

# acts like the stack data structure, cards only can be removed when the top card is dragged off
# cards is the Cards() object

# TODO : Allow player to drag off the last card 

class CardStack:
    # how much to move the next card in the stack down
    y_offset = 20

    def __init__(self, game, stack):
        self.game = game
        self.cards = game.cards
        self.stack = stack
        self.top_card = stack[0]
        self.accepted_cards = self.top_card.accepted_cards
        self.rect = pg.Rect(self.top_card.rect.x, self.top_card.rect.y, self.top_card.rect.width, self.y_offset)
        self.stack_size = 2

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
    def check_bottom_drag(self):
        if self.cards.card_to_drag == self.stack[-1]:
            self.cards.update_list.append(self.stack[-1])
            self.stack.remove(-1)

    # adds card to stack, removing it from the update_list
    def add(self, card):
        self.cards.update_list.remove(card)
        self.cards.append(card)
        self.rect.y += card.rect.height
        self.rect.clamp(card)

    def update(self):
        self.check_bottom_drag()
        # for testing
        pg.draw.rect(self.cards.game.screen, (255, 255, 255), self.rect)
        for card in self.stack:
            card.update()
            if card != self.stack[0]:
                self.align_stack()
