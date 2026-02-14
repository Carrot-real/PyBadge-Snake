import time
import board
import keypad
import displayio
import terminalio
from adafruit_display_text import label

#add keypad as keys
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

#defining the colors in the palette
palette = displayio.Palette(4)
palette[0] = 0xFF00FF # magenta
palette[1] = 0x00FF00 # green
palette.make_transparent(0)
body_segment_color = 1

#change size of tile
tile_size = 8
#set the bitmap size according to tile_size
bitmap = displayio.Bitmap(tile_size,tile_size*4,4)
#color palette 1
for y in range(tile_size,20):
    for x in range(tile_size):
        bitmap[x,y] = body_segment_color

game_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader= palette,
    width=160//tile_size,
    height=120//tile_size,
    tile_width=tile_size,
    tile_height=tile_size,
    default_tile=0,
    x = 0,
    y = 8,
)
#segments of snake body
segment = []

segment.append((9,0))
for x,y in segment:
    game_tilegrid[x, y] = body_segment_color

def snake(operation):
    if operation == "new":
        segment.insert(0,(head_x,head_y))
    if operation == "tail":
        segment.pop()

#game group
game_group = displayio.Group()
game_group.append(game_tilegrid)

#root group
root_group = displayio.Group()
root_group.append(game_group)
display.root_group = root_group

#snake directions
direction_up = False
direction_down = False
direction_left = True
direction_right = False
#button held
left_held = False
right_held = False
up_held = False
down_held = False
#select_held = False
start_pressed = False
start_sequence = False

game_speed = 0.7 #speed that game runs at
last_time = time.monotonic()
while True:
    buttons = keys.events.get()
    if buttons:
        if button(left):
            left_held = buttons.pressed
        if button(right):
            right_held = buttons.pressed
        if button(up):
            up_held = buttons.pressed
        if button(down):
            down_held = buttons.pressed
        if button(start):
            start_pressed = True
    #checks if moving left or right
    if direction_left or direction_right == True:
        #checks if only up or only down held
        #if both are held they cancel out
        #NOTE: "^" is XOR
        if up_held ^ down_held:
            #sets the snakes direction to the button held
            direction_up = up_held
            direction_down = down_held
            direction_left = False
            direction_right = False
    #checks if moving up or down
    if direction_up or direction_down == True:
        #checks if only left or only right held
        #if both are held they cancel out
        #NOTE: "^" is XOR
        if left_held ^ right_held:
            #sets the snakes direction to the button held
            direction_left = left_held
            direction_right = right_held
            direction_up = False
            direction_down = False

    #checks if start pressed
    if start_pressed:
        #only run start sequence once
        if start_sequence==False:
            #sets all snake directions to false except for left
            start_sequence = True
            direction_up = False
            direction_down = False
            direction_right = False
            direction_left = True

        current_time = time.monotonic()
        if current_time - last_time > game_speed:
            last_time = time.monotonic()
            #game loop
            print("direction","    up =",direction_up,"    down =",direction_down,"    left =",direction_left,"    right =",direction_right,)
            print("pressed  ","    up =",up_held,"    down =",down_held,"    left =",left_held,"    right =",right_held,"    select = ",select_held)
            print("")
