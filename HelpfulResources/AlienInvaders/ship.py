import pygame as pg
from pygame.sprite import Sprite
from game_functions import clamp
from vector import Vector
from timer import Timer


class Ship(Sprite):
    def __init__(self, game, settings, screen, sound, lasers=None, alien_lasers=None):
        super().__init__()
        self.game = game
        self.screen = screen
        self.settings = settings
        self.sound = sound
        self.ships_left = settings.ship_limit  
        self.images = [pg.image.load(f'images/ship-{n}.png.png') for n in range(1,12)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.posn = self.center_ship()
        self.vel = Vector()
        self.lasers = lasers
        self.shooting = False
        self.lasers_attempted = 0
        self.alien_lasers = alien_lasers.lasers
        self.timer = Timer(image_list = self.images)  
    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10
        return Vector(self.rect.left, self.rect.top)
    def reset(self): 
        self.vel = Vector()
        self.posn = self.center_ship()
        self.rect.left, self.rect.top = self.posn.x, self.posn.y
    def die(self):
        self.ships_left -= 1
        print(f'Ship is dead! Only {self.ships_left} ships left')
        self.game.reset() if self.ships_left > 0 else self.game.game_over()
    def check_collisions(self):  
        collisions = pg.sprite.groupcollide([self], self.alien_lasers, False, True)  
        if collisions:
            self.die()
    def update(self):
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(settings=self.settings, screen=self.screen,
                                ship=self, sound=self.sound)
        self.draw()
        self.check_collisions()
    def draw(self): 
        self.image = self.timer.image()
        self.screen.blit(self.image, self.rect)
