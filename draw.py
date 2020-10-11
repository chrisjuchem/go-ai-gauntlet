from PIL import Image
from PIL.ImageDraw import ImageDraw
from math import ceil
from functools import reduce
import string
from collections import defaultdict

STONE_SIZE = 30

STARPOINTS = [(3,3), (3,9), (3,15), (9,3), (9,9), (9,15), (15,3), (15,9), (15,15)]

BLACK = (0,0,0)
WHITE = (255,255,255)

def box(w,h,center):
    return ((center[0] - w/2, center[1] - h/2), (center[0] + w/2, center[1] + h/2))

def pix(coords):
    return (STONE_SIZE * (coords[0] + 0.5), STONE_SIZE * (coords[1] + 0.5)) 

def draw_game(game, dur=50):
    BOARD_SIZE = game.board.size
    base = Image.new("P", [STONE_SIZE * (BOARD_SIZE + 1)] * 2, (235,222,151))
    draw = ImageDraw(base)

    min_pix = STONE_SIZE / 2
    max_pix = STONE_SIZE * (BOARD_SIZE - 0.5) 
    for i in range(BOARD_SIZE):
        x = (i + 0.5) * STONE_SIZE
        draw.line(((min_pix, x), (max_pix, x)), BLACK)
        draw.line(((x, min_pix), (x, max_pix)), BLACK)
    for p in STARPOINTS:
        draw.ellipse(box(4,4,pix(p)), BLACK)
    for txt, pt in [(str(BOARD_SIZE-n), (BOARD_SIZE, n)) for n in range(BOARD_SIZE)] + \
            [(string.ascii_uppercase[n], (n, BOARD_SIZE)) for n in range(BOARD_SIZE)]:
        center = pix(pt)
        text_offset = draw.textsize(txt)
        draw.text(
            (center[0] - text_offset[0]/2, center[1] - text_offset[1]/2),
            txt,
            fill=BLACK,
        )

    ims = [base]
    moves = [(m[0], m[1], game.moves+2) for m in game.board if m[0]] + \
        game.w_prisoners + game.b_prisoners
    moves.sort(key=lambda x:x[0])
    caps = defaultdict(lambda:[])
    for _, pt, cap_mv in game.w_prisoners + game.b_prisoners:
        caps[cap_mv].append(pt)
    
    for n, pt, _ in moves:
        new_im = ims[-1].copy()
        ims.append(new_im)
        draw = ImageDraw(new_im)
    
        center = pix(pt)
        place = box(STONE_SIZE-4, STONE_SIZE-4, pix(pt)) 

        draw.ellipse(
            place,
            outline=BLACK,
            fill=(BLACK if n % 2 == 1 else WHITE),
        )
        text_offset = draw.textsize(str(n))
        draw.text(
            (center[0] - text_offset[0]/2, center[1] - text_offset[1]/2),
            str(n),
            fill=(BLACK if n % 2 == 0 else WHITE),
        )
        #captures
        for cap in caps[n]:
            tl,br = box(STONE_SIZE, STONE_SIZE, pix(cap))
            size = (int(tl[0]), int(tl[1]), int(br[0]), int(br[1]))
            patch = base.copy().crop(size)
            new_im.paste(patch, size)

    ims += [ims[-1]] * ceil(5000/dur)
    base.save("gif.gif", save_all=True, append_images=ims, duration=dur, loop=0)
