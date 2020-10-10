from PIL import Image
from PIL.ImageDraw import ImageDraw
from functools import reduce

STONE_SIZE = 30

STARPOINTS = [(3,3), (3,9), (3,15), (9,3), (9,9), (9,15), (15,3), (15,9), (15,15)]

BLACK = (0,0,0)
WHITE = (255,255,255)

def box(w,h,center):
    return ((center[0] - w/2, center[1] - h/2), (center[0] + w/2, center[1] + h/2))

def pix(coords):
    return (STONE_SIZE * (coords[0] + 0.5), STONE_SIZE * (coords[1] + 0.5)) 

def draw_game(game):
    BOARD_SIZE = len(game.board)
    im = Image.new("RGB", [STONE_SIZE * BOARD_SIZE] * 2, (235,222,151))
    draw = ImageDraw(im)

    min_pix = STONE_SIZE / 2
    max_pix = STONE_SIZE * (BOARD_SIZE - 0.5) 
    for i in range(BOARD_SIZE):
        x = (i + 0.5) * STONE_SIZE
        draw.line(((min_pix, x), (max_pix, x)), BLACK)
        draw.line(((x, min_pix), (x, max_pix)), BLACK)
    for p in STARPOINTS:
        draw.ellipse(box(4,4,pix(p)), BLACK)

    stones = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            stone = game.board[x][y]
            if stone:
                stones.append((stone, (x,y)))
    stones.sort(key=lambda x: x[0])

    ims = [im]
    for stone in stones:
        new_im = ims[-1].copy()
        ims.append(new_im)
        draw = ImageDraw(new_im)
    
        mv_num, pt = stone
        center = pix(pt)
        place = box(STONE_SIZE-4, STONE_SIZE-4, pix(pt))

        draw.ellipse(
            place,
            outline=BLACK,
            fill=(BLACK if mv_num % 2 == 1 else WHITE),
        )
        text_offset = draw.textsize(str(mv_num))
        draw.text(
            (center[0] - text_offset[0]/2, center[1] - text_offset[1]/2),
            str(mv_num),
            fill=(BLACK if mv_num % 2 == 0 else WHITE),
        )

    ims += [ims[-1]] * 10
    ims[0].save("gif.gif", save_all=True, append_images=ims[1:], duration=100, loop=0)
