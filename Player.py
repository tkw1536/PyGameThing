import typing
import random

import Board

MOVES = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1),
    9: (2, 2)
}


class Player(object):
    def __init__(self, name: str):
        """ Creates a new Player.

        :param name: Name of player to create
        """

        self.name = name

    def getName(self) -> str:
        """ Gets the name of this player. """

        return self.name

    def getMove(self, board: Board.Board) -> typing.Tuple[int, int]:
        """ Gets the next move of this player.

        :param board: Board that the player should make a move on

        :returns: a tuple (row, column) indicating the move to be made
        """

        raise NotImplementedError


class HumanPlayer(Player):
    """ A Player controlled by a human """

    def getMove(self, board: Board.Board) -> typing.Tuple[int, int]:
        """ Gets the next move of this player.

        :param board: Board that the player should make a move on

        :returns: a tuple (row, column) indicating the move to be made
        """

        while True:
            move = input("{} please enter your move:".format(self.getName()))
            try:
                move = int(move)
            except ValueError:
                print("Please enter an integer")
                continue

            if move < 1 or move > 9:
                print("Please enter a number between 1 and 9")
                continue

            index = MOVES[move]

            if board.fields[index[0]][index[1]] == 0:
                return index

            else:
                print("This is not a valid move, please enter a move. ")


class RandomPlayer(Player):
    """ A player that makes a random move """

    def getMove(self, board: Board.Board) -> typing.Tuple[int, int]:
        """
        Gets the next move of this player.

        :param board: Board that the player should make a move on

        :returns: a tuple (row, column) indicating the move to be made
        """

        moves = []

        for (i, row) in enumerate(board.fields):
            for (j, cell) in enumerate(row):
                if cell == 0:
                    moves.append((i, j))

        return random.choice(moves)


class SmartPlayer(Player):
    """ A player that makes a smart move """

    def getMove(self, board):
        """
        Gets the next move of this player.

        :param board: Board that the player should make a move on

        :returns: a tuple (row, column) indicating the move to be made
        """

        (move, score) = SmartPlayer.minmax(
            board.fields,
            board.getCurrentPlayer(),
            board.getCurrentPlayer()
        )

        return move

    @staticmethod
    def minmax(state: typing.List[typing.List[int]], player: int, me: int) \
            -> typing.Tuple[typing.Tuple[int, int], int]:
        """ Attempts to compute the best possible move for a given player by
        recursively expanding a tree of possible moves. This assumes the worst
        case scenario, that is the other player plays optimally.

        :param state: The current state of the field
        :param player: The player in the current move
        :param me: The player to optimise for

        :returns: A tuple (move, score) with the choosen move and the score of the
        situation overall
        """

        # Check if we are inside of a 'leaf' state, i.e. one that can not be expanded
        # any further.
        if SmartPlayer.is_leaf(state):
            return ((-1, -1), SmartPlayer.leaf_score(state, me))

        newplayer = 1 if player == 2 else 2

        def process_substate(substate: typing.Tuple[
            typing.Tuple[int, int],
            typing.List[typing.List[int]]
        ]) -> typing.Tuple[typing.Tuple[int, int], int]:
            """ Recursively processes a substate

            :param substate: (move, newstate) tuple to processes

            :returns: a tuple (move, score) of the move being made and the score it
            receives
            """

            # unpack the possible move
            (move, newstate) = substate

            # compute the move recursively
            (submove, score) = SmartPlayer.minmax(newstate, newplayer, me)

            # return it along with the score
            return (move, score)

        # expand all possible moves
        moves = map(process_substate, SmartPlayer.expand_state(state, player))

        # if it is our move, we pick the one that will give us the maximal score
        if player == me:
            return SmartPlayer.argmax_efficient(moves, lambda s: s[1], 1)

        # if it is the enemys move, we assume they will make their best possible move
        # that is we minimise the score
        else:
            return SmartPlayer.argmin_efficient(moves, lambda s: s[1], -1)

    @staticmethod
    def has_winner(state: typing.List[typing.List[int]], player: int) -> bool:
        """ Checks if a given state has a given winner """

        return (state[0][0] == player and state[0][1] == player and
                state[0][2] == player) or \
               (state[1][0] == player and state[1][1] == player and
                state[1][2] == player) or \
               (state[2][0] == player and state[2][1] == player and
                state[2][2] == player) or \
               (state[0][0] == player and state[1][0] == player and
                state[2][0] == player) or \
               (state[0][1] == player and state[1][1] == player and
                state[2][1] == player) or \
               (state[0][2] == player and state[1][2] == player and
                state[2][2] == player) or \
               (state[0][0] == player and state[1][1] == player and
                state[2][2] == player) or \
               (state[0][2] == player and state[1][1] == player and
                state[2][0] == player)

    @staticmethod
    def is_full(state: typing.List[typing.List[int]]) -> bool:
        """ Checks if a given state represents a full Board

        :param state: State to check

        :returns: a boolean indicating if the board is full or not
        """

        for row in state:
            for cell in row:
                if cell == 0:
                    return False
        return True

    @staticmethod
    def is_leaf(state: typing.List[typing.List[int]]) -> bool:
        """ Checks if a state is a leaf state, that is if it can not be expanded
        further.

        :param state: State to check

        :returns: a boolean indicating the leaf
        """

        return SmartPlayer.has_winner(state, 1) or \
               SmartPlayer.has_winner(state, 2) or \
               SmartPlayer.is_full(state)

    @staticmethod
    def leaf_score(state: typing.List[typing.List[int]], player: int) -> int:
        """ Computes the score of a leaf state

        :param state: State to compute score of
        :param player: Player to optimise for

        :returns: 1 if player is winning, -1 if the enemy is winning and 0 else
        """

        if SmartPlayer.has_winner(state, player):
            return 1
        elif SmartPlayer.has_winner(state, 1 if player == 2 else 2):
            return -1
        else:
            return 0

    @staticmethod
    def expand_state(state: typing.List[typing.List[int]], player: int) \
            -> typing.Iterable[
                typing.Tuple[
                    typing.Tuple[int, int],
                    typing.List[typing.List[int]]
                ]]:
        """ Expands a state into a set of new states

        :param state: Current State of the TicTacToe board
        :param player: Player whose turn it is

        :returns: an iterator of pairs (move, state) of new expanded states
        """

        for (i, row) in enumerate(state):
            for (j, cell) in enumerate(row):
                if cell == 0:
                    # make a copy of the state
                    newstate = [[c for c in row] for row in state]

                    # make the move
                    newstate[i][j] = player

                    # and return it to the list of states
                    yield ((i, j), newstate)

    @staticmethod
    def argmax_efficient(lst, score, bound: int):
        """ Computes the argmax in an efficient way

        :param lst: List or iterator to iterate over
        :param score: Scoring function
        :param bound: Upper Bound for the maximum

        :returns: the argmax
        """

        max_val = None
        max_elem = None

        for elem in lst:
            val = score(elem)

            # if we have the bound, we can already return
            if val == bound:
                return elem

            if max_val == None or val > max_val:
                max_val = val
                max_elem = elem

        return max_elem

    @staticmethod
    def argmin_efficient(lst, score, bound: int):
        """ Computes the argmin in an efficient way

        :param lst: List or iterator to iterate over
        :param score: Scoring function
        :param bound: Lower Bound for the minimum

        :returns: the arhmin
        """

        min_val = None
        min_elem = None

        for elem in lst:
            val = score(elem)

            # if we have the bound, we can already return
            if val == bound:
                return elem

            if min_val == None or val < min_val:
                min_val = val
                min_elem = elem

        return min_elem
