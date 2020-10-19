import arcade
import football
import numpy

INPUT_LAYER_SZ = 16
OUTPUT_LAYER_SZ = 2

GENERATION_CNT = 20


def get_random_matrix(sz_i, sz_j):
    a = []
    for i in range(0, sz_i):
        b = []
        for j in range(0, sz_j):
            b.append(numpy.random.random() * 2 - 1)
        a.append(b)
    return numpy.array(a)


def random_w1():
    w1 = [[-1.99922182e+01, -1.88353663e+01, 6.11163581e+00, -1.71907867e+01,
           -2.04595495e+01, -1.57655625e+01, 3.06872608e+01, -1.84938279e+01,
           2.55614995e+01, -3.43102529e+01, 1.39795805e+01, -4.02781630e+00,
           -1.45114968e+01, -4.50503844e+01, 1.11003703e+01, 2.18209140e+01],
          [5.10307646e+00, -1.90749841e+01, -6.88266771e+00, -3.43647013e-01,
           1.09734593e+01, -3.16568480e+01, 9.13924455e+00, 1.34422033e+01,
           -4.41396397e+00, 1.29355094e+01, 2.97929495e+01, -7.60053311e+00,
           1.20463096e+01, 2.86741786e+01, 1.91573959e+01, -8.33677884e+00],
          [-7.31172124e+00, -1.76175893e+01, 9.03348095e+00, 8.09444685e+00,
           6.96666010e+00, -1.92559184e+01, 1.77175394e+01, 1.81863417e+01,
           2.11524908e+00, -2.88114956e+00, -2.40048718e+01, 5.55319042e+00,
           3.45339770e+01, 3.89301386e-03, 5.58533297e+00, 1.84657151e+00],
          [1.29984184e+01, 1.25677626e+01, -1.61841244e+01, -3.38243644e+00,
           -2.22575840e+00, 3.13918732e+01, -1.36680603e+00, -4.96470786e+00,
           1.55668479e+01, 4.58656560e+01, 2.22400574e+01, 4.98509984e+00,
           -1.58836041e+01, -1.27149160e+01, -8.02144910e+00, 1.69700028e+01],
          [-5.90374091e+00, -2.75582609e+01, 6.01493859e+00, -5.79455289e+00,
           -2.23997408e+00, -3.90822379e+00, -6.38778870e+00, -7.85905265e+00,
           2.24994712e+01, 1.24250724e+01, -6.68308315e+00, 1.47341128e+01,
           3.70462052e+00, 1.10291408e+01, 5.75935316e+00, -9.94074004e+00],
          [-5.21453667e+00, 1.14634766e+01, -3.70052054e+00, -6.99261720e+00,
           -2.74772915e+00, 1.58636280e+01, -4.81163755e+00, 6.29053110e+00,
           -5.19106619e+00, -1.55409982e+01, 7.62553500e-01, -1.34949108e+00,
           4.32366028e-01, -8.74896035e-01, -1.20000447e+01, 3.84902931e+00],
          [6.47602908e+00, 2.58957063e+01, -1.90448973e+01, 1.71177106e+00,
           6.37876948e+00, 1.86418923e+01, -2.22965651e+01, -3.59679450e+01,
           -2.01302460e+01, 1.81991482e+01, -2.56732210e+01, 1.05395506e+01,
           7.18171559e+00, 6.63900621e+00, -3.44014383e+00, -8.24314163e+00],
          [-4.78519216e-01, -1.96901756e+01, 1.42884970e+01, 7.74300089e+00,
           -8.24417423e-01, -1.84611016e+01, 4.02236915e+00, 1.35056610e+01,
           -2.15506878e+01, -2.19926172e+01, 1.22934931e+01, 5.18419776e+00,
           -2.73261928e+01, 7.74163813e+00, -1.46087345e+01, 1.56397790e+00],
          [-2.21710798e+01, -2.90787394e+00, -3.03627269e+01, 4.11996121e+00,
           -7.54429758e+00, -1.10584120e+01, 1.57818850e+01, -3.00837612e+00,
           -9.86791294e+00, -1.09715051e+01, -1.12652480e+01, 2.14551688e+01,
           -2.62293604e+01, 1.47059744e+01, 1.43779205e+01, 1.00264731e+01],
          [-1.24638022e+01, 4.06409445e+00, 9.90757775e+00, 1.24955945e+01,
           1.90842332e+01, -1.11527580e+00, -3.14190633e+01, 2.12978203e+00,
           -1.41735883e+01, 1.03087312e+01, -2.38848298e+01, 7.96843505e-01,
           1.01835299e+01, -1.33233768e+01, -2.39984537e+01, -2.31969104e+01],
          [8.29896454e+00, -1.76196030e+01, -5.72443623e+00, -1.32479697e+01,
           -3.86167025e+00, -7.32533021e+00, -3.22583249e+01, -3.43540847e+01,
           3.91892236e+00, 9.19963566e+00, -1.15544859e+01, 1.72600972e+01,
           2.13971555e+01, 7.90140047e+00, -1.94946637e+01, -3.39181746e+00],
          [5.03945994e-02, -5.12467883e+00, 1.01660676e+01, 2.14136777e+01,
           -1.47450015e+01, 8.52631325e+00, 8.40779916e+00, 5.75944879e+01,
           -3.61253481e+00, -4.17921653e+01, -7.53164491e+00, -4.55535223e+01,
           -1.81293062e+01, -2.17471363e+01, 4.02041756e+01, 6.17993073e+00],
          [1.62119489e+01, 1.61438673e+01, -2.68848517e+01, -7.19538895e+00,
           1.92986634e+01, 8.96564284e-01, 3.43956484e+00, -1.77982414e+01,
           -3.89734030e+00, 7.17809217e+00, 1.49419849e+01, -1.24414951e+01,
           -1.07818502e+01, -6.11759451e+00, 2.70063249e+00, -3.87171587e+00],
          [-1.39619739e+01, -8.77531718e+00, -4.10276718e+01, 1.95682456e+01,
           -3.64044435e+00, -1.48827899e+01, 1.62219673e+01, 2.04934355e+01,
           3.58809693e+01, 1.84043501e+01, -2.29411881e+00, 5.81465407e+00,
           -2.08274169e+01, 1.95249267e+00, -4.45654170e-01, 3.64073397e-01],
          [-4.12959361e+00, -1.85058512e+00, 1.29838468e+01, -1.55855304e+01,
           -2.64955412e+01, 3.62257817e+00, 1.26592147e+01, -2.05439633e+01,
           2.19967589e+01, -1.31531942e+00, 3.57595569e+01, 6.85296205e+00,
           7.94770716e+00, 1.16846364e+01, -1.00817944e+01, 7.47040293e+00],
          [2.32145023e+01, -1.53260930e+01, 3.08116744e+00, -1.32753631e+01,
           -2.84195036e+01, -1.19077092e+01, 6.68636160e+00, -1.75866379e+00,
           -9.84837947e+00, -5.35074623e+00, -8.29422567e+00, -1.49937053e+01,
           1.00456036e+01, -2.95994838e+00, 7.08847549e+00, -1.55384260e+01]]

    w1 = numpy.array(w1)

    return mutate(w1, INPUT_LAYER_SZ, INPUT_LAYER_SZ, 0.5, 10.0)


