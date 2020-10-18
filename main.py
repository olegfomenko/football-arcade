import arcade
import football
import genetic
import functools

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.fields = []

        self.fields.append(football.Field(150, 50, 0.2))
        self.fields.append(football.Field(150, 200, 0.2))
        self.fields.append(football.Field(150, 350, 0.2))
        self.fields.append(football.Field(150, 500, 0.2))
        self.fields.append(football.Field(150, 650, 0.2))

        self.fields.append(football.Field(450, 50, 0.2))
        self.fields.append(football.Field(450, 200, 0.2))
        self.fields.append(football.Field(450, 350, 0.2))
        self.fields.append(football.Field(450, 500, 0.2))
        self.fields.append(football.Field(450, 650, 0.2))

        self.fields.append(football.Field(750, 50, 0.2))
        self.fields.append(football.Field(750, 200, 0.2))
        self.fields.append(football.Field(750, 350, 0.2))
        self.fields.append(football.Field(750, 500, 0.2))
        self.fields.append(football.Field(750, 650, 0.2))

        self.fields.append(football.Field(1050, 50, 0.2))
        self.fields.append(football.Field(1050, 200, 0.2))
        self.fields.append(football.Field(1050, 350, 0.2))
        self.fields.append(football.Field(1050, 500, 0.2))
        self.fields.append(football.Field(1050, 650, 0.2))

        self.games = []

        self.timer = 0.0
        self.session_cnt = 1

        for field in self.fields:
            gene1 = genetic.Gene(field, field.players[0], field.players[1], genetic.random_w1(), genetic.random_w2())
            gene2 = genetic.Gene(field, field.players[1], field.players[0], genetic.random_w1(), genetic.random_w2())
            self.games.append(genetic.GeneticGame(field, gene1, gene2))

        arcade.set_background_color(arcade.color.WHITE)

    def new_game_session(self):
        self.timer = 0.0
        self.session_cnt += 1

        print("Preparing new session number ", self.session_cnt, "\n")

        for field in self.fields:
            field.new_game()

        self.games = genetic.get_new_game_session(self.fields, self.games)

    def setup(self):
        for field in self.fields:
            field.setup()

    def on_draw(self):
        arcade.start_render()

        for field in self.fields:
            field.draw()

    def update(self, delta_time):

        if self.timer > 180.0:
            self.new_game_session()

        for field in self.fields:
            field.update(delta_time)

        for game in self.games:
            game.update()

        self.timer += delta_time


game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
game.setup()
game.on_draw()
arcade.run()
