import arcade
import football
import numpy

INPUT_LAYER_SZ = 16
OUTPUT_LAYER_SZ = 2

numpy.random.seed(1)


def get_random_matrix(sz_i, sz_j):
    a = []
    for i in range(0, sz_i):
        b = []
        for j in range(0, sz_j):
            b.append(numpy.random.random() * 2 - 1)
        a.append(b)
    return numpy.array(a)


def random_w1():
    return get_random_matrix(INPUT_LAYER_SZ, INPUT_LAYER_SZ)


def random_w2():
    return get_random_matrix(INPUT_LAYER_SZ, OUTPUT_LAYER_SZ)


class Gene:
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

    def __cmp__(self, other):
        if self.player.count < other.player.count:
            return -1
        elif self.player.count == other.player.count:
            return 0
        else:
            return 1

    def get_input_layer(self):
        layer = []
        layer.append(self.field.get_dist(self.player, self.opponent))
        layer.append(self.field.get_ball_distance(self.player))
        layer.append(self.field.get_ball_distance(self.opponent))
        layer.append(self.field.get_player_goal_distance(self.player))
        layer.append(self.field.get_player_opponent_goal_distance(self.player, self.opponent))
        layer.append(self.field.get_player_opponent_goal_distance(self.opponent, self.player))
        layer.append(self.field.get_ball_to_goal_distance(self.player))
        layer.append(self.field.get_ball_to_goal_distance(self.opponent))
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
        input_layer = self.get_input_layer()
        hidden_layer = numpy.dot(input_layer, self.w1)
        output_layer = numpy.dot(hidden_layer, self.w2)
        return output_layer


def mutate(w, sz_i, sz_j):
    for i in range(0, sz_i):
        for j in range(0, sz_j):
            if numpy.random.random() > 0.8:
                w[i][j] *= numpy.random.random()

    return w


def cross_matrix(m1, m2, sz_i, sz_j):
    m = numpy.array(sz_i, sz_j)

    for i in range(0, sz_i):
        for j in range(0, sz_j):
            if numpy.random.random() < 0.5:
                m[i][j] = m1[i][j]
            else:
                m[i][j] = m2[i][j]

    return mutate(m, sz_i, sz_j)


def get_new_gene(gene1: Gene, gene2: Gene):
    w1 = cross_matrix(gene1.w1, gene2.w1, INPUT_LAYER_SZ, INPUT_LAYER_SZ)
    w2 = cross_matrix(gene1.w2, gene2.w2, INPUT_LAYER_SZ, OUTPUT_LAYER_SZ)
    return Gene(w1=w1, w2=w2)


class GeneticGame:
    def __init__(self, field: football.Field, gene1: Gene, gene2: Gene):
        self.field = field
        self.gene1 = gene1
        self.gene2 = gene2

    def press_key_up(self, player):
        if not(self.field.check_other_players_collision(player)) and not(self.field.check_border_collision(player)):
            player.speed_y = 300 * player.scale

    def press_key_down(self, player):
        if not (self.field.check_other_players_collision(player)) and not (self.field.check_border_collision(player)):
            player.speed_y = -300 * player.scale

    def press_key_right(self, player):
        if not (self.field.check_other_players_collision(player)) and not (self.field.check_border_collision(player)):
            player.speed_x = 300 * player.scale

    def press_key_left(self, player):
        if not (self.field.check_other_players_collision(player)) and not (self.field.check_border_collision(player)):
            player.speed_x = -300 * player.scale

    def make_choice(self, gene: Gene):
        choice = gene.update()

        if abs(choice[0]) > abs(choice[1]):
            if choice[0] > 0:
                self.press_key_up(gene.player)
            else:
                self.press_key_down(gene.player)
        else:
            if choice[1] > 0:
                self.press_key_right(gene.player)
            else:
                self.press_key_left(gene.player)

    def update(self):
        self.make_choice(self.gene1)
        self.make_choice(self.gene2)


def choose_best(games):
    genes = []

    for game in games:
        genes.append(game.gene1)
        genes.append(game.gene2)

    genes.sort()

    best = []

    for i in range(20, 40):
        best.append(genes[i])

    return best


def get_new_game_session(fields, games):
    games.clear()
    best = choose_best(games)

    for i in range(0, 20):
        best.append(get_new_gene(best[i], best[(i + 1) % 20]))

    print("Best gene from this session: \ncnt=", best[19].player.count, "\nw1=", best[19].w1, "\nw2=", best[19].w2,
          "\n\n")

    for i in range(1, 40):
        best[i].set_player(fields[i // 2].players[0])
        best[i].set_opponent(fields[i // 2].players[1])
        best[i].set_field(fields[i // 2])

        best[i - 1].set_player(fields[i // 2].players[1])
        best[i - 1].set_opponent(fields[i // 2].players[0])
        best[i - 1].set_field(fields[i // 2])

        games.append(GeneticGame(fields[i // 2], best[i], best[i - 1]))
