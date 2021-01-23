import pygame as pg
import numpy as np

RESOLUTION = 1920, 1080
std_red, std_blue = 0, 0

class Matrix:
    def __init__(self, app, font_size = 12):
        self.app = app
        self.FONT_SIZE = font_size
        self.SIZE = self.ROWS, self.COLS = app.HEIGHT // font_size, app.WIDTH // font_size
        self.katakana = np.array([chr(int('0x30a0', 16) + i) for i in range(96)] + [' ' for i in range(10)])
        self.font = pg.font.SysFont('ms mincho', font_size, bold = True)

        self.matrix = np.random.choice(self.katakana, self.SIZE)
        self.char_intervals = np.random.randint(25, 50, size = self.SIZE)
        self.cols_speed = np.random.randint(0, 200, size = self.SIZE)
        self.prerendered_chars = self.get_prerendered_chars()

        self.image = self.get_image('image3.jpg')

    def get_image(self, path_to_file):
        image = pg.image.load(path_to_file)
        image = pg.transform.scale(image, self.app.RES)
        pixel_array = pg.pixelarray.PixelArray(image)
        return pixel_array

    def get_prerendered_chars(self):
        char_colors = [(std_red, green, std_blue) for green in range(256)]
        prerendered_chars = {}
        for char in self.katakana:
            prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
            prerendered_chars.update(prerendered_char)
        return prerendered_chars

    def change_chars(self, frames):
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(self.katakana, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars

    def shift_columns(self, frames):
        num_cols = np.argwhere(frames % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = np.unique(num_cols)
        self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift = 1, axis = 0)

    def draw(self):
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * self.FONT_SIZE, y * self.FONT_SIZE
                    _, red, green, blue = pg.Color(self.image[pos])
                    if red and green and blue:
                        color = np.round(np.mean([red, green, blue]))
                        color = 220 if color > 220 else color
                        color = 50 if color < 50 else color
                        char = self.prerendered_chars[(char, (std_red, color, std_blue))]
                        char.set_alpha(color + 60)
                        self.app.surface.blit(char, pos)

    def run(self):
        frames = pg.time.get_ticks()
        self.change_chars(frames)
        self.shift_columns(frames)
        self.draw()

class MatrixVision:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = RESOLUTION
        pg.init()
        self.screen = pg.display.set_mode(self.RES)
        self.surface = pg.Surface(self.RES)
        self.clock = pg.time.Clock()
        self.matrix = Matrix(self)

    def draw(self):
        self.surface.fill(pg.Color('black'))
        self.matrix.run()
        self.screen.blit(self.surface, (0, 0))

    def run(self):
        while True:
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            pg.display.set_caption(str(self.clock.get_fps()))
            self.clock.tick()

if __name__ == '__main__':
    app = MatrixVision()
    app.run()
