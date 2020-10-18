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

        self.count_blue = 0
        self.count_red = 0

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

    def check_border_collision(self, object: GameObject):
        border_list = object.sprite.collides_with_list(self.y_border_list)

        if len(border_list) > 0:
            border = border_list[0]

            if border.center_y < object.y:
                object.speed_y = abs(object.speed_y)
            else:
                object.speed_y = -abs(object.speed_y)

        border_list = object.sprite.collides_with_list(self.x_border_list)

        if len(border_list) > 0:
            border = border_list[0]

            if border.center_x < object.x:
                object.speed_x = abs(object.speed_x)
            else:
                object.speed_x = -abs(object.speed_x)


    def push_objects(self, object: GameObject, to_push: GameObject, c = 1.0):
        if object.x < to_push.x:
            object.speed_x = -abs(object.speed_x)
            to_push.speed_x = abs(object.speed_x) * c
        else:
            object.speed_x = abs(object.speed_x)
            to_push.speed_x = -abs(object.speed_x) * c

        if object.y < to_push.y:
            object.speed_y = -abs(object.speed_y)
            to_push.speed_y = abs(object.speed_y) * c
        else:
            object.speed_y = abs(object.speed_y)
            to_push.speed_y = -abs(object.speed_y) * c

    def check_ball_collision(self, player: Player):
        if arcade.check_for_collision(player.sprite, self.ball.sprite):
            self.push_objects(player, self.ball, 1.5)

    def check_other_players_collision(self, player):
        for pl in self.players:
            if pl != player and pl.sprite.collides_with_sprite(player.sprite):
                self.push_objects(player, pl)

    def update(self, delta_time):
        self.ball.update(delta_time)
        self.player.update(delta_time)

        self.check_ball_collision(self.player)
        self.check_border_collision(self.ball)
        self.check_border_collision(self.player)
        self.check_other_players_collision(self.player)

        if self.ball.x < self.x - self.width / 2:
            self.ball.to_default()
            self.player.to_default()
            ++self.count_blue
            print("Goal by blue! Red : Blue", self.count_red, ":", self.count_blue)

        if self.ball.x > self.x + self.width / 2:
            self.ball.to_default()
            self.player.to_default()
            ++self.count_red
            print("Goal by red! Red : Blue", self.count_red, ":", self.count_blue)
