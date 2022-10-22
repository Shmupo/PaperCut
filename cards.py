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
        self.collide = 0

    # moves the card when the user drags it around
    def check_drag(self):
        if self.rect.x < pg.mouse.get_pos()[0] < self.rect.x + self.rect.width and self.rect.y < pg.mouse.get_pos()[1] < self.rect.y + self.rect.height:
            if self.rect.collidepoint(self.rect.center) == pg.mouse.get_pos():
                self.rect.center = self.last_pos
                self.draw()
            
            elif pg.mouse.get_pressed()[0]:
                self.rect.center = pg.mouse.get_pos()
                self.collide = self.rect.collidepoint(self.rect.center)
                self.last_pos = self.rect.center
                



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
    def __init__(self, game, card_image, name='Enemy Card', description='This is an enemy card'): 
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


class SettingCard(Card):
    def __init__(self, game ,card_image, name='Setting Card', description='This is a setting card', duration = 0, accepted_cards = None, event = None):
        super().__init__(game, card_image, name, description)
        self.duration = duration
        # list of cards that can interact with this card
        self.accepted_cards = accepted_cards
        self.events = event
        self.rect.x = 100
        self.rect.y = 100
       ## self.border_rect = [5,25,80,10]
       ## self.inner_rect =[7,27.5,0,5]
        self.border_rect = [self.rect.x+5,self.rect.y+110,80,10]
        self.inner_rect =[self.rect.x+6,self.rect.y+112,0,5]
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.fps = 60
        self.speed = 5
        self.game = game
        self.settings = game.settings
        self.card_size = self.settings.card_size
        self.start_timer()


    # when triggered, create and start the progress bar
    def start_timer(self):
        clock = pg.time.Clock()
        clock.tick(self.fps)
    def trigger_event(self):
        self.inner_rect =[self.rect.x+6,self.rect.y+112,0,5]

        self.goblin_image = pg.image.load('images/GoblinCard.png')
        self.goblin_image = pg.transform.scale(self.goblin_image, self.game.settings.card_size)
        self.goblin_card = EnemyCard(self.game, self.goblin_image)
        self.game.update_card_list.append(self.goblin_card)
        self.start_timer()

    def draw(self):
        super().draw()

    def update(self):
        super().update()
        ##self.border_rect = [self.rect.x+5,self.rect.y+110,80,10]
        ##self.inner_rect =[self.rect.x+6,self.rect.y+112,0,5]
        if self.inner_rect[2] < 76:
            self.inner_rect[2] += (self.speed/self.fps)

            pg.draw.rect(self.screen,self.red,self.border_rect, 3)
            pg.draw.rect(self.screen,self.green,(self.inner_rect[0],self.inner_rect[1],int(self.inner_rect[2]),self.inner_rect[3]))
           ## pg.display.flip()
        else:
            self.trigger_event()


class ObjectCard(Card):
    def __init__(self, game ,card_image, name='Object Card', description='This is an object card'):
        super().__init__(self, game, card_image, name, description)

    def replenish(self, EntityCard):
        pass

    def update(self):
        pass

    def draw(self):
        pass