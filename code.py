import time
import board
import keypad
import displayio
import terminalio
from adafruit_display_text import label

#adding buttons as
keys = keypad.ShiftRegisterKeys(
    clock= board.BUTTON_CLOCK,
    data=  board.BUTTON_OUT,
    latch= board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
    interval=0.01,
)
#button(a, b, start, select, up, down, left, right)
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

palette = displayio.Palette(4)
palette[0] = 0xFF00FF # red
palette[1] = 0x00FF00 # green
palette.make_transparent(0)

bitmap = displayio.Bitmap(8,24,4)
#color palette 1
for y in range(8,16):
    for x in range(8):
        bitmap[x,y] =1

# make the color at 0 index transparent.
palette.make_transparent(0)

background = displayio.TileGrid(
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
segment_x = [1,7,3,8]
tile_index = 1
segment_y = [3,8,9,8]

for x,y in zip(segment_x, segment_y):
    background[x, y] = tile_index

snake_body_group = displayio.Group()
snake_body_group.append(background)
#test = list()
#for i in test:
group = displayio.Group()
group.append(snake_body_group)

#group.append(text_area)

left_held = False
right_held = False

display.root_group = group
while True:
    #needs to have "buttons = keys.events.get()"  otherwise the button() will look for buttons even though it does not exist
    buttons = keys.events.get()
    if buttons:
        if button(left):
            left_held = buttons.pressed


