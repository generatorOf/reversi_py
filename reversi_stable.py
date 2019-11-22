def opposit(player):
    return int(not bool(player))



def sieve(everything, allowed="01234567"):
    return tuple(int(n) for n in filter(lambda x: x in allowed, list(everything)))[0:2]
# get a string of chaos-characters returns a tuple of first 2 numbers from the string


class Reversi:
    table = []
    reversibles = {(): [(), ...]}

    @staticmethod
    def score():
        print("the points of the player Computer:", sum([row.count(1) for row in Reversi.table]))
        print("your points:", sum([row.count(0) for row in Reversi.table]))

    @staticmethod
    def start():
        Reversi.reset_playground()
        while True:
            print(f'please input the position (y,x) for your next step')
            my_move = tuple(x for x in sieve(input()))
            if my_move in [n for n in Reversi.reversibles.keys()]:
                Reversi.set_chip(*my_move, 0)
                Reversi.score()
                Reversi.computer_takes_a_move()
                Reversi.score()
            else:
                print('mistyped? the list of valide possible steps is written here above. Try again!')

    @staticmethod
    def computer_takes_a_move():
        a = list(Reversi.reversibles.keys())
        if len(a) > 0:
            print(f'\n######## my move is on #{a[0]}# ########')
            Reversi.set_chip(*a[0], 1)
        else:
            print('I skip. There are no possible moves for me :(')
            Reversi.find_possible_next_steps(0)

    @staticmethod
    def reset_playground():
        Reversi.table = [[2 for i in range(8)] for i in range(8)]
        # 2 = nothing, 0,1 = players, 3 possible step
        Reversi.table[3][3] = 1
        Reversi.table[3][4] = 0
        Reversi.table[4][4] = 1
        Reversi.table[4][3] = 0
        Reversi.find_possible_next_steps(0)

    @staticmethod
    def turn_around(x, y, player):  # надо потом допилить
        for q, w, l in Reversi.reversibles[(x, y)]:  # hier muss er nacheinander einträge ausspucken
            for i in range(1, l):
                Reversi.table[x + q * i][y + w * i] = player

    @staticmethod
    def set_chip(x, y, player):
        if Reversi.table[x][y] == 3:
            Reversi.turn_around(x, y, player)
        Reversi.table[x][y] = player
        Reversi.find_possible_next_steps(opposit(player))

    @staticmethod
    def reset_asterisks():
        for i in range(8):
            for j in range(8):
                if Reversi.table[i][j] > 2:
                    Reversi.table[i][j] = 2
        Reversi.reversibles.clear()

    @staticmethod
    def find_possible_next_steps(player):
        print('there are the possible steps for', ("YOU (_)", "ME |%|")[player])
        Reversi.reset_asterisks()

        def is_the_next_chip(direction):
            q, w = direction

        def search_in_one_direction(direction):
            q, w = direction
            at_least = 0  # set 1 if at list  one chip is of another color
            opposit_player = opposit(player)
            for i in range(1, 8):
                tx = x + q * i  # temporary x and y values, which are to prove
                ty = y + w * i
                if tx < 0 or tx > 7 or ty < 0 or ty > 7:
                    return  # we want stay in the matrix
                tmp = Reversi.table[tx][ty]
                if tmp == player:  # breaks the search in this direction if found the same color.
                    return
                elif tmp == opposit_player:
                    at_least = 1
                elif tmp == 2 and at_least == 1:  #
                    Reversi.reversibles[(tx,ty)] = [(-q, -w, i)]
                    Reversi.table[tx][ty] = 3
                    return
                elif tmp == 3 and at_least == 1:
                    # wenn * schon gesetzt ist, es ist aber eine andere Route
                    Reversi.reversibles[(tx, ty)].append((-q, -w, i))
                    return
                elif tmp == 2 or tmp == 3:
                    return

        for x in range(8):
            for y in range(8):
                if Reversi.table[x][y] == player:  # x y
                    for d in [(-1, -1), (0, -1), (1, -1),
                              (-1, 0), (1, 0),
                              (-1, 1), (0, 1), (1, 1)]:
                        search_in_one_direction(d)
                        # search in the all directions then.
        Reversi.display_current_state()

    @staticmethod
    def display_current_state():
        print('\n  ', *[n for n in range(8)], sep='  ')
        print('  ', '\n  '.join([str(i) + ''.join([["(_)", "|%|", "   ", " * "][item] for item in Reversi.table[i]])
                                 for i in range(8)]), sep='')
        print('  ', *[n for n in range(8)], sep='  ', end='\n\n')

        print(Reversi.reversibles)


Reversi.start()