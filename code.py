import time
import board
import keypad
import random
import displayio
import terminalio
from adafruit_display_text import label

class randclass:
    rand_x = random.randint(0,19)
    rand_y = random.randint(0,13)
    def x(self):
        return random.randint(0,19)
    def y(self):
        return random.randint(0,13)
    def xy(self):
        rand_x = random.randint(0,19)
        rand_y = random.randint(0,13)
        return rand_x,rand_y
rand = randclass()

#add keypad as keys
keys = keypad.ShiftRegisterKeys(
    clock= board.BUTTON_CLOCK,
    data=  board.BUTTON_OUT,
    latch= board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
    interval=0.01,
)

class buttonhandler:
    """
    Handles button inputs for the game.
    Usage: button.a, button.b, button.up, etc.
    """
    @property
    def b(self):
        return buttons.key_number==0
    @property
    def a(self):
        return buttons.key_number==1
    @property
    def start(self):
        return buttons.key_number==2
    @property
    def select(self):
        return buttons.key_number==3
    @property
    def right(self):
        return buttons.key_number==4
    @property
    def down(self):
        return buttons.key_number==5
    @property
    def up(self):
        return buttons.key_number==6
    @property
    def left(self):
        return buttons.key_number==7
button: buttonhandler = buttonhandler()
"""
Returns button key number from keys.events.get()
    Inputs: a, b, start, select, up, down, left, right
"""

#initializing the display
display = board.DISPLAY
display.refresh()

#defining the colors in the palette
palette = displayio.Palette(4)
palette[0] = 0xFF00FF #magenta
palette[1] = 0x00FF00 #green
palette[2] = 0xFF0000 #red
palette.make_transparent(0)
segment_color = 1
apple_color = 2

#set size of tile
tile_size = 8

#set the bitmap size according to tile_size
bitmap = displayio.Bitmap(tile_size,tile_size*4,4)
#color palette 1
for y in range(tile_size,2*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = segment_color

for y in range(2*tile_size,3*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = apple_color

#game tile grid
game_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader= palette,
    width=160//tile_size,
    height=120//tile_size,
    tile_width=tile_size,
    tile_height=tile_size,
    default_tile=0,
    x = 0,
    y = 16,
)
apple_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader= palette,
    width=160//tile_size,
    height=120//tile_size,
    tile_width=tile_size,
    tile_height=tile_size,
    default_tile=0,
    x = 0,
    y = 16,
)

#segments of snake body
segment = []

head_x = None
head_y = None
def snake(operation,x=None,y=None):
    if operation == "new":
        segment.insert(0,(head_x,head_y))
    if operation == "tail":
        oldx,oldy = segment.pop()
        game_tilegrid[oldx,oldy] = 0
    if operation == "update":
        segment.insert(0,(head_x,head_y))
        oldx,oldy = segment.pop()
        game_tilegrid[oldx,oldy] = 0
    if operation == "seg_xy":
        segment.insert(0,(x,y))
    for x,y in segment:
        game_tilegrid[x, y] = segment_color
new = "new" #add new segment at head location
tail = "tail" #removes tail
update = "update"#adds new segment at head and removes segment at tail
seg_xy = "seg_xy"#add segment at defined coordinates
remove = "remove"#removes apple
apples = []
apple_xy = None
def apple(operation,x=None,y=None):
    if operation == "new":
        apples.insert(0,rand.xy())
    if operation == "remove":
        if apples:
            oldx,oldy = apples.pop()
            apple_tilegrid[oldx,oldy] = 0
    if operation == "update":
        apples.insert(0,rand.xy())
        oldx,oldy = apples.pop()
        apple_tilegrid[oldx,oldy] = 0
    if operation == "seg_xy":
        apples.insert(0,(x,y))
    for x,y in apples:
        apple_tilegrid[x, y] = apple_color
        global apple_xy
        apple_xy = x,y
    print("apple is located at",apple_xy)




#game group
game_group = displayio.Group()
game_group.append(apple_tilegrid)
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
#initialize game variables
if True:
    #snake start position
    head_x = 10
    head_y = 6
    snake(seg_xy,8,6)
    snake(seg_xy,9,6)
    snake(new)
    #speed that game runs at
    game_speed = 0.7

last_time = time.monotonic()
while True:
    buttons = keys.events.get()
    if buttons:
        if button.left:
            left_held = buttons.pressed
        if button.right:
            right_held = buttons.pressed
        if button.up:
            up_held = buttons.pressed
        if button.down:
            down_held = buttons.pressed
        if button.start:
            start_pressed = True
    #checks if moving left or right
    if direction_left or direction_right:
        #checks if only up or only down held
        #if both are held they cancel out
        #NOTE: "^" is XOR
        if up_held ^ down_held:
            #input cool down to prevent from quickly pressing buttons to do a 180
            if input_cooldown == False:
                #sets the snakes direction to the button held and set cool down
                direction_up = up_held
                direction_down = down_held
                direction_left = False
                direction_right = False
                input_cooldown = True
    #checks if moving up or down
    if direction_up or direction_down:
        #checks if only left or only right held
        #if both are held they cancel out
        #NOTE: "^" is XOR
        if right_held ^ left_held:
            #input cool down to prevent from quickly pressing buttons to do a 180
            if input_cooldown == False:
                #sets the snakes direction to the button held and set cool down
                direction_left = left_held
                direction_right = right_held
                direction_up = False
                direction_down = False
                input_cooldown = True

    #checks if start pressed
    if start_pressed:
        #only run start sequence once when start pressed
        if start_sequence!= True:
            #sets all snake directions to false except for left
            start_sequence = True
            direction_up = False
            direction_down = False
            direction_right = True
            direction_left =False
            apple(new)


        current_time = time.monotonic()
        if current_time - last_time > game_speed:
            last_time = time.monotonic()
            #game loop
            if direction_left:
                head_x -= 1
            if direction_right:
                head_x += 1
            if direction_up:
                head_y -= 1
            if direction_down:
                head_y += 1
            input_cooldown= False
            snake(new)
            apple_snake = any(xy in apples for xy in segment)
            if apple_snake:
                apple(update)
            else:
                snake(tail)



            #print(apple,segment)
            #print("direction","    up =",direction_up,"    down =",direction_down,"    left =",direction_left,"    right =",direction_right)
            #print("pressed  ","    up =",up_held,"    down =",down_held,"    left =",left_held,"    right =",right_held)
            #print("")
