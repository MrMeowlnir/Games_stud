import pygame
from random import randrange
import sys

RES = 800
SIZE = 50

x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
dirs = {'W': True, 'S': True, 'D': True, 'A': True,}
length = 1
score = 0
snake = [(x,y)]
pause = False
dx, dy = 0, 0
fps = 5

pygame.init()
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 26, bold = True)
font_end = pygame.font.SysFont('Arial', 48, bold = True)
img = pygame.image.load('E:\projects\Games_stud-1\pySnake_2D\landscape.jpeg').convert()

gameover_sound = pygame.mixer.Sound('pySnake_2D/gameover.mp3')

pygame.mixer.music.load('pySnake_2D/music.wav')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops = -1)
while True:
    if not pause:
        sc.blit(img, (0, 0))
        # drawing snake and apple
        [(pygame.draw.rect(sc, pygame.Color('green'), (i, j, SIZE - 2, SIZE - 2))) for i, j in snake]
        pygame.draw.rect(sc, pygame.Color('red'), (*apple, SIZE, SIZE))
        #render score
        render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
        sc.blit(render_score, (5, 5))

        #snake movement
        x += dx * SIZE
        y += dy * SIZE
        if x < 0:
            x = RES - SIZE
        if x > RES - SIZE:
            x = 0
        if y < 0:
            y = RES - SIZE
        if y > RES - SIZE:
            y = 0

        snake.append((x, y))
        snake = snake[-length:]

        #eating
        if snake[-1] == apple:
            eat_sound.play()
            apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
            while apple in snake:
                apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
            length += 1
            score += 1
            fps += 1


        if len(snake) != len(set(snake)):
            game_over = True
            gameover_sound.play()
            while game_over:
                render_end = font_end.render('G A M E  O V E R', 1, pygame.Color('Orange'))
                sc.blit(render_end, (RES // 2 - 170, RES // 2 - 100))
                render_reset = font_score.render('Press "Enter" for try again!', 1, pygame.Color('Orange'))
                sc.blit(render_reset, (RES // 2 - 150, RES // 2 - 50))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            game_over = False
                            x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
                            apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
                            dirs = {'W': True, 'S': True, 'D': True, 'A': True,}
                            length = 1
                            score = 0
                            snake = [(x,y)]
                            pause = False
                            dx, dy = 0, 0
                            fps = 5
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
        #display
        pygame.display.flip()
        clock.tick(fps)

        # controll
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and dirs['W']:
                    dx, dy = 0, -1
                    dirs = {'W': True, 'S': False, 'D': True, 'A': True,}
                if event.key == pygame.K_s and dirs['S']:
                    dx, dy = 0, 1
                    dirs = {'W': False, 'S': True, 'D': True, 'A': True,}
                if event.key == pygame.K_a and dirs['A']:
                    dx, dy = -1, 0
                    dirs = {'W': True, 'S': True, 'D': False, 'A': True,}
                if event.key == pygame.K_d and dirs['D']:
                    dx, dy = 1, 0
                    dirs = {'W': True, 'S': True, 'D': True, 'A': False,}
                if event.key == pygame.K_SPACE:
                    render_pause = font_end.render('P A U S E', 1, pygame.Color('Orange'))
                    sc.blit(render_pause, (RES // 2 - 100, RES // 2 - 100))
                    pygame.display.flip()
                    pause = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
