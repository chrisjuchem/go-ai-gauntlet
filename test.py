from game import Game
import ai
from draw import draw_game
from board import Board

SIZE = 19
b = ai.DilutedLeelaAI(35)
w = ai.DilutedLeelaAI(25)
g = Game(b, w, size=SIZE)

try:
    g.autoplay()
    draw_game(g,
        # dur=2000
    )
except KeyboardInterrupt as k:
    print("drawing partial game")
    draw_game(g,
        # dur=2000
    )
    # raise k
