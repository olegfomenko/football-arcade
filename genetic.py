import arcade
import football
import numpy
import random

INPUT_LAYER_SZ = 26
OUTPUT_LAYER_SZ = 2

GENERATION_CNT = 20


def get_random_matrix(sz_i, sz_j, rg):
    """
    Generation random matrix with -rg/2 ... rg/2 values
    :param sz_i: matrix size
    :param sz_j: matrix size
    :param rg: range
    :return:
    """
    a = []
    for i in range(0, sz_i):
        b = []
        for j in range(0, sz_j):
            b.append(numpy.random.random() * rg - rg / 2)
        a.append(b)
    return numpy.array(a)


def random_w1():
    return get_random_matrix(INPUT_LAYER_SZ, INPUT_LAYER_SZ, 2.0)


def random_w2():
    return get_random_matrix(INPUT_LAYER_SZ, OUTPUT_LAYER_SZ, 2.0)


class Gene:
    """
    Gene representation class.
    Contains information about player, his opponent, played field and also neurons weights
    """
    def __init__(self, field: football.Field, player: football.Player, opponent: football.Player, w1, w2):
        self.w2 = w2
        self.w1 = w1
        self.opponent = opponent
        self.player = player
        self.field = field

    def set_opponent(self, opponent):
        self.opponent = opponent

    def set_player(self, player):
        self.player = player

    def set_field(self, field):
        self.field = field

    def get_input_layer(self):
        """
        Creating input neurons layer
        :return: numpy matrix representation of layer
        """
        layer = []
        layer.append(self.player.x - self.opponent.x)
        layer.append(self.player.y - self.opponent.y)
        layer.append(self.player.x - self.field.ball.x)
        layer.append(self.player.y - self.field.ball.y)
        layer.append(self.opponent.x - self.field.ball.x)
        layer.append(self.opponent.y - self.field.ball.y)
        layer.append(self.player.x - self.player.goal_x)
        layer.append(self.player.y - self.player.goal_y)
        layer.append(self.player.x - self.opponent.goal_x)
        layer.append(self.player.y - self.opponent.goal_y)
        layer.append(self.opponent.x - self.player.goal_x)
        layer.append(self.opponent.y - self.player.goal_y)
        layer.append(self.opponent.x - self.opponent.goal_x)
        layer.append(self.opponent.y - self.opponent.goal_y)
        layer.append(self.player.goal_x - self.field.ball.x)
        layer.append(self.player.goal_y - self.field.ball.y)
        layer.append(self.opponent.goal_x - self.field.ball.x)
        layer.append(self.opponent.goal_y - self.field.ball.y)
        layer.append(self.field.get_top(self.player))
        layer.append(self.field.get_bottom(self.player))
        layer.append(self.field.get_right(self.player))
        layer.append(self.field.get_left(self.player))
        layer.append(self.player.speed_x)
        layer.append(self.player.speed_y)
        layer.append(self.field.ball.speed_x)
        layer.append(self.field.ball.speed_y)
        return numpy.array(layer)

    def update(self):
        """
        Getting output layer based on input information and current weights
        :return: numpy matrix representation of output layer
        """
        input_layer = self.get_input_layer()
        hidden_layer = numpy.dot(input_layer, self.w1)
        output_layer = numpy.dot(hidden_layer, self.w2)
        return output_layer


def mutate(w, sz_i, sz_j, c=0.5, rg=2.0):
    """
    Weight matrix mutation function.
    :param w: numpy matrix representation of weights
    :param sz_i:
    :param sz_j:
    :param c: mutation probability
    :param rg: mutation add range (-rg/2 ... rg/2)
    :return:
    """
    for i in range(0, sz_i):
        for j in range(0, sz_j):
            if numpy.random.random() < c:
                w[i][j] += numpy.random.random() * rg - rg/2

    return w


def cross_matrix(m1, m2, sz_i, sz_j):
    """
    Crossing wioght's matrix functions.
    Choosing (i, j) weight from first or sec matrix with 0.5 probability
    :param m1:
    :param m2:
    :param sz_i:
    :param sz_j:
    :return:
    """
    m = numpy.zeros(shape=(sz_i, sz_j))

    for i in range(0, sz_i):
        for j in range(0, sz_j):
            if numpy.random.random() < 0.5:
                m[i][j] = m1[i][j]
            else:
                m[i][j] = m2[i][j]

    return mutate(m, sz_i, sz_j)


