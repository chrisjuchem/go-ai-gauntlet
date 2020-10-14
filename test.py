from game import Game
import ai
from draw import draw_game

SIZE = 19
g = Game(ai.AlphabeticalAI, ai.ReverseAlphabeticalAI, size=SIZE)

try:
    g.autoplay()
    draw_game(g,
        # dur=1000
    )
except KeyboardInterrupt as k:
    print("drawing partial game")
    draw_game(g)
    # raise k
