import board
import time
import displayio
import terminalio
import adafruit_imageload
#from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
#initializing the display
display = board.DISPLAY
display.refresh()
#text = "test"
#font = terminalio.FONT
#color = 0x0000FF
#the text label
#text_area = label.Label(font, text=text, color=color)

#text_area.x = 20
#text_area.y = 20

sprite_sheet, palette = adafruit_imageload.load(
    "assets/sprite_sheet.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette,
)
# make the color at 0 index transparent.
palette.make_transparent(0)

snake_body = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=palette,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
)
snake_body_group = displayio.Group()
snake_body_group.append(snake_body)
#test = list()
#for i in test:
group = displayio.Group()
group.append(snake_body_group)
#group.append(text_area)
snake_body.x = 40
snake_body.y = 40

display.root_group = group

while True:
    pass

