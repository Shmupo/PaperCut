#This modules should only be used for testing is is used as a parent class for other card classes

# Problem : when a card is directly on top of another one, both cards move
import pygame as pg

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

    # moves the card when the user drags it around
    def check_drag(self):
        if self.rect.x < pg.mouse.get_pos()[0] < self.rect.x + self.rect.width and self.rect.y < pg.mouse.get_pos()[1] < self.rect.y + self.rect.height:
            if pg.mouse.get_pressed()[0]:
                self.rect.center = pg.mouse.get_pos()

    # checks if the card was dropped on a target and if it is valid
    def check_target(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.check_drag()
        #self.check_target()
        self.draw()


class EnemyCard(Card):
    def __init__(self): 
        pass


class SettingCard(Card):
    def __init__(self, game ,card_image, name='Setting Card', description='This is a setting card', duration = 0, accepted_cards = None, event = None):
        super().__init__(game, card_image, name, description)
        self.duration = duration
        # list of cards that can interact with this card
        self.accepted_cards = accepted_cards
        self.events = event
        self.rect.x = 100
        self.rect.y = 100

    # when triggered, create and start the progress bar
    def start_timer(self):
        pass

    def trigger_event():
        pass

    def draw(self):
        super().draw()

    def update(self):
        super().update()


class ObjectCard(Card):
    def __init__(self, game ,card_image, name='Object Card', description='This is an object card'):
        super().__init__(self, game, card_image, name, description)

    def replenish(self, EntityCard):
        pass

    def update(self):
        pass

    def draw(self):
        pass