# Classes for the different types of cards
# Current card types : Object, Enemy, Player, Setting, NPC

from pickletools import stackslice
import pygame as pg
import time
import random

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

    def __repr__(self):
        return repr(str(type(self)) + ' ' + self.name + str(self.rect.center))

    def draw(self):
        self.screen.blit(self.card_image, (self.rect.x, self.rect.y))

    def update(self):
        self.draw()
        

class PlayerCard(Card):
    def __init__(self, game, card_image, name, description):
        super().__init__(game, card_image, name, description)
        self.max_health = 10
        self.max_damage = 5
        self.health = 10
        self.damage = 5

    # player attacks the given card
    def attack(self, card):
        enemy_damage = card.damage
        card.take_damage(self.damage)
        if self.damage > 1: self.damage -= 1
        
        self.health -= enemy_damage
        if self.health <= 0:
            self.health = 0
            self.die()

    # keeps health/damage stats within max boundaries
    def consume_item(self, card):
        if type(card) == ConsumableCard:
            if self.health + card.health >= self.max_health:
                self.health = 10
            elif self.max_health + card.health <= 0:
                self.health = 0
                self.die()
            else: self.health += card.health

            if self.damage + card.damage >= self.max_damage:
                self.damage = 5
            elif self.damage + card.damage <= 1:
                self.damage = 1
            else: self.damage += card.damage
            card.consume()

    # this is called whenever player health reaches 0
    def die(self):
        pass

    def display_health(self):
        y_val = 118
        for _ in range(self.health):
            pg.draw.rect(self.screen, (255, 0, 0), (self.rect.x-8, self.rect.y+y_val, 6, 9))
            y_val -= 13

    def display_attack(self):
        y_val = 118
        for _ in range(self.damage):
            pg.draw.rect(self.screen, (0, 0, 255), (self.rect.x-16, self.rect.y+y_val, 6, 9))
            y_val -= 13

    def update(self):
        self.draw()
        self.display_health()
        self.display_attack()


# The accepted_cards variable is a dict for this class - the value of dict is what the NPC gives for the given key of the dict
class NPCCard(Card):
    def __init__(self, game, card_image, accepted_cards, return_card, name, description): 
        super().__init__(game, card_image, name, description, accepted_cards)
        self.return_card = return_card

    def spawn_card(self, card):
        if card in self.accepted_cards:
            copy = self.return_card[card.name]
            return_copy = ConsumableCard(self.game, copy.card_image, copy.name, 
                                         copy.description, copy.accepted_cards, copy.health, copy.damage, None)

            return_copy.rect.center = (self.rect.x + self.rect.width / 2, self.rect.y + 190)
            return_copy.rect.y += 20
            self.game.cards.update_list.append(return_copy)
            self.game.cards.all_cards.append(return_copy)

    def update_accepted_cards(self):
        for card in self.accepted_cards:
            for element in self.game.cards.update_list:
                if type(element) == ConsumableCard: 
                    if card.name == element.name and element not in self.accepted_cards:
                        self.accepted_cards.append(element)

    def consume_item(self, card):
        self.spawn_card(card)
        card.consume()

    def update(self):
        self.update_accepted_cards()
        self.draw()


class EnemyCard(Card):
    def __init__(self, game, card_image, hp, dmg, accepted_cards, name, description, loot_drop_chance, loot_cards): 
        super().__init__(game, card_image, name, description, accepted_cards)
        self.health = hp
        self.damage = dmg
        self.highlight_color = (150, 0, 0)
        self.loot_drop_chance = loot_drop_chance
        self.loot_cards = loot_cards

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()

    def display_stats(self):
        y_val = 118
        for _ in range(self.damage):
            pg.draw.rect(self.screen, (0, 0, 255), (self.rect.x+106, self.rect.y+y_val, 6, 9))
            y_val -= 13
        
        y_val = 118
        for _ in range(self.health):
            pg.draw.rect(self.screen, (255, 0, 0), (self.rect.x+98, self.rect.y+y_val, 6, 9))
            y_val -= 13

    # checks if card is dead or not
    def die(self):
        self.drop_loot()
        card_stack = self.game.cards.is_in_stack(self)
        card_stack.remove_card(self)
        self.game.cards.all_cards.remove(self)
        self.game.cards.update_list.remove(self)

    # chooses a loot card to drop based on probabilities
    # return None when no card is chosen
    def choose_loot(self):
        if self.loot_cards != None:
            for card in self.loot_cards:
                roll = random.random()
                if roll < self.loot_drop_chance[self.loot_cards.index(card)]:
                    return card
            else: return None
        else: return None

    def drop_loot(self):
        card = self.choose_loot()
        if card != None:
            copy = ConsumableCard(self.game ,card.card_image, card.name, card.description, card.accepted_cards, card.health, card.damage, card.transform_to)
            copy.rect.center = (self.rect.x + self.rect.width / 2, self.rect.y + 190)
            copy.rect.y += 20
            self.game.cards.update_list.append(copy)
            self.game.cards.all_cards.append(copy)

    # when other goblin cards are made, add them to the accepted_cards list
    def update_accepted_cards(self):
        for card in self.game.cards.update_list:
            if type(card) == EnemyCard and card.name == self.name:
                if card not in self.accepted_cards:
                    self.accepted_cards.append(card)

    def update(self):
        self.update_accepted_cards()
        self.draw()


