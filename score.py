import pygame as pg


class Score():
    def __init__(self, point):
        self.point = point

    def display_score(self):
        score = 3
        x_pos = 870
        y_pos = 10
        if score > 9999:
            x_pos -= 80
        elif score > 999:
            x_pos -= 60
        elif score > 99:
            x_pos -= 40
        elif score > 9:
            x_pos -= 20
        comicsans = pg.font.SysFont('comicsans', 30, True)
        text = comicsans.render('High Score ' + str(score), 1, (0,0,0))
        self.screen.blit(text, (x_pos, y_pos))

    def update(self):
        self.display_score()

