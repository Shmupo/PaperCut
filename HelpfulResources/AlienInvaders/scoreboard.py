import pygame as pg 

class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.level = 0
        self.score_file = open('score.txt', 'r')
        self.high_score = self.score_file.read()
        self.settings = game.settings
        self.points = game.settings.alien_points
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)
        self.score_image = None 
        self.score_rect = None
        self.high_score_image = None 
        self.high_score_rect = None
        self.prep_score()

    def increment_score(self, points): 
        self.score += points
        self.score_file = open('score.txt', 'r')
        self.high_score = self.score_file.readlines()[0]
        if self.score > int(float(self.high_score)):
            del self.high_score
            self.high_score = self.score
            self.score_file = open('score.txt', 'w+')
            self.score_file.write(str(self.high_score))
            self.score_file.close()
        self.prep_score()

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        high_score_str = str(self.high_score)
        self.high_score_image = self.font.render(high_score_str, True, (255, 0, 0), self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.top = 100
    def reset(self): 
        self.score = 0
        self.update()
    def update(self): 
        self.draw()
    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)