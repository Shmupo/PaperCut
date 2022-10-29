# Classes for the different types of cards
# Current card types : Object, Enemy, Player, Setting, NPC
import pygame as pg
import time
import copy

class Card:
    def __init__(self, game, card_image, name='Base Card', description='This is a base card'):
        self.game = game
        self.settings = game.settings
        self.screen = self.game.screen
        self.name = name
        self.description = description
        self.card_image = card_image
        self.rect = self.card_image.get_rect()
        self.rect.clamp_ip(self.settings.play_area_rect)
        self.accepted_cards = None
        # a list of what the card can interact with
        self.targets = []

    # moves the card when the user drags it around
    # this is used by the createcards class
    def drag(self):
        self.rect.center = pg.mouse.get_pos()
        self.rect.clamp_ip(self.settings.play_area_rect)

    # highlight the borders around the card
    def highlight(self):
        pass

    # checks if the card was dropped on a target and if it is valid
    def check_target(self):
        pass

    def __repr__(self):
        return repr(str(type(self)) + ' ' + self.name + str(self.rect.center))

    def draw(self):
        self.screen.blit(self.card_image, (self.rect.x, self.rect.y))

    def update(self):
        self.draw()

class PlayerCard(Card):
    def __init__(self, game, card_image, name, description):
        super().__init__(game, card_image, name, description)
        self.health = 10
        self.damage = 5

class EnemyCard(Card):
    def __init__(self, game, card_image, name='Enemy Card', description='This is an enemy card', health = 1, damage = 1): 
        super().__init__(game, card_image, name, description)
        self.health = health
        self.damage = damage


# event_card param : cards that are to be spawned upon trigger_event()
#   only duplicates of these cards are created
# accepted cards param : list of cards that can interact with this card
# duration param : seconds to run progress bar
class SettingCard(Card):
    def __init__(self, game ,card_image, name='Setting Card', description='This is a setting card', 
                 duration = 1, accepted_cards = None, event_cards = None):
        super().__init__(game, card_image, name, description)
        # list of cards that can interact with this card
        self.accepted_cards = accepted_cards
        self.event_cards = event_cards
        self.rect.x = 100
        self.rect.y = 100
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.bar_color = (0, 0, 255)
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

    # spawns cards in event_cards into play
    def trigger_event(self):
        for card in self.event_cards:
            if type(card) is EnemyCard and card:
                enemy_copy = EnemyCard(self.game, card.card_image)
                enemy_copy.rect.center = self.rect.center
                enemy_copy.rect.y += 20
                self.game.cards.update_list.append(enemy_copy)
                self.game.cards.all_cards.append(enemy_copy)

    def draw(self):
        super().draw()

    def update(self):
        super().update()
        self.progress_bar()
        self.draw()