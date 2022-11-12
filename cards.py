# Classes for the different types of cards
# Current card types : Object, Enemy, Player, Setting, NPC

import pygame as pg
import time

class Card:
    def __init__(self, game, card_image, name='Base Card', description='This is a base card', accepted_cards=None):
        self.delete = False
        self.game = game
        self.settings = game.settings
        self.screen = self.game.screen
        self.name = name
        self.description = description
        self.card_image = card_image
        self.rect = self.card_image.get_rect()
        self.rect.clamp_ip(self.settings.play_area_rect)
        self.accepted_cards = accepted_cards
        # a list of what the card can interact with
        self.targets = []
        self.highlight_rect = pg.Rect(self.rect.x-5, self.rect.y-5, self.rect.width + 10, self.rect.height + 10)
        self.highlight_color = (0, 150, 0)

    # moves the card when the user drags it around
    # this is used by the createcards class
    def drag(self):
        self.rect.center = pg.mouse.get_pos()
        self.rect.clamp_ip(self.settings.play_area_rect)

    # highlight the borders around the card
    def highlight(self, color=None):
        self.highlight_rect.clamp_ip(self.rect)
        if color == None:
            pg.draw.rect(self.screen, self.highlight_color, self.highlight_rect, border_radius=10)
        else: pg.draw.rect(self.screen, color, self.highlight_rect, border_radius=10)

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
        self.damage = 10

    def display_health(self):
        width = 3
        len = 9
        health = self.health
        red_bar_length = 0 # damage received
        y_val = 118
        for i in range(0, health):
            pg.draw.rect(self.screen, (0, 255, 0), (self.rect.x-5, self.rect.y+y_val, width, len))
            y_val -= 13
        #pg.draw.rect(self.screen, (0, 255, 0), (self.rect.x-10, self.rect.y, width, 128)) # green bar
        #pg.draw.rect(self.screen, (255, 0, 0), (self.rect.x-10, self.rect.y, width, red_bar_length)) # red bar
        # place bar on the left side

    def display_attack(self):
        width = 3
        len = 9
        attack_point = self.damage
        y_val = 118
        for i in range(0, attack_point):
            pg.draw.rect(self.screen, (255, 0, 0), (self.rect.x-10, self.rect.y+y_val, width, len))
            y_val -= 13
        #pg.draw.rect(self.screen, (255, 255, 255), (self.rect.x-5, self.rect.y, width, 128)) # white bar
        #pg.draw.rect(self.screen, (0, 0, 0), (self.rect.x-5, self.rect.y, width, blk_bar_length)) # black bar
        # place bar o the right side

    def update(self):
        print("HEALTH:", self.health)
        self.draw()
        self.display_health()
        self.display_attack()

class EnemyCard(Card):
    def __init__(self, game, card_image, name='Enemy Card', description='This is an enemy card', accepted_cards=None, health = 1, damage = 1): 
        super().__init__(game, card_image, name, description, accepted_cards)
        self.health = health
        self.damage = damage
        self.highlight_color = (150, 0, 0)

    def display_health(self):
        width = 3
        len = 9
        health = self.health
        y_val = 118
        for i in range(0, health):
            pg.draw.rect(self.screen, (0, 255, 0), (self.rect.x+96, self.rect.y+y_val, width, len))
            y_val -= 13
        #pg.draw.rect(self.screen, (0, 255, 0), (self.rect.x+101, self.rect.y, width, 128)) # green bar
        #pg.draw.rect(self.screen, (255, 0, 0), (self.rect.x+101, self.rect.y, width, red_bar_length)) # red bar
        # place bar on the left side

    def display_attack(self):
        width = 3
        len = 9
        attack_point = self.damage
        y_val = 118
        for i in range(0, attack_point):
            pg.draw.rect(self.screen, (255, 0, 0), (self.rect.x+101, self.rect.y+y_val, width, len))
            y_val -= 13


        #pg.draw.rect(self.screen, (255, 255, 255), (self.rect.x+96, self.rect.y, width, 128)) # white bar
        #pg.draw.rect(self.screen, (0, 0, 0), (self.rect.x+96, self.rect.y, width, blk_bar_length)) # black bar
        # place bar o the right side

    def update(self):
        print("HEALTH:", self.health)
        self.draw()
        self.display_health()
        self.display_attack()


# event_card param : cards that are to be spawned upon trigger_event()
#       only duplicates of these cards are created
# accepted cards param : list of cards that can interact with this card
# duration param : seconds to run progress bar
class SettingCard(Card):
    def __init__(self, game ,card_image, name='Setting Card', description='This is a setting card', 
                 duration = 1, accepted_cards = None, event_cards = None):
        super().__init__(game, card_image, name, description, accepted_cards)
        # list of cards that can interact with this card
        self.event_cards = event_cards
        self.rect.x = 100
        self.rect.y = 100
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.bar_color = (0, 0, 255)
        self.duration = duration
        self.start_time = None
        self.time_progress = 0
        self.progress_rect = pg.Rect(self.rect.x, self.rect.y - 10, 0, 5)
        self.active = False

    def progress_bar(self):
        self.progress_rect.x = self.rect.x
        self.progress_rect.y = self.rect.y - 10
      
        if self.start_time == None: self.start_time = time.time()
        current_time = time.time()

        if current_time - self.start_time > self.time_progress and self.time_progress < self.duration:
            self.progress_rect.width += self.rect.width / self.duration
            self.time_progress += 1
        elif self.time_progress == self.duration: 
            self.start_time = None
            self.time_progress = 0
            self.trigger_event()
            self.progress_rect.width = 0

        pg.draw.rect(self.screen, self.bar_color, self.progress_rect, 5)

    # activate the setting card
    def activate(self, activate = True):
        self.active = activate

    # spawns cards in event_cards into play
    def trigger_event(self):
        for card in self.event_cards:
            if type(card) is EnemyCard:
                enemy_copy = EnemyCard(self.game, card.card_image, card.name, card.description, card.accepted_cards)
                enemy_copy.rect.center = (self.rect.x + self.rect.width / 2, self.rect.y + 190)
                enemy_copy.rect.y += 20
                self.game.cards.update_list.append(enemy_copy)
                self.game.cards.all_cards.append(enemy_copy)

    def update(self):
        super().update()
        if self.active:
            self.progress_bar()
        self.draw()

class ConsumableCard(Card):
    def __init__(self, game ,card_image, name='Consumable Card', description='This is a consumable card', accepted_cards = None, event_cards = None):
        super().__init__(game, card_image, name, description, accepted_cards)
        #restore 1 heatlh or 1 attack default value for now
        self.player_card = None
        self.health = 1
        self.attack = 1

    #restore health/attack of player
    def consume(self,player_card):
        self.player_card = player_card
        self.player_card.health += self.health
        self.player_card.damage += self.attack
        #remove effect
        self.health = 0
        self.attack = 0
        #delete card
        self.delete = True
    
    def update(self):
        super().update()
        self.draw()
 
        