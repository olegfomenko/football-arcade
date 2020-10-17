import arcade


class Field:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height

        self.x = x
        self.y = y

        self.borderList = arcade.SpriteList()
        self.field = arcade.Sprite("sprite/field_texture.png")

    def __init_borders(self):
        top_border = arcade.Sprite("sprite/top_border.png")
        top_border.width = self.width
        top_border.height = self.height / 2.5
        top_border.set_position(self.x, self.y + self.height / 2 - top_border.height / 2)

        bottom_border = arcade.Sprite("sprite/bottom_border.png")
        bottom_border.width = self.width
        bottom_border.height = self.height / 2.5
        bottom_border.set_position(self.x, self.y - self.height / 2 + bottom_border.height / 2)

        self.borderList.append(top_border)
        self.borderList.append(bottom_border)

    def setup(self):
        self.__init_borders()

        self.field.width = self.width
        self.field.height = self.height
        self.field.set_position(self.x, self.y)

    def draw(self):
        self.field.draw()
        self.borderList.draw()
