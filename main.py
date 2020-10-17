import arcade
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class Field:

    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height

        self.x = x
        self.y = y

        self.border_w = width
        self.border_h = 10

        self.turned_border_w = 10
        self.turned_border_h = height

        self.borderList = arcade.SpriteList()
        self.field = arcade.Sprite("sprite/field.png")

    def __add_border_w(self, x, y):
        border = arcade.Sprite("sprite/border_w.png",
                               center_x=x, center_y=y,
                               image_width=self.border_w,
                               image_height=self.border_h)
        self.borderList.append(border)

    def __add_border_h(self, x, y):
        border = arcade.Sprite("sprite/border_h.png",
                               center_x=x, center_y=y,
                               image_width=self.turned_border_w,
                               image_height=self.turned_border_h)
        self.borderList.append(border)

    def __init_borders(self):
        self.__add_border_w(self.x, self.y - self.height / 2 + self.border_h / 2)
        self.__add_border_w(self.x, self.y + self.height / 2 - self.border_h / 2)

        self.__add_border_h(self.x - self.width / 2 + self.turned_border_w / 2, self.y)
        self.__add_border_h(self.x + self.width / 2 - self.turned_border_w / 2, self.y)

    def setup(self):
        self.__init_borders()

        self.field.width = self.width
        self.field.height = self.height
        self.field.set_position(self.x, self.y)

    def draw(self):
        self.field.draw()
        self.borderList.draw()

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.ball = arcade.Sprite("sprite/ball.png")
        self.field = Field(300, 300, 500, 300)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.ball.center_x = 100
        self.ball.center_y = 100

        self.ball.width = 20
        self.ball.height = 20

        self.field.setup()

    def on_draw(self):
        arcade.start_render()
        self.ball.draw()
        self.field.draw()

    def update(self, delta_time):
        self.ball.center_x += delta_time * 100
        self.ball.center_y = self.ball.center_x ** 1.02


game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
game.setup()
game.on_draw()
arcade.run()
