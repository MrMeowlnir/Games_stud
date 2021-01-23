from ursina import *

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.black
        window.fullscreen_size = 1920, 1080
        window.fullscreen = True
        Light(type = 'ambient', color = (0.5, 0.5, 0.5, 1))
        Light(type = 'directional', color = (0.5, 0.5, 0.5, 1), direction = (1, 1, 1))
        self.MAP_SIZE = 20
        self.new_game()
        camera.position = (self.MAP_SIZE // 2, -20.5, -20)
        camera.rotation_x = -57
    def create_map(self, MAP_SIZE):
        Entity(model = 'quad', scale = MAP_SIZE,
                    position = (MAP_SIZE // 2, MAP_SIZE // 2, 0),
                    color = color.dark_gray)
        Entity(model=Grid(MAP_SIZE, MAP_SIZE), scale = MAP_SIZE,
                    position = (MAP_SIZE // 2, MAP_SIZE // 2, -0.01),
                    color = color.white)


    def new_game(self):
        self.create_map(self.MAP_SIZE)

    def input(self, key):
        super().input(key)

    def update(self):
        pass

if __name__=='__main__':
    game = Game()
    update = game.update
    game.run()