def random_w2():
    w2 = [[1.56320904e-02, -5.33047541e-02],
          [-1.27526692e+01, 1.96334644e+01],
          [-2.57675578e+01, -2.49101765e+01],
          [1.40404075e+01, -1.27515214e+01],
          [4.24662556e+00, 1.33945132e+01],
          [8.44223431e+00, 5.10868535e+00],
          [3.26286594e+01, -2.46729514e+01],
          [6.54551327e+00, -3.31256663e+01],
          [8.80714553e+00, -2.39238909e+01],
          [-3.00278652e-01, 1.32539924e+01],
          [-7.64908853e+00, -8.05794019e+00],
          [3.82299410e+00, 3.33227254e+01],
          [-1.28812859e+01, 3.93977494e+00],
          [8.67828821e+00, 2.70567250e+00],
          [6.24280540e-01, -9.91433631e+00],
          [2.10622388e+01, -9.76508366e+00]]

    w2 = numpy.array(w2)
    return mutate(w2, INPUT_LAYER_SZ, OUTPUT_LAYER_SZ, 0.5, 10.0)


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


def mutate(w, sz_i, sz_j, c=0.3, rg=2.0):
    for i in range(0, sz_i):
        for j in range(0, sz_j):
            if numpy.random.random() < c:
                w[i][j] += numpy.random.random() * rg - rg/2

    return w


def cross_matrix(m1, m2, sz_i, sz_j):
    m = numpy.zeros(shape=(sz_i, sz_j))

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
    return Gene(None, None, None, w1=w1, w2=w2)


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

    genes = sorted(genes, key=lambda gene : gene.player.count)

    best = []

    for i in range(GENERATION_CNT, GENERATION_CNT * 2):
        best.append(genes[i])

    return best


def get_new_game_session(fields, games) -> []:
    best = choose_best(games)

    games.clear()

    for i in range(0, GENERATION_CNT):
        best.append(get_new_gene(best[i], best[(i + 1) % GENERATION_CNT]))

    print("Best gene from this session: \ncnt=", best[GENERATION_CNT - 1].player.count, "\nw1=", best[GENERATION_CNT-1].w1, "\nw2=", best[GENERATION_CNT-1].w2, "\n\n")

    for i in range(1, GENERATION_CNT * 2, 2):
        best[i].set_player(fields[i // 2].players[0])
        best[i].set_opponent(fields[i // 2].players[1])
        best[i].set_field(fields[i // 2])

        best[i - 1].set_player(fields[i // 2].players[1])
        best[i - 1].set_opponent(fields[i // 2].players[0])
        best[i - 1].set_field(fields[i // 2])

        games.append(GeneticGame(fields[i // 2], best[i], best[i - 1]))

    return games
