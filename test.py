from game import Game
from ai import HumanAI, RandomAI
from draw import draw_game

g = Game(RandomAI(), RandomAI())
g.autoplay()
draw_game(g)