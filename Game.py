import Board
import Player


class Game(object):
    def __init__(self, player1: Player.Player, player2: Player.Player):
        """ Creates a new Game() instance

        :param player1: The name of player 1
        :param player2: The name of player 2
        """

        self.player1 = player1  #: Player
        self.player2 = player2  #: Player

        self.board = Board.Board()

    def run(self, quiet: bool = False) -> int:
        """ Plays the game and returns the winner
        :param quiet: Boolean indicating if output should be printed
        """

        while not self.board.isOver():
            if not quiet:
                print(self.board)

            # get a move from the current player
            if self.board.current == 1:
                move = self.player1.getMove(self.board)
            else:
                move = self.player2.getMove(self.board)

            # make the move
            self.board.makeMove(move)

            # Update the current player by setting self.board.current
            self.board.current = 2 if self.board.current == 1 else 1

        # print the board
        if not quiet:
            print(self.board)

        # and return the result
        return self.board.getResult()


if __name__ == "__main__":
    game = Game(Player.HumanPlayer("A"), Player.SmartPlayer("B"))
    result = game.run()

    if result == 1:
        print("{} wins with Xs".format(game.player1.getName()))
    elif result == 2:
        print("{} wins with Os".format(game.player2.getName()))
    else:
        print("The board is just full")
