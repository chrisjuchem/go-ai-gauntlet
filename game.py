from draw import draw_game



class Game:
    def __init__(self, b_ai=None, w_ai=None, size=19):
        self.board = [[None] * size for i in range(size)]
        self.ko = None
        self.w_prisoners = []
        self.b_prisoners = []
        self.moves = 0
        self.b_ai = b_ai
        self.w_ai = w_ai
        self.size = size

    def group(self, point, color):
        grp = []
        liberties = []
        todo = [point]
        while len(todo) > 0:
            next_pt = todo.pop()
            next_st = self.board[next_pt[0]][next_pt[1]]
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

    def autoplay(self):
        for i in range(100): # while not game over
            self.b_ai.move(self)
            self.w_ai.move(self)

    def move(self, x, y):
        if self.board[x][y]:
            raise RuntimeError("Point taken")
        if (x,y) == self.ko:
            raise RuntimeError("Ko move")
        
        self.moves += 1
        self.board[x][y] = self.moves

        # self.capture
        caps = set()
        for n in self.neighbors((x, y)):
            group, libs = self.group(n, (self.moves+1) % 2)
            # if all([(self.board[l[0]][l[1]] and 
            #             (self.board[l[0]][l[1]] % 2 == self.moves % 2))
            #         for l in libs]):
            if not any([self.board[l[0]][l[1]] is None for l in libs]): 
                caps.update(group)
        if len(caps) == 0:
            _, self_libs = self.group((x,y), (self.moves) % 2)
            if not any([self.board[l[0]][l[1]] is None for l in self_libs]):
                # Suicide - undo
                self.moves -= 1
                self.board[x][y] = None
                raise RuntimeError("Suicide")
        if len(caps) == 1:
            self.ko = list(caps)[0]
        else:
            self.ko = None
        for c in caps:
            prisoners = self.w_prisoners if self.moves % 2 == 1 else self.b_prisoners
            prisoners.append((self.board[c[0]][c[1]], c))
            self.board[c[0]][c[1]] = None
