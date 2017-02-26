import Player
import Game

class Competition(object):
    def __init__(self, players):
        self.players = players
        self.points = {}
        for p in players:
            self.points[p.getName()] = 0

    def run(self, numGames):
        for (i, player1) in enumerate(self.players):
            for (j, player2) in enumerate(self.players):
                if i < j:
                    for _ in range(numGames):
                        g = Game.Game(player1, player2)
                        winner = g.run(quiet=True)

                        if winner == 1:
                            self.points[player1.getName()] += 2
                        elif winner == 2:
                            self.points[player2.getName()] += 2
                        else:
                            self.points[player1.getName()] += 1
                            self.points[player2.getName()] += 1

    def printResults(self):
        results = [(player, self.points[player.getName()]) for player in self.players]

        for (player, points) in sorted(results, key=lambda t: -t[1]):
            print("{}: {} points".format(player.getName(), points))


if __name__ == "__main__":
    p1 = Player.RandomPlayer("A")
    p2 = Player.RandomPlayer("B")
    p3 = Player.SmartPlayer("C")
    comp = Competition([p1, p2, p3])
    comp.run(5)
    comp.printResults()