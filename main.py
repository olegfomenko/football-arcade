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

    def press_key_up(self, player):
        player.speed_y = 150

    def press_key_down(self, player):
        player.speed_y = -150

    def press_key_right(self, player):
        player.speed_x = 150

    def press_key_left(self, player):
        player.speed_x = -150

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP:
            self.press_key_up(self.field.player)

        if key == arcade.key.DOWN:
            self.press_key_down(self.field.player)

        if key == arcade.key.RIGHT:
            self.press_key_right(self.field.player)

        if key == arcade.key.LEFT:
            self.press_key_left(self.field.player)

game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
game.setup()
game.on_draw()
arcade.run()
