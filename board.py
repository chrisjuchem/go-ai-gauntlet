from constants import *

_gn = 0
class Group:
    def __init__(self):
        global _gn
        self.gn = _gn
        _gn += 1
        self.pts = set()
        self.libs = set()

    def refresh_libs(self, board):
        self.libs = set()
        for p in self.pts:
            for np in board.neighbors(p):
                if board.stones[np] == EMPTY:
                    self.libs.add(np)


class BoardIter:
    def __init__(self, board):
        self.board = board
        self.n=0
    def __next__(self):
        self.n += 1
        if self.n >= len(self.board.stones):
            raise StopIteration()
        if self.board.stones[self.n] is WALL:
            return self.__next__()
        else: 
            return self.board.stones[self.n], self.board.to_2d(self.n)

class Board:
    def __init__(self, size):
        self.size = size
        self.stones = [WALL] * (size + 1) + \
            ([WALL] + [EMPTY] * size) * size + \
            [WALL] * (size + 2)
        self.groups = [None] * ((size + 1) * (size + 2) + 1)
        #TODO groups set

    def __iter__(self):
        return BoardIter(self)

    def to_2d(self, p):
        return (p % (self.size + 1)) - 1, (p // (self.size + 1)) - 1

    def to_1d(self, pt):
        return (self.size + 1) * (pt[1] + 1) + pt[0] + 1
    
    def __getitem__(self, pt):
        return self.stones[self.to_1d(pt)]

    def neighbors(self, p):
        return (p+1, p-1, p+(self.size+1), p-(self.size+1))

    def join_groups(self, c1, c2):
        c1.pts.update(c2.pts)
        c1.libs.update(c2.libs)
        for p in c2.pts:
            self.groups[p]=c1
        return c1

    def move(self, pt, color): # pt: [0, size-1]^2
        p = self.to_1d(pt)
        c = Group()
        c.pts.add(p)
        self.groups[p] = c
        self.stones[p] = color
        caps = set()
        for n in self.neighbors(p):
            # if self.groups[n]:
            #     self.groups[n].libs.discard(p)

            if self.stones[n] == EMPTY:
                c.libs.add(n)
            elif self.stones[n] == color:
                c = self.join_groups(self.groups[n], c)
                c.libs.discard(p)
            elif self.stones[n]: # enemy
                nc = self.groups[n]
                nc.libs.discard(p)
                if len(nc.libs) == 0:
                    caps.update(nc.pts) # (PushPoints) #3
                    self.clear_group(nc)
        new_ko = self.to_2d(list(caps)[0]) if len(caps) == 1 else None
        if len(c.libs) == 0:
            self.clear_group(c)
            caps.update(c.pts) # we dont count prisoners so we can just combine these for drawing
        return map(self.to_2d, caps), new_ko

    def clear_group(self, group_to_cap):
        groups_to_refresh = set()
        for capd_pt in group_to_cap.pts:
            self.stones[capd_pt] = EMPTY #1
            self.groups[capd_pt] = None  #1
            for capd_neighbor in self.neighbors(capd_pt):
                if self.groups[capd_neighbor]:
                    groups_to_refresh.add(self.groups[capd_neighbor]) #4
        for capd_neighbor_groups in groups_to_refresh:
            capd_neighbor_groups.refresh_libs(self)

    def hash(self):
        place = 1
        hsh = 0
        for s in self.stones:
            if s is not WALL:
                hsh += s*place
                place *= 3
        return hsh

    def debug(self):
        res = ""
        for i,v in enumerate(self.stones):
            if v == WHITE:
                res += "W"
            if v == BLACK:
                res += "B"
            if v == EMPTY:
                res += "."
            if v == WALL:
                res += "#"
            if (i+1) % (self.size+1) == 0:
                res+="\n"
        res+="\n"
        for i,v in enumerate(self.groups):
            for n,g in enumerate(set(self.groups)):
                if v == g:
                    if self.stones[i] is not WALL:
                        res += str(g.gn) if g else '.'
                    else: 
                        res += "#"
            if (i+1) % (self.size+1) == 0:
                res+="\n"
        print(res)