import arcade
import football

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.field = football.Field(300, 300, 0.5)

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        self.field.setup()

    def on_draw(self):
        arcade.start_render()
        self.field.draw()

    def update(self, delta_time):
        self.field.update(delta_time)

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.field.player.speed_y = 0

        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.field.player.speed_x = 0

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP:
            self.field.player.speed_y = 150

        if key == arcade.key.DOWN:
            self.field.player.speed_y = -150

        if key == arcade.key.RIGHT:
            self.field.player.speed_x = 150

        if key == arcade.key.LEFT:
            self.field.player.speed_x = -150


game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
game.setup()
game.on_draw()
arcade.run()
