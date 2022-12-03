import pygame as pg

class Score():
    def __init__(self, game):
        self.points = 0
        self.x_pos = 10
        self.y_pos = 10
        self.comicsans = pg.font.SysFont('comicsans', 30, True)
        self.text = self.comicsans.render('Score ' + str(self.points), 1, (0,0,0))
        self.screen = game.screen

        self.screen.blit(self.text, (self.x_pos, self.y_pos))

    def update_points(self, score):
        self.points += score
        self.text = self.comicsans.render('Score : ' + str(self.points), 1, (0,0,0))

    def update(self):
        self.screen.blit(self.text, (self.x_pos, self.y_pos))
