import arcade


class GameObject:
    def __init__(self, sprite: arcade.Sprite, default_x, default_y, scale):
        self.sprite = sprite

        self.width = self.sprite.width * scale
        self.height = self.sprite.height * scale

        self.sprite.scale = scale
        self.sprite.color = arcade.color.GOLD
        self.sprite.set_position(default_x, default_y)

        self.default_x = self.x = default_x
        self.default_y = self.y = default_y

    def to_default(self):
        self.x = self.default_x
        self.y = self.default_y
        self.sprite.set_position(self.x, self.y)

    def draw(self):
        self.sprite.draw()

    def update(self, delta_time):
        self.sprite.set_position(self.x, self.y)


class Ball(GameObject):
    ACCELERATION = 50
    EPS = 0e-9

    def __init__(self, sprite, x, y, scale):
        super().__init__(sprite, x, y, scale)

        self.speed_x = 0
        self.speed_y = 0

    def update(self, delta_time):
        if self.speed_x != 0 or self.speed_y != 0:
            self.x += self.speed_x * delta_time
            self.y += self.speed_y * delta_time

            if self.speed_x > 0:
                self.speed_x -= Ball.ACCELERATION * delta_time
            else:
                self.speed_x += Ball.ACCELERATION * delta_time

            if self.speed_y > 0:
                self.speed_y -= Ball.ACCELERATION * delta_time
            else:
                self.speed_y += Ball.ACCELERATION * delta_time

            if abs(self.speed_x) < Ball.EPS:
                self.speed_x = 0

            if abs(self.speed_y) < Ball.EPS:
                self.speed_y = 0

        super().update(delta_time)

    def change_speed(self, speed_x, speed_y):
        self.speed_x = speed_x * 1.5
        self.speed_y = speed_y * 1.5


class Player(GameObject):
    def __init__(self, sprite, x, y, scale):
        super().__init__(sprite, x, y, scale)

        self.speed_x = 0
        self.speed_y = 0

    def update(self, delta_time):
        if self.speed_x != 0 or self.speed_y != 0:
            self.x += self.speed_x * delta_time
            self.y += self.speed_y * delta_time

        super().update(delta_time)


class Field:
    def __init__(self, x, y, scale):
        self.scale = scale

        self.field = arcade.Sprite("sprite/field_texture.png")

        self.width = self.field.width * scale
        self.height = self.field.height * scale

        self.field.scale = scale

        self.x = x
        self.y = y

        self.top_border = arcade.Sprite("sprite/top.png")
        self.bottom_border = arcade.Sprite("sprite/top.png")

        self.left_border = arcade.Sprite("sprite/left.png")
        self.right_border = arcade.Sprite("sprite/left.png")

        self.ball = Ball(arcade.Sprite("sprite/ball.png"), x, y, scale)
        self.player = Player(arcade.Sprite("sprite/red_player.png"), x - 100, y, scale)

    def __init_borders(self):
        self.top_border.scale = self.scale
        self.top_border.set_position(self.x, self.y + self.height / 2 - self.top_border.height / 2)

        self.bottom_border.scale = self.scale
        self.bottom_border.set_position(self.x, self.y - self.height / 2 + self.bottom_border.height / 2)

        self.left_border.scale = self.scale
        self.left_border.set_position(self.x - self.width / 2 + self.left_border.width / 2, self.y)

        self.right_border.scale = self.scale
        self.right_border.set_position(self.x + self.width / 2 - self.left_border.width / 2, self.y)

    def setup(self):
        self.__init_borders()
        self.field.set_position(self.x, self.y)

    def draw(self):
        self.top_border.draw()
        self.bottom_border.draw()
        self.left_border.draw()
        self.right_border.draw()

        self.field.draw()
        self.ball.draw()
        self.player.draw()

    def update(self, delta_time):

        self.ball.update(delta_time)
        self.player.update(delta_time)

        if arcade.check_for_collision(self.player.sprite, self.ball.sprite):
            self.ball.change_speed(self.player.speed_x, self.player.speed_y)

        if arcade.check_for_collision(self.ball.sprite, self.top_border) or \
                arcade.check_for_collision(self.ball.sprite, self.bottom_border):
            self.ball.speed_y = -self.ball.speed_y

        if arcade.check_for_collision(self.ball.sprite, self.right_border) or \
                arcade.check_for_collision(self.ball.sprite, self.left_border):
            self.ball.speed_y = -self.ball.speed_y
