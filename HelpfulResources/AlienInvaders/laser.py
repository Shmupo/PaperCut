import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint
from timer import Timer

class Lasers:
    def __init__(self, settings, laser_images, speed_factor):
        self.lasers = Group()
        self.settings = settings
        self.laser_images = laser_images
        self.speed_factor = speed_factor
    def reset(self):
        self.lasers.empty()        
    def shoot(self, settings, screen, ship, sound):
        self.lasers.add(Laser(settings=settings, screen=screen, ship=ship, 
                              sound=sound, laser_images = self.laser_images, speed_factor=self.speed_factor))
    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0 or laser.rect.top >= self.settings.screen_height: self.lasers.remove(laser)
    def draw(self):
        for laser in self.lasers.sprites(): laser.draw()

class Laser(Sprite):
    """A class to manage lasers fired from the ship"""
    def __init__(self, settings, screen, ship, sound, laser_images, speed_factor):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load('images/Laser1.png')
        self.laser_images = laser_images
        self.timer_normal = Timer(image_list=self.laser_images)
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.speed_factor = speed_factor
        self.timer = Timer(image_list=self.laser_images)      
        sound.shoot_laser()
    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
        self.draw()
    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
