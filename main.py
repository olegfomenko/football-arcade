import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.ball = arcade.Sprite("sprite/ball.png")

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.ball.center_x = 100
        self.ball.center_y = 100
        self.ball.width = 20
        self.ball.height = 20

    def on_draw(self):
        arcade.start_render()
        self.ball.draw()

    def update(self, delta_time):
        self.ball.center_x += delta_time * 100
        self.ball.center_y = self.ball.center_x ** 1.02

game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
game.setup()
game.on_draw()
arcade.run()
