import pygame as pg

# cards is the Cards() object for card management

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
        card.trigger_event()

    # if the bottom card is dragged, remove it
    def remove_bottom(self):
        self.cards.update_list.append(self.stack[-1])
        self.stack.pop()
        self.rect.y - self.game.settings.card_size[1]

        if len(self.stack) < 2:
            self.convert_to_card()

    # adds card to stack, removing it from the update_list
    def add(self, card):
        self.cards.update_list.remove(card)
        self.cards.append(card)
        self.rect.y += card.rect.height
        self.rect.clamp(card)
    # if only 1 card in stack, remove the CardStack object and put the single card into update list
    def convert_to_card(self):
        self.cards.update_list.insert(-1, self.stack[0])
        self.cards.update_list.pop(self.cards.update_list.index(self))
    # activates the cards in the stack to trigger their events
    def activate_cards(card):
        print("Activate_card")
        card.trigger_event()

    def update(self):
        # for testing
        pg.draw.rect(self.cards.game.screen, (255, 255, 255), self.rect)
        for card in self.stack:
            card.update()
            if card != self.stack[0]:
                self.align_stack()