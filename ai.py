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
    def move(self, game):
        i=0
        while i<15:
            i+=1
            x = random.randrange(game.size)
            y = random.randrange(game.size)
            try:
                game.move(x, y)
                print(i, " attempts")
                return
            except RuntimeError:
                continue
            except KeyboardInterrupt as k:
                draw_game(game)
                raise k
        i=0
        allmoves = list(itertools.product(range(game.size), range(game.size)))
        random.shuffle(allmoves)
        for mv in allmoves:
            i+=1
            try:
                game.move(mv[0], mv[1])
                print(i, " brute force attempts")
                return
            except RuntimeError:
                continue
        print("PASS")
        game.passs()
