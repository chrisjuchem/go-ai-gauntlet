from draw import draw_game
from ai import RandomAI
from debug import debug, info
from board import Board
from constants import *
from collections import namedtuple

Move = namedtuple("Move", ["color", "pt", "caps"])

class Game:
    def __init__(self, b_ai=RandomAI(), w_ai=RandomAI(), size=19):
        self.board = Board(size)
        self.ko = None
        self.prev_state = self.board.hash()
        self.history = [] # (color, point, set(caps))
        self.b_ai = b_ai.init_game(self, BLACK)
        self.w_ai = w_ai.init_game(self, WHITE)
        self.komi = 6.5

    @property
    def moves(self):
        return len(self.history)

    def two_passes(self):
        return len(self.history) > 1 and self.history[-1].pt == PASS and self.history[-2].pt == PASS

    def autoplay(self):
        while not self.two_passes() and self.moves < 2000 and not self.total_domination():
            info(self.moves)
            (self.b_ai if self.moves % 2 == 0 else self.w_ai).move()
        print("Game over: {}".format(self.score()))
        print("{} moves".format(self.moves))

    def passs(self):
        to_move = (self.moves % 2) + 1
        self.history.append(Move(to_move, PASS, []))

    def move(self, mv):
        """Returns: (bool) successful move"""
        if self.board[mv]:
            return False
            # raise RuntimeError("Point taken")
        if mv == self.ko:
            return False
            # raise RuntimeError("Ko move")
        
        to_move = (self.moves % 2) + 1
        caps, self.ko = self.board.move(mv, to_move)

        h = self.board.hash()
        if h == self.prev_state:
            # TODO implement undo and have this work for all cases (self.ko = 2 move ago, this = 1)
            return False
            # raise RuntimeError("Positional Super-ko violation")

        self.history.append(Move(to_move, mv, caps))
        self.prev_state = h
        return True

    def total_domination(self):
        # end game if all of someone's stones are captured
        if self.moves < 2:
            return False
        b = False
        w = False
        for stone in self.board.stones:
            if stone == BLACK:
                b = True
            elif stone == WHITE:
                w = True
            if b and w:
                return False
        return True

    def score(self):
        b=0
        w=self.komi
        emptys = set()
        for stone, pos in self.board:
            if stone == EMPTY:
                emptys.add(pos)
            elif stone == BLACK:
                b+=1
            else:
                w+=1
        while len(emptys) > 0:
            pt = emptys.pop()
            pts, edge = self.group(pt, EMPTY)

            if all([self.board[l] == WHITE for l in edge]):
                w += len(pts)
            elif all([self.board[l] == BLACK for l in edge]):
                b += len(pts)
            emptys = emptys.difference(set(pts))

        return b-w

    def group(self, point, color):
        grp = []
        liberties = []
        todo = [point]
        while len(todo) > 0:
            next_pt = todo.pop()
            next_st = self.board[next_pt]
            if next_st == color:
                grp.append(next_pt)
                for n in self.neighbors(next_pt):
                    if n not in grp and n not in liberties and n not in todo:
                        todo.append(n)
            else:
                liberties.append(next_pt)
        return grp, liberties

    def neighbors(self, pt):
        ns = []
        if pt[0]>0:
            ns.append((pt[0]-1, pt[1]))
        if pt[0]<self.board.size-1:
            ns.append((pt[0]+1, pt[1]))
        if pt[1]>0:
            ns.append((pt[0], pt[1]-1))
        if pt[1]<self.board.size-1:
            ns.append((pt[0], pt[1]+1))
        return ns
