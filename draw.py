from PIL import Image
from PIL.ImageDraw import ImageDraw

STONE_SIZE = 30
BOARD_SIZE = 19

BOARD = [[None] * BOARD_SIZE for i in range(BOARD_SIZE)] 
BOARD[3][3] = 1
BOARD[2][15] = 2
BOARD[2][16] = 4 

STARPOINTS = [(3,3), (3,9), (3,15), (9,3), (9,9), (9,15), (15,3), (15,9), (15,15)]

BLACK = (0,0,0)
WHITE = (255,255,255)

def box(w,h,center):
    return ((center[0] - w/2, center[1] - h/2), (center[0] + w/2, center[1] + h/2))

def pix(coords):
    return (STONE_SIZE * (coords[0] + 0.5), STONE_SIZE * (coords[1] + 0.5)) 

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

for x in range(BOARD_SIZE):
    for y in range(BOARD_SIZE):
        stone = BOARD[x][y]
        center = pix((x, y))
        place = box(STONE_SIZE-4, STONE_SIZE-4, pix((x, y)))
        if stone:
            draw.ellipse(
                place,
                outline=BLACK,
                fill=(BLACK if stone % 2 == 1 else WHITE),
            )
            text_offset = draw.textsize(str(stone))
            draw.text(
                (center[0] - text_offset[0]/2, center[1] - text_offset[1]/2),
                str(stone),
                fill=(BLACK if stone % 2 == 0 else WHITE),
            )

im.show()
