import arcade


class GameObject:
    ACCELERATION = 50
    EPS = 0e-9

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

        self.sprite.set_position(self.x, self.y)


class Ball(GameObject):
    def __init__(self, sprite, x, y, scale):
        super().__init__(sprite, x, y, scale)

        self.speed_x = 0
        self.speed_y = 0

    def change_speed(self, speed_x, speed_y):
        self.speed_x = speed_x * 1.5
        self.speed_y = speed_y * 1.5


class Player(GameObject):
    def __init__(self, sprite, x, y, scale):
        super().__init__(sprite, x, y, scale)

        self.speed_x = 0
        self.speed_y = 0

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0


class Field:
    def __init__(self, x, y, scale):
        self.scale = scale

        self.field = arcade.Sprite("sprite/field_texture.png")

        self.width = self.field.width * scale
        self.height = self.field.height * scale

        self.field.scale = scale

        self.x = x
        self.y = y

        self.x_border_list = arcade.SpriteList()
        self.y_border_list = arcade.SpriteList()
        self.players = []

        self.ball = Ball(arcade.Sprite("sprite/ball.png"), x, y, scale)
        self.player = Player(arcade.Sprite("sprite/red_player.png"), x - 100, y, scale)

        self.players.append(self.player)

    def __init_borders(self):
        border = arcade.Sprite("sprite/top.png")
        border.scale = self.scale
        border.set_position(self.x, self.y + self.height / 2 - border.height / 2)
        self.y_border_list.append(border)

        border = arcade.Sprite("sprite/top.png")
        border.scale = self.scale
        border.set_position(self.x, self.y - self.height / 2 + border.height / 2)
        self.y_border_list.append(border)

        border = arcade.Sprite("sprite/part.png")
        border.scale = self.scale
        border.set_position(self.x - self.width / 2 + border.width / 2,
                            self.y - self.height / 2 + border.height / 2)
        self.x_border_list.append(border)

        border = arcade.Sprite("sprite/part.png")
        border.scale = self.scale
        border.set_position(self.x - self.width / 2 + border.width / 2,
                            self.y + self.height / 2 - border.height / 2)
        self.x_border_list.append(border)

        border = arcade.Sprite("sprite/part.png")
        border.scale = self.scale
        border.set_position(self.x + self.width / 2 - border.width / 2,
                            self.y - self.height / 2 + border.height / 2)
        self.x_border_list.append(border)

        border = arcade.Sprite("sprite/part.png")
        border.scale = self.scale
        border.set_position(self.x + self.width / 2 - border.width / 2,
                            self.y + self.height / 2 - border.height / 2)
        self.x_border_list.append(border)

    def setup(self):
        self.__init_borders()
        self.field.set_position(self.x, self.y)

    def draw(self):
        self.x_border_list.draw()
        self.y_border_list.draw()

        self.field.draw()
        self.ball.draw()
        self.player.draw()

    def check(self, pl) -> bool:
        for i in range(0, len(self.players)):
            if pl != self.players[i] and arcade.check_for_collision(self.players[i].sprite, pl.sprite):
                self.players[i].stop()
                pl.stop()
                return True

        if pl.sprite.collides_with_list(self.y_border_list):
            pl.speed_y = -pl.speed_y
            return True

        if pl.sprite.collides_with_list(self.x_border_list):
            pl.speed_x = -pl.speed_x
            return True

        return False

    def update(self, delta_time):
        self.ball.update(delta_time)
        self.player.update(delta_time)

        if arcade.check_for_collision(self.player.sprite, self.ball.sprite):
            self.ball.change_speed(self.player.speed_x, self.player.speed_y)
            self.player.speed_x = -self.player.speed_x
            self.player.speed_y = -self.player.speed_y

        if len(self.ball.sprite.collides_with_list(self.y_border_list)) > 0:
            self.ball.speed_y = -self.ball.speed_y
            self.player.update(delta_time)

        if len(self.ball.sprite.collides_with_list(self.x_border_list)) > 0:
            self.ball.speed_x = -self.ball.speed_x
            self.player.update(delta_time)

        for i in range(0, len(self.players)):
            self.check(self.players[i])

        if self.ball.x < self.x - self.width / 2 or self.ball.x > self.x + self.width / 2:
            self.ball.to_default()
            print("Goal!")
