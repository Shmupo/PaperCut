import pygame as pg
from settings import Settings
import game_functions as gf
import menu

from laser import Lasers
from alien import *
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from barrier import Barriers

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/Eastward.wav")

        self.laser_images = [pg.image.load(f'images/Laser{n}.png') for n in range(1,3)]
        self.alien_laser_images = [pg.image.load(f'images/alien_laser{n}.png') for n in range(0,2)]

        self.alien_1 = [pg.image.load(f'images/UFOAlien{n}.png') for n in range(2)]
        self.alien_2 = [pg.image.load(f'images/HoverAlien{n}.png') for n in range(2)]
        self.alien_3 = [pg.image.load(f'images/TubeAlien{n}.png') for n in range(2)]

        self.point_alien_images = [pg.image.load(f'images/PointsUFO{n}.png') for n in range(5)]

        self.scoreboard = Scoreboard(game=self)  
        self.lasers = Lasers(settings=self.settings, laser_images = self.laser_images, speed_factor=self.settings.laser_speed_factor)
        self.alien_lasers = Lasers(settings=self.settings, laser_images = self.alien_laser_images, speed_factor=self.settings.laser_speed_factor * -1)
        self.ship = Ship(game=self, screen=self.screen, settings=self.settings, sound=self.sound, lasers=self.lasers, alien_lasers=self.alien_lasers)
        self.aliens = Aliens(game=self, screen=self.screen, settings=self.settings, lasers=self.lasers, ship=self.ship, 
                             alien_images1=self.alien_1, alien_images2=self.alien_2, alien_images3=self.alien_3, alien_lasers=self.alien_lasers, sound=self.sound)
        self.settings.initialize_speed_settings()

        self.big_alien = BigAliens(settings = self.settings, screen = self.screen, alien_images = self.point_alien_images,
                                 lasers = self.lasers, scoreboard = self.scoreboard)

        self.barriers = Barriers(game=self)

        self.running = True
        self.playing = False

    def reset(self):
        print('Resetting game...')
        self.lasers.reset()
        self.alien_lasers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.barriers.reset()
        self.big_alien.reset()
        self.playing = False

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        self.running = False
        self.playing = False

    def play(self):
        self.sound.play_bg()

        while self.running:
            if not self.playing:
                self.playing = menu.display_menu(self.screen, self)
            while self.playing:
                gf.check_events(settings=self.settings, ship=self.ship)
                self.screen.fill(self.settings.bg_color)
                self.ship.update()
                self.big_alien.update()
                self.aliens.update()
                self.lasers.update()
                self.alien_lasers.update()
                self.barriers.update()
                self.scoreboard.update()
                pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
