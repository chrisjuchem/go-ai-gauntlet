from draw import draw_game
import random
import itertools
from debug import debug, info
from leela import Leela
from constants import *

class AI:
    def init_game(self, game, color):
        self.game = game
        self.color = color
        return self

class HumanAI(AI):
    def move(self):
        inp = input("{} to move: ".format(
            "Black" if self.color == BLACK else "White"
        ))
        if inp == "pic":
            draw_game(self.game)
            return self.move(self.game)
        parts = inp.split(" ")
        x = int(parts[0]) - 1
        y = int(parts[1]) - 1
        self.game.move((x, y))


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
        allmoves = [pt for c, pt in self.game.board if c == EMPTY and self.candidate(pt)]
        debug("candidates done")
        random.shuffle(allmoves)
        allmoves.sort(key=self.priority)
        debug("sort done")
        for mv in allmoves:
            if not self.reject(mv) and self.game.move((mv[0], mv[1])):
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

class CenterAI(HeuristicAI):
    name = "center"
    def priority(self, mv):
        center = self.game.board.size//2
        return abs(mv[0] - center) + abs(mv[1] - center)

class AntiCenterAI(CenterAI):
    name = "anti-center"
    def priority(self, mv):
        return super().priority(mv) * -1


class LeelaAI(AI):
    name = "leela"
    letters = "ABCDEFGHJKLMNOPQRST"

    def __init__(self):
        self.engine = Leela()

    def init_game(self, game, color):
        super().init_game(game, color)
        self.color_str = "black" if self.color == BLACK else "white"
        self.oppo_str = "black" if self.color == WHITE else "white"
        resp = self.engine.cmd("clear_board")
        if resp == "":
            info("Engine initialized")
        else:
            info("Engine initialization failed")
        return self

    def tuple_to_string(self, mv):
        if mv == PASS:
            return PASS
        return "{}{}".format(self.letters[mv[0]], self.game.board.size - mv[1])
        
    def string_to_tuple(self, mv):
        if mv == PASS:
            return PASS
        return self.letters.find(mv[0]), self.game.board.size - int(mv[1:])

    def move(self):
        self.ensure_current()
        self.genmove()

    def ensure_current(self, hist_idx=-1):
        if len(self.game.history) < -hist_idx or self.game.history[hist_idx].color == self.color:
            return
        self.ensure_current(hist_idx-1)

        last_move = "{} {}".format(self.oppo_str, self.tuple_to_string(self.game.history[hist_idx].pt))
        self.engine.cmd("play " + last_move)

    def genmove(self):
        mv = self.engine.cmd("genmove "+self.color_str)
        if mv == "pass": #or mv == "resign":
            self.game.passs()
        else:
            self.game.move(self.string_to_tuple(mv))

class DilutedLeelaAI(LeelaAI):
    def __init__(self, pct_leela, base=100):
        super().__init__()
        self.pct_leela = pct_leela
        self.base = base
        self.name = "{}%-leela".format(pct_leela*100/base)

    def move(self):
        self.ensure_current()
        if random.randrange(self.base) < self.pct_leela:
            self.genmove()
        else:
            allmoves = [pt for m, pt in self.game.board if m == EMPTY]
            random.shuffle(allmoves)
            for mv in allmoves:
                if self.game.move((mv[0], mv[1])):
                    self.engine.cmd("play {} {}".format(self.color_str, self.tuple_to_string(mv)))
                    return
            self.engine.cmd("play {} pass".format(self.color_str))
            self.game.passs()



ALL = [RandomAI, OddDiagonalAI, EvenDiagonalAI, AlphabeticalAI, LeelaAI, DilutedLeelaAI]
