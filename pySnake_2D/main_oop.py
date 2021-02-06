import pygame
from random import randrange


class Snake:
    def __init__(self, field, head=(0, 0), length=1, speed=5, eat_sound='pySnake_2D/eat.mp3'):  # eat_sound (Cap!)
        self.scene = field.scene
        self.SIZE = field.SIZE  # Size of 1 square
        self.head = head
        self.length = length
        self.speed = speed
        self.path = {'W': (0, -1),  # dict for walking
                     'S': (0, 1),
                     'A': (-1, 0),
                     'D': (1, 0),
                     0: (0, 0)}
        self.body = [head]
        try:
            self.eat_sound = pygame.mixer.Sound(eat_sound)
        except Exception:
            pass

    # snake walking method, step-by-step
    def step(self, direction):
        x = self.head[0] + self.path[direction][0]
        y = self.head[1] + self.path[direction][1]
        self.head = (x, y)
        self.body.append(self.head)
        self.body = self.body[-self.length:]

    # draw snake method
    def draw(self):
        pygame.draw.rect(self.scene, pygame.Color('green'),
                         (self.body[-1][0] * self.SIZE,
                          self.body[-1][1] * self.SIZE,
                          self.SIZE, self.SIZE))
        if len(self.body) > 1:
            [(pygame.draw.rect(self.scene, pygame.Color('darkgreen'),
                               (i * self.SIZE + 1, j * self.SIZE + 1,
                                self.SIZE - 2, self.SIZE - 2))) for i, j in self.body[:-1]]

    # eat and grows apple method
    def eat(self):
        self.length += 1
        try:
            self.eat_sound.play()
        except Exception:
            pass


# Class Field - it's a main game field
class Field:
    def __init__(self, score=0,
                 size=25,  # size of 1 square
                 W=30, H=20):  # number of squares Width + Height

        self.SIZE = size
        self.W, self.H = W, H
        self.RES = [W * size, H * size]
        self.font_score = pygame.font.SysFont('Arial', 26, bold=True)
        self.scene = pygame.display.set_mode(self.RES)
        self.score = score

    # draw method
    def draw(self):
        # print backprint
        self.scene.fill((30, 30, 30))  # or fill the field with black
        [(pygame.draw.rect(self.scene, (20, 20, 20),
                           (i * self.SIZE, j * self.SIZE,
                            self.SIZE, self.SIZE), 1)) for i in range(self.W) for j in range(self.H)]
        # print score
        render_score = self.font_score.render(f'SCORE: {self.score}', True,
                                              pygame.Color('darkorange'))
        self.scene.blit(render_score, (5, 5))


class Apple:
    def __init__(self, field):  # link with game field object
        self.scene = field.scene
        self.SIZE = field.SIZE
        self.RES_X = field.W
        self.RES_Y = field.H
        self.x = randrange(0, self.RES_X)
        self.y = randrange(0, self.RES_Y)
        self.spawn()

    # draw method
    def draw(self):
        pygame.draw.rect(self.scene, pygame.Color('red'),
                         (self.x * self.SIZE, self.y * self.SIZE,
                          self.SIZE, self.SIZE))

    # spawn new apple
    def spawn(self):
        self.x = randrange(0, self.RES_X)
        self.y = randrange(0, self.RES_Y)


class Game:
    def __init__(self, gameW=46, gameH=27, gameSIZE=25):
        self.W, self.H, self.SIZE = gameW, gameH, gameSIZE
        self.field = Field(size=self.SIZE, W=self.W, H=self.H)
        rand_head = (randrange(0, self.field.W),
                     randrange(0, self.field.H))
        self.snake = Snake(self.field, head=rand_head)
        self.apple = Apple(self.field)
        self.dirs = {'W': True, 'S': True, 'D': True, 'A': True, }
        self.dir = 0
        self.font_score = pygame.font.SysFont('Arial', 26, bold=True)
        self.font_gameover = pygame.font.SysFont('Arial', 48, bold=True)
        self.clock = pygame.time.Clock()
        self.pause = False

    def play(self):
        self.field.draw()
        self.snake.draw()
        while (self.apple.x, self.apple.y) in self.snake.body:
            self.apple.spawn()
        self.apple.draw()

        # snake movement
        self.snake.step(self.dir)

        # snake eating
        if self.snake.head == (self.apple.x, self.apple.y):
            self.snake.eat()
            while (self.apple.x, self.apple.y) in self.snake.body:
                self.apple.spawn()
            self.field.score += 1
            self.snake.speed += 1

        # Game over execution
        A = len(self.snake.body) != len(set(self.snake.body))
        B1 = self.snake.head[0] > self.field.W - 1
        B2 = self.snake.head[0] < 0
        B = B1 or B2
        C1 = self.snake.head[1] > self.field.H - 1
        C2 = self.snake.head[1] < 0
        C = C1 or C2

        if A or B or C:
            game_over = True
            try:
                pygame.mixer.Sound('pySnake_2D/gameover.mp3').play()
            except Exception:
                pass

            while game_over:
                render_end = self.font_gameover.render(
                    'GAME OVER', True, pygame.Color('orange'))
                self.field.scene.blit(render_end,
                                      (self.field.RES[0] // 2 - 130,
                                       self.field.RES[1] // 2 - 100))
                render_reset = self.font_score.render(
                    'Press "Enter" to try again!', True, pygame.Color('orange'))
                self.field.scene.blit(render_reset,
                                      (self.field.RES[0] // 2 - 140,
                                       self.field.RES[1] // 2 - 50))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            game_over = False
                            self.field = Field(size=self.SIZE, W=self.W, H=self.H)
                            rand_head = (randrange(0, self.field.W),
                                         randrange(0, self.field.H))
                            self.snake = Snake(self.field, head=rand_head)
                            self.apple = Apple(self.field)
                            self.dirs = {'W': True, 'S': True, 'D': True, 'A': True, }
                            self.dir = 0
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()

        pygame.display.flip()

    def core(self):
        if not self.pause:
            self.play()
            self.clock.tick(self.snake.speed)
            self.control()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
        # controll

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP] and self.dirs['W']:
                    self.dir = 'W'
                    self.dirs = {'W': True, 'S': False, 'D': True, 'A': True, }
                if event.key in [pygame.K_s, pygame.K_DOWN] and self.dirs['S']:
                    self.dir = 'S'
                    self.dirs = {'W': False, 'S': True, 'D': True, 'A': True, }
                if event.key in [pygame.K_a, pygame.K_LEFT] and self.dirs['A']:
                    self.dir = 'A'
                    self.dirs = {'W': True, 'S': True, 'D': False, 'A': True, }
                if event.key in [pygame.K_d, pygame.K_RIGHT] and self.dirs['D']:
                    self.dir = 'D'
                    self.dirs = {'W': True, 'S': True, 'D': True, 'A': False, }
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                    if self.pause:
                        render_pause = self.font_gameover.render('P A U S E', True,
                                                                 pygame.Color('orange'))
                        self.field.scene.blit(render_pause,
                                              (self.field.RES[0] // 2 - 100,
                                               self.field.RES[1] // 2 - 100))
                        pygame.display.flip()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    game = Game(gameW=16 * 5, gameH=9 * 5, gameSIZE=20)
    while True:
        game.core()
