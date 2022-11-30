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
        # PLAYER
        self.card_image = pg.transform.scale(pg.image.load('images/playercard.png'), self.card_size)
        self.player_card = PlayerCard(self.game, self.card_image, 'Player', 
                                'Your best friend was a magical beetle. Now you wear his skull so that he is always with you. Rest in peace Moe.')
        self.update_list.append(self.player_card)
        self.all_cards.append(self.player_card)
        self.player_card.rect.x = 150
        self.player_card.rect.y = 350

        # CONSUMABLES
        self.milk_image = pg.transform.scale(pg.image.load('images/MilkCard.png'), self.card_size)
        self.milk_card = ConsumableCard(self.game, self.milk_image, 'Milk',
                                        description='Nothing like having a carton of milk after a hard days work.',
                                        accepted_cards=[self.player_card], health=1,damage=1)

        self.shoe_image = pg.transform.scale(pg.image.load('images/ShoeCard.png'), self.card_size)
        self.shoe_card = ConsumableCard(self.game, self.shoe_image, 'Shoe',
                                        description='Comes with a free snake. He has a hat.')

        self.egg_image = pg.transform.scale(pg.image.load('images/EggCard.png'), self.card_size)
        self.egg_card = ConsumableCard(self.game, self.egg_image, 'Egg',
                                       description='Don\'t ask where it came from.',
                                       accepted_cards=[self.player_card], health=3,damage=2)

        self.spoon_image = pg.transform.scale(pg.image.load('images/SpoonCard.png'), self.card_size)
        self.spoon_card = ConsumableCard(self.game, self.spoon_image, 'Spoon',
                                        'You ate steak with this once.')

        self.fork_image = pg.transform.scale(pg.image.load('images/ForkCard.png'), self.card_size)
        self.fork_card = ConsumableCard(self.game, self.fork_image, 'Fork',
                                        'For when you want to poke things three times.', )

        self.knife_image = pg.transform.scale(pg.image.load('images/KnifeCard.png'), self.card_size)
        self.knife_card = ConsumableCard(self.game, self.knife_image, 'Knife',
                                        'A suitable armament for dinner.')

        self.goblin_image = pg.transform.scale(pg.image.load('images/GoblinCard.png'), self.card_size)
        self.goblin_card = EnemyCard(self.game, self.goblin_image, hp=2, dmg=2, accepted_cards=[self.player_card], name='Goblin', 
                                     description='Goblin has junk. Goblin minds own business.', loot_drop_chance=[.3, .3, .3], 
                                     loot_cards=[self.spoon_card, self.fork_card, self.knife_card])        

        self.dwarf_image = pg.transform.scale(pg.image.load('images/DwarfCard.png'), self.card_size)
        self.dwarf_card = EnemyCard(self.game, self.dwarf_image, hp=4, dmg= 2, accepted_cards=[self.player_card], name='Dwarf', 
                                    description='Rock and Stone!', loot_drop_chance=[.5], loot_cards=[self.shoe_card])

        self.shoes_image = pg.transform.scale(pg.image.load('images/ShoesCard.png'), self.card_size)
        self.shoes_card = NPCCard(self.game, self.shoes_image, [self.shoe_card], self.milk_card, 'Shoes', 'He takes shoes. Can\'t you tell?')

        self.moff_image = pg.transform.scale(pg.image.load('images/MoffCard.png'), self.card_size)
        self.moff_card = NPCCard(self.game, self.moff_image, [self.spoon_card, self.fork_card, self.knife_card, self.lamp_card],
                                 [self.egg_card, self.egg_card, self.egg_card, self.map_card], 'Moff', 'Desires shiny things. Give him another lamp.')

        self.lamp_image = pg.transform.scale(pg.image.load('images/LampCard.png'), self.card_size)
        self.lamp_card = ConsumableCard(self.game, self.lamp_image, 'Lamp',
                                        description='You are drawn to the flame.', accepted_cards=[self.player_card],
                                        transform_to=self.moff_card)

        self.moff_card.accepted_cards.append(self.lamp_card)

        self.gobo_image = pg.transform.scale(pg.image.load('images/GoboCard.png'), self.card_size)
        self.gobo_card = EnemyCard(self.game, self.gobo_image, hp=2, dmg=3, accepted_cards=[self.player_card], name='Gobo', 
                                   description='A meaner Goblin. He came prepared.', loot_drop_chance=[.5], 
                                   loot_cards=[self.lamp_card])

        self.shack_image = pg.transform.scale(pg.image.load('images/ShackCard.png'), self.card_size)
        self.shack_card = SettingCard(self.game, self.shack_image, 'Shack', 
                                      'This is where gobo and his family lives. It ain\'t much, but it\'s home.', duration=3, 
                                      accepted_cards=[self.player_card], event_cards=[self.gobo_card, self.goblin_card], 
                                      event_spawn_chance=[.3, .7], max_card_spawns=5)
        self.update_list.append(self.shack_card)
        self.all_cards.append(self.shack_card)
        self.shack_card.rect.x = 800
        self.shack_card.rect.y = 350

        self.mountain_image = pg.transform.scale(pg.image.load('images/MountainCard.png'), self.card_size)
        self.mountain_card = SettingCard(self.game, self.mountain_image, 'Mountain', 
                                      'Something grumbly lurks inside.', duration=5, 
                                      accepted_cards=[self.player_card], event_cards=[self.dwarf_card], 
                                      event_spawn_chance=[1], max_card_spawns=3)

        self.map_image = pg.transform.scale(pg.image.load('images/MapCard.png'), self.card_size)
        self.map_card = ConsumableCard(self.game, self.map_image, 'Map',
                                        description='This is a piece of cardboard...', accepted_cards=[self.player_card],
                                        transform_to=self.mountain_card)

        self.house_image = pg.transform.scale(pg.image.load('images/HouseCard.png'), self.card_size)
        self.house_card = SettingCard(self.game, self.house_image, 'House', 'Your mother lives here. Ask her nicely for milk.',
                                      duration=2, accepted_cards=[self.player_card], event_cards=[self.milk_card], event_spawn_chance=[1], max_card_spawns=5)
        self.all_cards.append(self.house_card)
        self.update_list.append(self.house_card)
        self.house_card.rect.x = 250
        self.house_card.rect.y = 350

        # FOR TESTING ###########################################################################################
        self.all_cards.append(self.lamp_card)
        self.update_list.append(self.lamp_card)
        self.update_list.append(self.fork_card)
        self.all_cards.append(self.fork_card)

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

    # Return the stack if the card is currently in a stack
    def is_in_stack(self, card):
        for stack in self.update_list:
            if type(stack) == CardStack:
                if card in stack.stack: return stack
        else: return None

    # detecting whether a card is dragged on another card to create a stack or add to existing stack
    # target is the card being hovered over, card_to_drag is the dragged card
    def check_drag_card_on_card(self):
        target = self.card_at_mouse()
        if self.card_to_drag != None and type(self.card_to_drag) != CardStack:
            if self.is_in_stack(target) and self.card_to_drag in target.accepted_cards:
                self.is_in_stack(target).add(self.card_to_drag)
            elif target and target.accepted_cards and self.card_to_drag in target.accepted_cards:
                pg.mixer.Channel(1).play(pg.mixer.Sound("sounds/fight.mp3"))
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
                    # if target is a stack of cards, check if user wants to drag the bottom off
                    if type(target) == CardStack:
                        if target.stack[-1].rect.collidepoint(pg.mouse.get_pos()):
                            pg.mixer.Channel(0).play(pg.mixer.Sound("sounds/select.wav"))
                            target.remove_bottom()
                            self.card_to_drag = target.stack[-1]
                        elif target.rect.collidepoint(pg.mouse.get_pos()):
                                pg.mixer.Channel(0).play(pg.mixer.Sound("sounds/select.wav"))
                                self.card_to_drag = target
                    elif target.rect.collidepoint(pg.mouse.get_pos()):
                            pg.mixer.Channel(0).play(pg.mixer.Sound("sounds/select.wav"))
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
            if type(card) == EnemyCard: card.display_stats()
            
        self.display_description()
        #print(self.last_card_at_mouse)