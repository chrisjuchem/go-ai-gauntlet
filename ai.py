from draw import draw_game
import random

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
        while True:
            i+=1
            x = random.randrange(game.size)
            y = random.randrange(game.size)
            try: 
                game.move(x, y)
                print(i, " attempts")
                return
            except RuntimeError:
                continue