# event_card param : list of cards that are to be spawned upon trigger_event()
#       only duplicates of these cards are created,
# event_spawn_chance: list of percentages to spawn cards
# accepted cards param : list of cards that can interact with this card
# duration param : seconds to run progress bar
class SettingCard(Card):
    def __init__(self, game ,card_image, name='Setting Card', description='This is a setting card', 
                 duration = 1, accepted_cards = None, event_cards = None, event_spawn_chance = None, max_card_spawns=0):
        super().__init__(game, card_image, name, description, accepted_cards)
        # list of cards that can interact with this card
        self.event_cards = event_cards
        self.event_spawn_chance = event_spawn_chance
        self.rect.x = 100
        self.rect.y = 100
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.bar_color = (0, 0, 255)
        self.max_card_spawns = max_card_spawns
        self.spawned_cards = []
        self.duration = duration
        self.start_time = None
        self.time_progress = 0
        self.progress_rect = pg.Rect(self.rect.x, self.rect.y - 10, 0, 5)
        self.active = False

    def progress_bar(self):
        if self.active == False and self.time_progress != 0: 
            self.time_progress = 0
            self.start_time = None
            self.progress_rect.width = 0
        elif self.active: 
            self.progress_rect.x = self.rect.x
            self.progress_rect.y = self.rect.y - 10
  
            if self.start_time == None: self.start_time = time.time()
            current_time = time.time()

            if self.max_card_spawns > len(self.spawned_cards):
                if current_time - self.start_time > self.time_progress and self.time_progress < self.duration:
                    self.progress_rect.width += self.rect.width / self.duration
                    self.time_progress += 1
                elif self.time_progress == self.duration: 
                    self.start_time = None
                    self.time_progress = 0
                    self.trigger_event()
                    self.progress_rect.width = 0
            else: 
                self.active = False
                self.start_time = None

            pg.draw.rect(self.screen, self.bar_color, self.progress_rect, 5)

    # activate the setting card
    def activate(self, activate = True):
        self.active = activate

    # runs the probabilites within event_spawn_chance and returns the card chosen
    # make sure the card probabilities are ordered in ascending order
    def choose_event(self):
        roll = random.random()
        for chance in self.event_spawn_chance:
            if roll < chance:
                return self.event_cards[self.event_spawn_chance.index(chance)]
        else: return self.event_cards[-1]

    # spawns cards in event_cards into play according to percent chances
    def trigger_event(self):
        card = self.choose_event()
        copy = None
            
        if type(card) == EnemyCard:
            copy = EnemyCard(self.game, card.card_image, card.health, card.damage, card.accepted_cards, card.name, 
                             card.description, card.loot_drop_chance, card.loot_cards)
        elif type(card) == ConsumableCard:
            copy = ConsumableCard(self.game, card.card_image, card.name, card.description, card.accepted_cards,card.health,card.damage)

        if copy:
            copy.rect.center = (self.rect.x + self.rect.width / 2, self.rect.y + 190)
            copy.rect.y += 20
            self.game.cards.update_list.append(copy)
            self.game.cards.all_cards.append(copy)
            self.spawned_cards.append(copy)

    # keeps track of whether the cards spawned are despawned or not
    def check_spawned_cards(self):
        for card in self.spawned_cards:
            if card not in self.game.cards.update_list and not self.game.cards.is_in_stack(card):
                self.spawned_cards.remove(card)

    def update(self):
        super().update()
        self.progress_bar()
        self.check_spawned_cards()
        self.draw()


class ConsumableCard(Card):
    def __init__(self, game ,card_image, name, description, 
                 accepted_cards = [], health = 0, damage = 0, transform_to = None):
        super().__init__(game, card_image, name, description, accepted_cards)
        self.health = health
        self.damage = damage
        self.transform_to = transform_to

    # remove this card from play
    def consume(self):
        if self.transform_to != None:
            self.transform()
        card_stack = self.game.cards.is_in_stack(self)
        card_stack.remove_card(self)
        self.game.cards.all_cards.remove(self)
        self.game.cards.update_list.remove(self)

    # delete this card and spawn the transform_to card in its place
    def transform(self):
        self.game.cards.all_cards.append(self.transform_to)
        self.game.cards.update_list.append(self.transform_to)
        self.transform_to.rect.x = self.rect.x
        self.transform_to.rect.y = self.rect.y - 20

    # allows same cards to stack
    def update_accepted_cards(self):
        for card in self.game.cards.update_list:
            if type(card) == ConsumableCard and card.name == self.name:
                if card not in self.accepted_cards:
                    self.accepted_cards.append(card)
    
    def update(self):
        super().update()
        self.update_accepted_cards()
        self.draw()
 
        