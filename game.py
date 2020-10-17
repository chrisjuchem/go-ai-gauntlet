from draw import draw_game
from ai import RandomAI
from debug import debug, info

class BoardIter:
    def __init__(self, board):
        self.board = board
        self.x = 0
        self.y = 0
    def __next__(self):
        if self.y >= self.board.size:
            self.y = 0
            self.x += 1
        if self.x >= self.board.size:
            raise StopIteration()
        ret = (self.board[self.x][self.y], (self.x,self.y))
        self.y += 1
        return ret

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[None] * size for i in range(size)]

    def __iter__(self):
        return BoardIter(self)

    def __getitem__(self, x):
        if isinstance(x, int):
            return self.board[x] # board[x] of board[x][y]
        else:
            return self.board[x[0]][x[1]]  # board[(x, y)]

    def __setitem__(self, key, value):
        #[x][y] form only needs the gen implemented, the set is on the inner list
        self.board[key[0]][key[1]] = value


class Game:
    def __init__(self, b_ai=RandomAI(), w_ai=RandomAI(), size=19):
        self.board = Board(size)
        self.ko = None
        self.w_prisoners = []
        self.b_prisoners = []
        self.moves = 0
        self.last_move = None
        self.b_ai = b_ai.init_game(self, 1)
        self.w_ai = w_ai.init_game(self, 0)
        self.size = size #remove
        self.komi = 6.5
        self.passes = 0

    def group(self, point, color):
        grp = []
        liberties = []
        todo = [point]
        while len(todo) > 0:
            next_pt = todo.pop()
            next_st = self.board[next_pt]
            if (next_st and next_st % 2) == color:
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
        if pt[0]<self.size-1:
            ns.append((pt[0]+1, pt[1]))
        if pt[1]>0:
            ns.append((pt[0], pt[1]-1))
        if pt[1]<self.size-1:
            ns.append((pt[0], pt[1]+1))
        return ns

    def total_domination(self):
        # end game if all of someone's stones are captured
        if self.moves < 2:
            return False
        b = False
        w = False
        for stone, _ in self.board:
            if stone:
                if stone % 2 == 1:
                    b = True
                else:
                    w = True
                if b and w:
                    return False
        return True

    def autoplay(self):
        while self.passes < 2 and self.moves < 2000 and not self.total_domination():
            info(self.moves)
            (self.b_ai if self.moves % 2 == 0 else self.w_ai).move()
        print("Game over: {}".format(self.score()))
        print("{} moves".format(self.moves))

    def passs(self):
        self.moves += 1
        self.passes += 1
        self.last_move = "pass"

    def move(self, mv):
        "Returns: successful move "
        x, y = mv
        if self.board[x][y]:
            return False
            # raise RuntimeError("Point taken")
        if (x,y) == self.ko:
            return False
            # raise RuntimeError("Ko move")
        
        self.moves += 1
        self.board[x][y] = self.moves

        # self.capture
        caps = set()
        neighs = set(self.neighbors((x, y)))
        while len(neighs) > 0:
            n = neighs.pop()
            group, libs = self.group(n, (self.moves+1) % 2)
            if not any([self.board[l] is None for l in libs]): 
                caps.update(group)
            neighs = neighs.difference(group)
        if len(caps) == 0:
            _, self_libs = self.group((x,y), (self.moves) % 2)
            if not any([self.board[l] is None for l in self_libs]):
                # Suicide - undo
                self.moves -= 1
                self.board[x][y] = None
                return False
                # raise RuntimeError("Suicide")
        if len(caps) == 1:
            self.ko = list(caps)[0]
        else:
            self.ko = None
        for c in caps:
            prisoners = self.w_prisoners if self.moves % 2 == 1 else self.b_prisoners
            prisoners.append((self.board[c], c, self.moves))
            self.board[c] = None
        self.passes = 0
        self.last_move = (x, y)
        return True

    # need somthing else to figure out if the game is over, this counts 1 eye groups as alive
    def score(self):
        # if self.moves <10: #TODO more elegant way of not giving a score in the beginning of the game
        #     return None
        b=0
        w=self.komi
        emptys = set()
        #TODO gotta kill off the ded groups
        for stone, pos in self.board:
            if stone is None:
                emptys.add(pos)
            elif stone % 2 == 1:
                b+=1
            else:
                w+=1
        while len(emptys) > 0:
            pt = emptys.pop()
            pts, edge = self.group(pt, None)

            if all([self.board[l] % 2 == 0 for l in edge]):
                w += len(pts)
                emptys = emptys.difference(set(pts))
            elif all([self.board[l] % 2 == 1 for l in edge]):
                b += len(pts)
                emptys = emptys.difference(set(pts))
            # else:
            #     return None

        return b-w
