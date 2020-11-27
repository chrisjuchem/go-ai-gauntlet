from itertools import product
from ai import *
from game import Game
from draw import draw_game
from collections import namedtuple
import json

Player = namedtuple("Player", ["id", "ai"])

PLAYERS = {
    "00": RandomAI,
    "01": CenterAI,
    "02": MixedAI.with_settings(CenterAI, RandomAI, 50)
}
# Need 2 instances of each AI to support mirror matches
BPLAYERS = [Player(id, p_cls()) for id, p_cls in PLAYERS.items()]
WPLAYERS = [Player(id, p_cls()) for id, p_cls in PLAYERS.items()]
MATCHUPS = product(BPLAYERS, WPLAYERS)

def matchup_name(b, w):
    return "{}-{}__{}-{}".format(b.id, b.ai.name, w.id, w.ai.name)

GAMES_PER_MATCH = 10

RESULTS_FILE = 'results/results.json'
try:
    with open(RESULTS_FILE) as f:
        results = json.load(f)
except FileNotFoundError:
    results = {}

try:
    for b, w in MATCHUPS:
        print("simulating "+ matchup_name(b, w))
        if not results.get(b.id):
            results[b.id] = {}
        if not results[b.id].get(w.id):
            results[b.id][w.id] = {
                "name": matchup_name(b, w),
                "wins_b": 0,
                "wins_w": 0,
                "scores": [],
                "moves": [],
            }

        matchup = results[b.id][w.id]
        while len(matchup["scores"]) < GAMES_PER_MATCH:
            g = Game(b.ai, w.ai)
            score = g.autoplay()
            draw_game(g, filename="results/gifs/{}__g{}".format(matchup_name(b,w), len(matchup["scores"])))
            matchup["scores"].append(score)
            matchup["moves"].append(g.moves)
            if score < 0:
                matchup["wins_w"] += 1
            elif score > 0:
                matchup["wins_b"] += 1
    print("All games simulated!")
finally:
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)

