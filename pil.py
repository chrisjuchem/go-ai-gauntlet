from PIL import Image
from PIL.ImageDraw import ImageDraw

STONE_SIZE = 30
BOARD_SIZE = 19

BOARD = [[None] * BOARD_SIZE] * BOARD_SIZE
BOARD[4][4] = 1
BOARD[3][16] = 2

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

im.show()
