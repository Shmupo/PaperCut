import pygame as pg
from  pygame.sprite import Sprite
from pygame.sprite import Group

class Barrier(Sprite):
    color = (255, 0, 0, 0)
    black = (0, 0, 0)
    def __init__(self, game, rect):
        super().__init__()
        self.screen = game.screen
        self.rect = rect
        self.hp = game.settings.barrier_hp
        self.size = (self.rect.width, self.rect.height)
        self.surface = pg.Surface(self.size)
        self.surface.fill(Barrier.color)
        self.alpha = 255
    def hit(self):
        self.hp = self.hp - 1
        self.alpha = self.alpha - 30
        self.surface.set_alpha(self.alpha)
    def update(self):
        self.draw()
    def draw(self):
        self.screen.blit(self.surface, (self.rect.x, self.rect.y))
        pg.draw.circle(self.screen, Barrier.black, (self.rect.centerx, self.rect.bottom), self.rect.width/4.2)

class Barriers:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.lasers = game.lasers.lasers
        self.alien_lasers = game.alien_lasers.lasers
        width = self.settings.screen_width / 12
        height = 2 * width / 4
        top = self.settings.screen_height - height * 3
        self.rects = [pg.Rect(x * width * 3 + width, top, width, height) for x in range(4)]
        self.barriers = Group()
        self.barriers.add(Barrier(game = game, rect=i) for i in self.rects)
    def check_collisions(self):  
        collisions = pg.sprite.groupcollide(self.barriers, self.lasers, False, True)  
        collisions2 = pg.sprite.groupcollide(self.barriers, self.alien_lasers, False, True)  
        if collisions:
            for barrier in collisions:
                barrier.hit()
        if collisions2:
            for barrier in collisions2:
                barrier.hit()
    def reset(self): 
        self.barriers.add(Barrier(game=self.game, rect=i) for i in self.rects)
    def update(self):
        self.check_collisions()
        for barrier in self.barriers:
            if barrier.hp > 1:
                barrier.update()
            else: self.barriers.remove(barrier)