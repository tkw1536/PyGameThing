"""
The dict MOVES is a map of key value pairs for the board
my board is numbered  1 to n9
"""
import typing

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


class Board(object):
    def __init__(self):
        """ Creates a new Board() instance """

        # all fields are empty
        self.fields = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # we start with player 1
        self.current = 1

    def getCurrentPlayer(self) -> int:
        """ Gets the current player """
        return self.current

    def getField(self, row: int, col: int) -> int:
        """ returns the value of the field 0,1,2

        :param row: Row of field to get
        :param col: Column of field to get
        """

        return self.fields[row][col]

    def __str__(self) -> str:
        """ Turns the board into a string (for printing) """

        playermap = {
            0: ' ',
            1: 'X',
            2: 'O'
        }

        return "\n---------\n".join([
            " | ".join([
                playermap[cell] for cell in row
            ])
            for row in self.fields
        ])

    def makeMove(self, move: typing.Tuple[int, int]):
        """ Makes a move on the board by updating a cell to the current player

        :param move: Move to make
        """

        (row, column) = move
        self.fields[row][column] = self.current

    def hasWon(self, player: int) -> bool:
        """ checks if a given player has won the game

        :param player: Player to check for
        """

        return (self.fields[0][0] == player and self.fields[0][1] == player and
                self.fields[0][2] == player) or \
               (self.fields[1][0] == player and self.fields[1][1] == player and
                self.fields[1][2] == player) or \
               (self.fields[2][0] == player and self.fields[2][1] == player and
                self.fields[2][2] == player) or \
               (self.fields[0][0] == player and self.fields[1][0] == player and
                self.fields[2][0] == player) or \
               (self.fields[0][1] == player and self.fields[1][1] == player and
                self.fields[2][1] == player) or \
               (self.fields[0][2] == player and self.fields[1][2] == player and
                self.fields[2][2] == player) or \
               (self.fields[0][0] == player and self.fields[1][1] == player and
                self.fields[2][2] == player) or \
               (self.fields[0][2] == player and self.fields[1][1] == player and
                self.fields[2][0] == player)

    def isFull(self) -> bool:
        """ checks if the board is full """

        for row in self.fields:
            for cell in row:
                if cell == 0:
                    return False

        return True

    def isOver(self) -> bool:
        """ Checks if the game is over by checking if a player has won or
        the board is full """

        return self.hasWon(1) or self.hasWon(2) or self.isFull()

    def getResult(self) -> int:
        """ if the game is over, returns the current result: 1 or 2 if a player
        has won, 0 otherwise """

        if self.hasWon(1):
            return 1
        elif self.hasWon(2):
            return 2
        else:
            return 0
