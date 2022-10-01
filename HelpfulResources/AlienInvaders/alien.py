import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from timer import Timer
import random

class Alien(Sprite):
    alien_explosion_images = [pg.image.load(f'images/explode{n}.png') for n in range(7)]
    
    def __init__(self, settings, screen, alien_images, alien_lasers, sound):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pg.image.load('images/UFOAlien0.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.alien_images = alien_images
        self.lasers = alien_lasers
        self.sound = sound
        self.dying = self.dead = False
        self.death_sound = pg.mixer.Sound('sounds/death.wav')
        self.death_sound.set_volume(.6)
        self.timer_normal = Timer(image_list=self.alien_images)              
        self.timer_explosion = Timer(image_list=self.alien_explosion_images, is_loop=False)  
        self.timer = self.timer_normal                                    
    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)
    def hit(self):
        self.death_sound.play(0)
        self.dying = True 
        self.timer = self.timer_explosion
    def alien_shoot(self):
        self.lasers.shoot(settings=self.settings, screen=self.screen,
                                ship=self, sound=self.sound)
    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)

class Aliens:
    def __init__(self, game, screen, settings, lasers: Lasers, ship, alien_images1, alien_images2, alien_images3, alien_lasers: Lasers, sound): 
        self.sound = sound        
        self.alien_images1 = alien_images1
        self.alien_images2 = alien_images2
        self.alien_images3 = alien_images3
        self.model_alien = Alien(settings=settings, screen=screen, alien_images=alien_images1, alien_lasers=alien_lasers, sound=sound)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()
        self.lasers = lasers.lasers
        self.alien_lasers = alien_lasers
        self.screen = screen
        self.settings = settings
        self.ship = ship
        self.create_fleet()
    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x
    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (alien_height * 5))
        return number_rows        
    def reset(self):
        self.aliens.empty()
        self.create_fleet()
    def create_alien(self, alien_number, row_number, alien_images):
        alien = Alien(settings=self.settings, screen=self.screen, alien_images=alien_images, alien_lasers=self.alien_lasers, sound=self.sound)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number 
        self.aliens.add(alien)     
    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(int(number_rows / 3)):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number, self.alien_images1)
        for row_number in range(int(number_rows / 3), int(2 * number_rows / 3)):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number, self.alien_images2)
        for row_number in range(int(2 * number_rows / 3), int(number_rows)):
             for alien_number in range(number_aliens_x):
                 self.create_alien(alien_number, row_number, self.alien_images3)
    def check_fleet_edges(self):
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self.change_fleet_direction()
                break
    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.die()
                break
    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.game.reset()
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def check_collisions(self):  
        collisions = pg.sprite.groupcollide(self.aliens, self.lasers, False, True)  
        if collisions:
            for alien in collisions:
                alien.hit()
            self.sb.increment_score(self.settings.alien_points)
    def shoot(self):
        if random.randint(0, self.settings.alien_fire_rate) < 1:
            random.choice(self.aliens.sprites()).alien_shoot()
    def update(self): 
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot()
        for alien in self.aliens.sprites():
            if alien.dead:
                alien.remove()
            alien.update() 
    def draw(self): 
        for alien in self.aliens.sprites(): 
            alien.draw() 

class BigAlien(Sprite):
    alien_explosion_images = [pg.image.load(f'images/PointExplode{n}.png') for n in range(1, 8)]
    def __init__(self, settings, screen, alien_images):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pg.image.load('images/PointsUFO0.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.alien_images = alien_images
        self.dead = True
        self.count = 0
        self.font = pg.font.Font('images/font0.ttf', 20)
        self.text = self.font.render(str(settings.big_alien_points), True, (255, 255, 255), self.settings.bg_color)
        self.text_rect = self.text.get_rect()
        self.death_sound = pg.mixer.Sound('sounds/Explosion.wav')
        self.death_sound.set_volume(.4)
        self.timer_normal = Timer(image_list = self.alien_images)              
        self.timer_explosion = Timer(image_list=self.alien_explosion_images, is_loop=False)  
        self.timer = self.timer_normal
    def hit(self):
        self.death_sound.play(0)
        self.timer = self.timer_explosion
    def check_edge(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right
    def display_points(self):
        self.text_rect.center = (self.x, self.rect.top)
        self.screen.blit(self.text, self.text_rect)
    def update(self): 
        if (self.timer == self.timer_explosion and self.timer.is_expired()) or self.check_edge():
            self.kill()
        else:
            settings = self.settings
            self.x += (settings.alien_speed_factor * .3)
            self.rect.x = self.x
            self.draw()
    def draw(self):
            image = self.timer.image()
            rect = image.get_rect()
            rect.left, rect.top = self.rect.left, self.rect.top
            self.screen.blit(image, rect)

class BigAliens:
    def __init__(self, settings, screen, alien_images, lasers: Lasers, scoreboard):
        self.settings = settings
        self.screen = screen
        self.alien_images = alien_images
        self.lasers = lasers.lasers
        self.sb = scoreboard
        self.big_alien = Group()
        self.dead = True
        self.oscil_sound = pg.mixer.Sound('sounds/oscil.wav')
        self.oscil_sound.set_volume(.3)

    def check_collisions(self):
        if len(self.lasers) != 0:
            collisions = pg.sprite.groupcollide(self.big_alien, self.lasers, False, True)  
            if collisions:
                for alien in collisions:
                    alien.hit()
                    self.dead = True
                self.sb.increment_score(self.settings.big_alien_points)
    def try_spawn(self):
        if random.randint(0, 1500) < 1 and self.count < 1:
            self.count += 1
            alien = BigAlien(settings = self.settings, screen = self.screen, alien_images = self.alien_images)
            self.big_alien.add(alien)
            self.dead = False
            self.oscil_sound.play()
    def reset(self):
        self.dead = True
        self.big_alien = Group()
    def update(self):
        if(self.dead == True or len(self.big_alien) == 0):
            self.oscil_sound.stop()
            self.big_alien.remove()
            self.count = 0
            for alien in self.big_alien:
                alien.display_points()
                alien.remove()
                alien.update()
            self.try_spawn()
        else:
            self.check_collisions()
            for alien in self.big_alien:
                alien.update()
       
