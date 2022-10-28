# Classes for the different types of cards
# Current card types : Object, Enemy, Player, Setting, NPC
import pygame as pg
import time

class Card:
    def __init__(self, game, card_image, name='Base Card', description='This is a base card'):
        self.game = game
        self.screen = self.game.screen
        self.name = name
        self.description = description
        self.image = card_image
        self.rect = self.image.get_rect()
        # a list of what the card can interact with
        self.targets = []
        self.last_pos = (0, 0)
        self.collide = 0

    # moves the card when the user drags it around
    # this is used by the createcards class
    def drag(self):
            self.rect.center = pg.mouse.get_pos()
            #self.collide = self.rect.collidepoint(self.rect.center)
            self.last_pos = self.rect.center

    # checks if the card was dropped on a target and if it is valid
    def check_target(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.draw()


class EnemyCard(Card):
    def __init__(self, game, card_image, name='Enemy Card', description='This is an enemy card'): 
        super().__init__(game, card_image, name, description)


class SettingCard(Card):
    def __init__(self, game ,card_image, name='Setting Card', description='This is a setting card', 
                 duration = 1, accepted_cards = None, event = None):
        super().__init__(game, card_image, name, description)
        # list of cards that can interact with this card
        self.accepted_cards = accepted_cards
        self.events = event
        self.rect.x = 100
        self.rect.y = 100
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.bar_color = (0, 0, 255)
        # in seconds, how long to count before event triggers
        self.duration = duration
        self.start_time = time.time()
        self.time_progress = 0
        self.progress_rect = pg.Rect(self.rect.x, self.rect.y + self.rect.height + 5, 0, 5)

    def progress_bar(self):
        self.progress_rect.x = self.rect.x
        self.progress_rect.y = self.rect.y + self.rect.height+5
        current_time = time.time()

        if current_time - self.start_time > self.time_progress and self.time_progress < self.duration:
            self.progress_rect.width += + (self.rect.width / self.duration)
            self.time_progress += 1
        elif self.time_progress == self.duration: 
            self.start_time = time.time()
            self.time_progress = 0
            self.trigger_event()
            self.progress_rect.width = 0

        pg.draw.rect(self.screen, self.bar_color, self.progress_rect, 5)

    def trigger_event(self):
        goblin_image = pg.image.load('images/GoblinCard.png')
        goblin_image = pg.transform.scale(goblin_image, self.game.settings.card_size)
        goblin_card = EnemyCard(self.game, goblin_image)
        self.game.cards.update_list.append(goblin_card)

    def draw(self):
        super().draw()

    def update(self):
        super().update()
        self.progress_bar()
        self.draw()