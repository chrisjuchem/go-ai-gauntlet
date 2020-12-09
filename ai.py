from draw import draw_game
import random
import itertools
from debug import debug, info
from leela import Leela, LEELA_INST
from constants import *

class AI:
    def init_game(self, game, color):
        self.game = game
        self.color = color
        return self

class WithSettings:
    @classmethod
    def _inst_ais(cls, args):
        return map(lambda arg: arg() if isinstance(arg, type) and issubclass(arg, AI) else arg, args)

    @classmethod
    def with_settings(cls, *args):
        return lambda: cls(*cls._inst_ais(args))


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
        self.game.move((x, y), self.color)


class MixedAI(AI, WithSettings):
    def __init__(self, primary, secondary, pct_primary, base=100):
        super().__init__()
        self.primary = primary
        self.secondary = secondary
        self.pct_primary = pct_primary
        self.base = base
        self.name = "{}%-{}-({})".format(pct_primary*100/base, primary.name, secondary.name)

    def init_game(self, game, color):
        super().init_game(game, color)
        self.primary.init_game(game, color)
        self.secondary.init_game(game, color)
        return self

    def move(self):
        if random.randrange(self.base) < self.pct_primary:
            self.primary.move()
        else:
            self.secondary.move()


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
        # debug("candidates done")
        random.shuffle(allmoves)
        allmoves.sort(key=self.priority)
        # debug("sort done")
        for mv in allmoves:
            if not self.reject(mv) and self.game.move((mv[0], mv[1]), self.color):
                return
        self.game.passs()


class RandomAI(HeuristicAI):
    name = "random"

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
        self.engine = LEELA_INST

    def init_game(self, game, color):
        super().init_game(game, color)
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
        if len(self.game.history) < -hist_idx:
            return

        mv = self.game.history[hist_idx]
        last_move = "{} {}".format(GET_COLOR_STRING(mv.color), self.tuple_to_string(mv.pt))
        if self.engine.cmd("last_move") == last_move:
            return
        else:
            self.ensure_current(hist_idx-1)
            self.engine.cmd("play " + last_move)

    def genmove(self):
        mv = self.engine.cmd("genmove "+GET_COLOR_STRING(self.color))
        if mv == "pass": #or mv == "resign":
            self.game.passs()
        else:
            self.game.move(self.string_to_tuple(mv), self.color)

