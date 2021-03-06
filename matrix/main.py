import os
import pygame as pg
from random import choice, randrange

class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.value = choice(green_katakana)
        self.interval = randrange(5, 30)
        self.speed = speed

    def draw(self, color):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_katakana if color == 'green' else lightgreen_katakana)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
        surface.blit(self.value, (self.x, self.y))

class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(8, 28)
        self.speed = randrange(1, 4)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self):
        [symbol.draw('green') if i else symbol.draw('lightgreen') for i,symbol in enumerate(self.symbols)]

os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 1920, 1080
FONT_SIZE = 25
alpha_value = 0

pg.init()
screen = pg.display.set_mode(RES)
surface = pg.Surface(RES)
surface.set_alpha(alpha_value)
clock = pg.time.Clock()
fps = 60
pg.mixer.music.load('matrix/music.mp3')
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play()

katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
font = pg.font.SysFont('ms mincho', FONT_SIZE, bold = True)

green_katakana = [font.render(char, True, pg.Color(20, randrange(100, 255), 20)) for char in katakana]
lightgreen_katakana = [font.render(char, True, pg.Color(200, 255, 200)) for char in katakana]

symbol_columns = [SymbolColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]

while True:
    screen.blit(surface, (0, 0))
    surface.fill(pg.Color('black'))

    [symbol_column.draw() for symbol_column in symbol_columns]

    if not pg.time.get_ticks() % 30 and alpha_value < 170:
        alpha_value += 1
        surface.set_alpha(alpha_value)

    [exit() for i in pg.event.get() if i.type == pg.QUIT]
    pg.display.flip()
    clock.tick(fps)
