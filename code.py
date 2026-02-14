import time
import board
import keypad
import displayio
import terminalio
import adafruit_imageload
#from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

#initializing the display
display = board.DISPLAY
display.refresh()

keys = keypad.ShiftRegisterKeys(
    clock= board.BUTTON_CLOCK,
    data=  board.BUTTON_OUT,
    latch= board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True, # 74HC165 on PyBadge is active-high
    interval=0.01,
)

#text = "test"
#font = terminalio.FONT
#color = 0x0000FF
#the text label
#text_area = label.Label(font, text=text, color=color)

#text_area.x = 20
#text_area.y = 20

palette = displayio.Palette(4)
palette[0] = 0xFF00FF # red
palette[1] = 0x00FF00 # green
palette.make_transparent(0)

bitmap = displayio.Bitmap(8,24,4)
for y in range(8,16):
    for x in range(8):
        bitmap[x,y] =1




# make the color at 0 index transparent.
palette.make_transparent(0)

snake_body = displayio.TileGrid(
    bitmap,
    pixel_shader= palette,
    width=24,
    height=20,
    tile_width=8,
    tile_height=8,
    default_tile=0,
    x = 0,
    y = 0,


)
snake_body[3,3] = 1
snake_body_group = displayio.Group()
snake_body_group.append(snake_body)
#test = list()
#for i in test:
group = displayio.Group()
group.append(snake_body_group)

#group.append(text_area)

def button(button_type):
    if button_type == "b":
        return buttons.key_number==0
    if button_type == "a":
        return buttons.key_number==1
    if button_type == "start":
        return buttons.key_number==2
    if button_type == "select":
        return buttons.key_number==3
    if button_type == "right":
        return buttons.key_number==4
    if button_type == "down":
        return buttons.key_number==5
    if button_type == "up":
        return buttons.key_number==6
    if button_type == "left":
        return buttons.key_number==7

a="a"
b="b"
up="up"
down="down"
left="left"
right="right"
start="start"
select="select"

display.root_group = group
while True:
    buttons = keys.events.get()
    if buttons:
        if button(right) and buttons.pressed:
            print(right)
    pass

