import pygame
from figures import figures_pos
from copy import deepcopy
from random import choice, randrange

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
FPS = 60
RES = 750, 940

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) 
                for x, y in fig_pos] 
                for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H + 1)]
anim_count, anim_speed, anim_limit = 0, 10, 2000
score, lines = 0, 0

main_font = pygame.font.SysFont('Comic Sans MS', 65)
font = pygame.font.SysFont('Comic Sans MS', 45)
main_font_color = pygame.Color('darkorange')
add_font_color = pygame.Color('darkgreen')

title = {'text': main_font.render('TETRIS', True, main_font_color), 'x': 485, 'y': 10}



get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()


scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

def check_floor():
    if figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx, rotate = 0, False
    sc.fill(pygame.Color('lightblue'))
    sc.blit(game_sc, (20, 20))
    game_sc.fill(pygame.Color('black'))
    #delay for full lines
    for i in range(lines):
        pygame.time.wait(100)

    #control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
    #move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx  
        if not check_borders():
            figure = deepcopy(figure_old)
            break      
    #move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_floor():
                for j in range(4):
                    field[figure_old[j].y][figure_old[j].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
    #rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders() or not check_floor():
                figure = deepcopy(figure_old)
                break
    #check lines
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
            lines += 1
    # count score
    score += scores[lines]
    if lines > 0: anim_speed += 1 
    #draw grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    #draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    #draw field
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    #draw next figure
    sc.blit(font.render('Next Figure', True, main_font_color),
            (title['x'], title['y']+100))
    pygame.draw.rect(sc, (40, 40, 40) , pygame.Rect(title['x'] + 25, title['y'] + 175, 210, 160), 0)
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + title['x'] - 95
        figure_rect.y = next_figure[i].y * TILE + title['y'] + 185
        pygame.draw.rect(sc, next_color, figure_rect)

    #draw titles
    sc.blit(title['text'], (title['x'], title['y']))
    sc.blit(font.render('SCORE', True, main_font_color),
            (title['x'] + 50, title['y'] + 650))
    sc.blit(font.render(str(score), True, add_font_color),
            (title['x'] + 90, title['y'] + 710))
    pygame.display.flip()

    #gameover
    for i in range(W):
        if field[0][i]:
            field = [[0 for i in range(W)] for j in range(H + 1)]
            anim_count, anim_speed, anim_limit = 0, 10, 2000
            score, lines = 0, 0
            pygame.time.wait(1000)
    clock.tick()

