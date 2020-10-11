from draw import draw_game
import random
import itertools

class HumanAI:
    def move(self, game):
        inp = input("{} to move: ".format(
            "Black" if game.moves % 2 == 0 else "White"
        ))
        if inp == "pic":
            draw_game(game)
            return self.move(game)
        parts = inp.split(" ")
        x = int(parts[0]) - 1
        y = int(parts[1]) - 1
        game.move(x, y)
        
class RandomAI:
    def passs(self, game):
        # give up if the game has progressed and all of someone's stones are captures
        if game.moves < 2:
            return False
        b = False
        w = False
        for stone, _ in game.board:
            if stone:
                if stone % 2 == 1:
                    b = True
                else:
                    w = True
                if b and w:
                    return False
        return True

    def move(self, game):
        if self.passs(game):
            game.passs()
            return
        i=0
        while i<15:
            i+=1
            x = random.randrange(game.size)
            y = random.randrange(game.size)
            if game.move(x, y):
                # print(i, " attempts")
                return
        i=0
        allmoves = [pt for m, pt in game.board if m is None]
        random.shuffle(allmoves)
        for mv in allmoves:
            i+=1
            if game.move(mv[0], mv[1]):
                # print(i, " brute force attempts")
                return
        game.passs()