def get_new_gene(gene1: Gene, gene2: Gene):
    """
    Generating new gene (son) based on two best
    :param gene1:
    :param gene2:
    :return:
    """
    w1 = cross_matrix(gene1.w1, gene2.w1, INPUT_LAYER_SZ, INPUT_LAYER_SZ)
    w2 = cross_matrix(gene1.w2, gene2.w2, INPUT_LAYER_SZ, OUTPUT_LAYER_SZ)
    return Gene(None, None, None, w1=w1, w2=w2)


class GeneticGame:
    def __init__(self, field: football.Field, gene1: Gene, gene2: Gene):
        self.field = field
        self.gene1 = gene1
        self.gene2 = gene2

    def check_top(self, player):
        for pl in self.field.players:
            if player != pl and arcade.check_for_collision(player.sprite, pl.sprite) and pl.y > player.y:
                return False

        return not (arcade.check_for_collision(player.sprite, self.field.ball.sprite)) or player.y > self.field.ball.y

    def check_down(self, player):
        for pl in self.field.players:
            if player != pl and arcade.check_for_collision(player.sprite, pl.sprite) and pl.y < player.y:
                return False

        return not (arcade.check_for_collision(player.sprite, self.field.ball.sprite)) or player.y < self.field.ball.y

    def check_right(self, player):
        for pl in self.field.players:
            if player != pl and arcade.check_for_collision(player.sprite, pl.sprite) and pl.x > player.x:
                return False

        return not (arcade.check_for_collision(player.sprite, self.field.ball.sprite)) or player.x > self.field.ball.x

    def check_left(self, player):
        for pl in self.field.players:
            if player != pl and arcade.check_for_collision(player.sprite, pl.sprite) and pl.x < player.x:
                return False

        return not (arcade.check_for_collision(player.sprite, self.field.ball.sprite)) or player.x < self.field.ball.x

    def press_key_up(self, player):
        if self.check_top(player) and not(self.field.check_border_collision(player)):
            player.speed_y = 300 * player.scale

    def press_key_down(self, player):
        if self.check_down(player) and not (self.field.check_border_collision(player)):
            player.speed_y = -300 * player.scale

    def press_key_right(self, player):
        if self.check_right(player) and not (self.field.check_border_collision(player)):
            player.speed_x = 300 * player.scale

    def press_key_left(self, player):
        if self.check_left(player) and not (self.field.check_border_collision(player)):
            player.speed_x = -300 * player.scale

    def make_choice(self, gene: Gene):
        choice = gene.update()

        if gene.player.goal_x < gene.field.x:
            if abs(choice[0]) > abs(choice[1]):
                self.press_key_up(gene.player) if choice[0] > 0 else self.press_key_down(gene.player)
            else:
                self.press_key_right(gene.player) if choice[1] > 0 else self.press_key_left(gene.player)
        else:
            if abs(choice[0]) > abs(choice[1]):
                self.press_key_down(gene.player) if choice[0] > 0 else self.press_key_up(gene.player)
            else:
                self.press_key_left(gene.player) if choice[1] > 0 else self.press_key_right(gene.player)

    def update(self):
        self.make_choice(self.gene1)
        self.make_choice(self.gene2)


def choose_best(games):
    """
    Choosing a half best genes
    :param games: list of Genetic Games
    :return:
    """
    genes = []

    for game in games:
        genes.append(game.gene1)
        genes.append(game.gene2)

    genes = sorted(genes, key=lambda gene: gene.player.count)

    best = []

    for i in range(GENERATION_CNT, GENERATION_CNT * 2):
        best.append(genes[i])

    return best


def get_new_game_session(fields, games) -> []:
    """
    Crating new list of GeneticGames - representation of new game session based, based on ended session
    :param fields: list of game fields
    :param games: list of genetic games ojbecs
    :return: list of GeneticGames
    """
    best = choose_best(games)

    games.clear()

    for i in range(0, GENERATION_CNT):
        best.append(get_new_gene(best[i], best[(i + 1) % GENERATION_CNT]))

    print("Best gene from this session: \ncnt=", best[GENERATION_CNT - 1].player.count, "\nw1=", best[GENERATION_CNT-1].w1, "\nw2=", best[GENERATION_CNT-1].w2, "\n\n")

    random.shuffle(best, numpy.random.random)

    for i in range(1, GENERATION_CNT * 2, 2):
        best[i].set_player(fields[i // 2].players[0])
        best[i].set_opponent(fields[i // 2].players[1])
        best[i].set_field(fields[i // 2])

        best[i - 1].set_player(fields[i // 2].players[1])
        best[i - 1].set_opponent(fields[i // 2].players[0])
        best[i - 1].set_field(fields[i // 2])

        games.append(GeneticGame(fields[i // 2], best[i], best[i - 1]))

    return games
