import pygame as pg

def display_menu(screen, game):

    alien_1 = game.alien_1[0]
    alien_2 = game.alien_2[0]
    alien_3 = game.alien_3[0]
    alien_4 = game.point_alien_images[0]

    title_f = pg.font.Font('images/font0.ttf', 45)
    prompt_f = pg.font.Font('images/font0.ttf', 20)
    score_f = pg.font.Font('images/font0.ttf', 30)

    title = title_f.render('Space Invaders', True, (255, 255, 255))
    prompt = prompt_f.render(f'Press mousebutton1 to start', True, (255, 255, 255))
    high_score = score_f.render((f'High Score : {game.scoreboard.high_score}'), True, (0, 255, 0))

    titleRect = title.get_rect()
    promptRect = prompt.get_rect()
    scoreRect = high_score.get_rect()

    screen_w = game.settings.screen_width
    screen_h = game.settings.screen_height

    titleRect.center = ( screen_w / 2, screen_h / 2 - 100 )
    promptRect.center = ( screen_w / 2, screen_h / 2 + 100 )
    scoreRect.center = ( screen_w / 2, screen_h / 2 - 50 )

    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                return True
        screen.fill((0, 0, 0))
        screen.blit(title, titleRect)
        screen.blit(prompt, promptRect)
        screen.blit(high_score, scoreRect)
        screen.blit(alien_1, (screen_w/2 - 100, screen_h/2))
        screen.blit(alien_2, (screen_w/2 - 50, screen_h/2))
        screen.blit(alien_3, (screen_w/2, screen_h/2))
        screen.blit(alien_4, (screen_w/2 + 100, screen_h/2))

        pg.display.flip()