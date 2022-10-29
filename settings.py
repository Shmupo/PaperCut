# game settings here

import pygame as pg

class Settings:
    def __init__(self):
        self.window_x = 1080
        self.window_y = 720
        
        self.play_area_rect = pg.Rect(10, 60, 1060, 650)

        self.card_size = (96, 128)
        self.menu_color = (85, 159, 248)
        self.font_color = (152, 249, 119)