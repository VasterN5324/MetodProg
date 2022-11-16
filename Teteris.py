from _curses import *
import pygame as pg
from copy import deepcopy
from random import choice, randrange


W, H = 10, 15
TILE = 35
GAME_RES = W*TILE, H*TILE
RES = 600,525
FPS = 60
RES_1 = 50,50

pg.init()
game_sc = pg.display.set_mode(RES)
sc = pg.Surface(GAME_RES)
clock = pg.time.Clock()
score_label = pg.Surface(RES_1)
grid = [pg.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
font = pg.font.Font(None,100)
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pg.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pg.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]
GO = font.render('Game Over(', True, pg.Color('green'))
ft = pg.font.Font(None,70)
title_score= font.render('score', True, pg.Color('white'))

score, lines = 0, 0
scores = {0: 0, 1:1, 2:3, 3:7, 4:15}

anim_count, anim_speed, anim_limit = 0, 60, 2000
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
# Обозначение поля
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx, rotate = 0, False
    score_label.fill(pg.Color('White'))
    game_sc.fill(pg.Color('Black'))
    # Контроль
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                dx = -1
            elif event.key == pg.K_RIGHT:
                dx = 1
            elif event.key == pg.K_DOWN:
                anim_limit = 100
            elif event.key == pg.K_UP:
                rotate = True
            if event.key ==pg.K_SPACE:
                field = [[0 for i in range(W)] for j in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
 # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = pg.Color('White')
                figure = next_figure
                next_figure = deepcopy(choice(figures))
                anim_limit = 2000
                break     
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    score += scores[lines]        
     # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pg.draw.rect(game_sc, pg.Color("White"), figure_rect)
    # darw grid
    [pg.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # draw next_figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 300
        figure_rect.y = next_figure[i].y * TILE + 50
        pg.draw.rect(game_sc, pg.Color("White"), figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pg.draw.rect(game_sc, col, figure_rect)
    #restart
    
    # game over
    for i in range(W):
        if field[0][i]:
            game_sc.blit(GO, (100, 170))
            anim_count, anim_speed, anim_limit = 0, 0, 0
    
    game_sc.blit(title_score, (400, 350))
    game_sc.blit(font.render(str(score), True, pg.Color('white')), (400,400))
    pg.display.flip()
    clock.tick(FPS)                 
    
                
                
                