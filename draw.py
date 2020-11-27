from PIL import Image
from PIL.ImageDraw import ImageDraw
from math import ceil
from functools import reduce
import string
from collections import defaultdict
from constants import *

STONE_SIZE = 30

CBLACK = (0,0,0)
CWHITE = (255,255,255)

def box(w,h,center):
    return ((center[0] - w/2, center[1] - h/2), (center[0] + w/2, center[1] + h/2))

def pix(coords):
    return (STONE_SIZE * (coords[0] + 0.5), STONE_SIZE * (coords[1] + 0.5)) 

def starpoints(sz):
    if sz > 12:
        d = 4
    else:
        d = 3
    pts = [
        (d-1, d-1),
        (sz-d, sz-d),
        (sz-d, d-1),
        (d-1, sz-d),
        (sz//2, sz//2),
        (sz, sz) # decorative
    ]
    if sz > 14:
        pts += [
            (d-1, sz//2),
            (sz//2, d-1),
            (sz-d, sz//2),
            (sz//2, sz-d),
        ]
    return pts

def draw_game(game, dur=50, filename="gif"):
    BOARD_SIZE = game.board.size
    img_size = (STONE_SIZE * (BOARD_SIZE + 1), STONE_SIZE * (BOARD_SIZE + 2))
    base = Image.new("P", img_size, (235,222,151))
    draw = ImageDraw(base)

    min_pix = STONE_SIZE / 2
    max_pix = STONE_SIZE * (BOARD_SIZE - 0.5) 
    for i in range(BOARD_SIZE):
        x = (i + 0.5) * STONE_SIZE
        draw.line(((min_pix, x), (max_pix, x)), CBLACK)
        draw.line(((x, min_pix), (x, max_pix)), CBLACK)
    for p in starpoints(BOARD_SIZE):
        draw.ellipse(box(4,4,pix(p)), CBLACK)
    for txt, pt in [(str(BOARD_SIZE-n), (BOARD_SIZE, n)) for n in range(BOARD_SIZE)] + \
            [("ABCDEFGHJKLMNOPQRST"[n], (n, BOARD_SIZE)) for n in range(BOARD_SIZE)]:
        center = pix(pt)
        text_offset = draw.textsize(txt)
        draw.text(
            (center[0] - text_offset[0]/2, center[1] - text_offset[1]/2),
            txt,
            fill=CBLACK,
        )
    draw.ellipse(
        box(STONE_SIZE-4, STONE_SIZE-4, pix((0,BOARD_SIZE+1))),
        outline=CBLACK,
        fill=CBLACK,
    )
    draw.ellipse(
        box(STONE_SIZE-4, STONE_SIZE-4, pix((BOARD_SIZE//2+1,BOARD_SIZE+1))),
        outline=CBLACK,
        fill=CWHITE,
    )
    text_lift = .2
    draw.text(pix((1,BOARD_SIZE+1-text_lift)), game.b_ai.name, fill=CBLACK)
    draw.text(pix((BOARD_SIZE//2+2,BOARD_SIZE+1-text_lift)), game.w_ai.name, fill=CBLACK)

    ims = [base]
    for n, mv in enumerate(game.history):
        n = n+1
        color, pt, caps = mv
        if pt == PASS:
            continue
        new_im = ims[-1].copy()
        ims.append(new_im)
        draw = ImageDraw(new_im)
    
        center = pix(pt)
        place = box(STONE_SIZE-4, STONE_SIZE-4, pix(pt)) 

        draw.ellipse(
            place,
            outline=CBLACK,
            fill=(CBLACK if color == BLACK else CWHITE),
        )
        text_offset = draw.textsize(str(n))
        draw.text(
            (center[0] - text_offset[0]/2, center[1] - text_offset[1]/2),
            str(n),
            fill=(CWHITE if color==BLACK else CBLACK),
        )
        #captures
        for cap in caps:
            tl,br = box(STONE_SIZE, STONE_SIZE, pix(cap))
            size = (int(tl[0]), int(tl[1]), int(br[0]), int(br[1]))
            patch = base.copy().crop(size)
            new_im.paste(patch, size)

    ims += [ims[-1]] * ceil(5000/dur)
    base.save("{}.gif".format(filename), save_all=True, append_images=ims, duration=dur, loop=0)
