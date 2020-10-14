from draw import draw_game
import random
import itertools
from debug import debug

class AI:
    def __init__(self, game, color):
        self.game = game
        self.color = color # 0 or 1

class HumanAI(AI):
    def move(self):
        inp = input("{} to move: ".format(
            "Black" if self.game.moves % 2 == 0 else "White"
        ))
        if inp == "pic":
            draw_game(self.game)
            return self.move(self.game)
        parts = inp.split(" ")
        x = int(parts[0]) - 1
        y = int(parts[1]) - 1
        self.game.move(x, y)


class HeuristicAI(AI):
    def candidate(self, mv):
        """
        Calculated on all moves to reject moves before priority calculation
        Implement this over `reject` if calculating `priority` is more expensive
        """
        return True

    def priority(self, mv):
        """
        Assign a score to each move. Lower is better. Ties broken randomly.
        """
        return 1

    def reject(self, mv):
        """
        Calculated on one move at a time in priority oreder only until a move is found
        Implement this over `candidate` if this is more expensive than `priority`
        """
        return False

    def move(self):
        allmoves = [pt for m, pt in self.game.board if m is None and self.candidate(pt)]
        debug("candidates done")
        random.shuffle(allmoves)
        allmoves.sort(key=self.priority)
        debug("sort done")
        for mv in allmoves:
            if not self.reject(mv) and self.game.move(mv[0], mv[1]):
                return
        self.game.passs()


class RandomAI(HeuristicAI):
    name = "random-ai"

class OddDiagonalAI(HeuristicAI):
    name = "odd-diagonal"
    def priority(self, mv):
        return (mv[0] + mv[1]) % 2

class EvenDiagonalAI(HeuristicAI):
    name = "even-diagonal"
    def priority(self, mv):
        return (mv[0] + mv[1] + 1) % 2

class AlphabeticalAI(HeuristicAI):
    name = "alphabetical"
    def priority(self, mv):
        return (mv[0] * 100 - mv[1]) 

class ReverseAlphabeticalAI(AlphabeticalAI):
    name = "reverse-alphabetical"
    def priority(self, mv):
        return super(ReverseAlphabeticalAI, self).priority(mv) * -1 


ALL = [RandomAI, OddDiagonalAI, EvenDiagonalAI, AlphabeticalAI]