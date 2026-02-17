import time
import board
board.DISPLAY.root_group = None
import keypad
import random
import displayio
import terminalio
import adafruit_imageload
from adafruit_display_text import label

class randclass:
    rand_x = random.randint(0,18)
    rand_y = random.randint(0,12)
    def x(self):
        return random.randint(0,18)
    def y(self):
        return random.randint(0,12)
    def xy(self):
        rand_x = random.randint(0,18)
        rand_y = random.randint(0,12)
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
palette = displayio.Palette(6)
palette[0] = 0xFF00FF #magenta
palette[1] = 0x652F8F #snake
palette[2] = 0xE7471D #red
palette[3] = 0x000000 #black
palette[4] = 0xFFFFFF #white
#0x652F8F Blinka purple
palette.make_transparent(0)
segment_color = 1
apple_color = 2

#set size of tile
tile_size = 8
#8 = normal size
#10 = big size

#set the bitmap size according to tile_size
bitmap = displayio.Bitmap(tile_size,tile_size*4,6)
#color palette
for y in range(tile_size,2*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = segment_color
for y in range(2*tile_size,3*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = apple_color
#round apple corners
bitmap[0,tile_size*2] = 0
bitmap[tile_size-1,tile_size*2] = 0
bitmap[0,tile_size*3-1] = 0
bitmap[tile_size-1,tile_size*3-1] = 0
for y in range(3*tile_size,4*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = 3

head_bitmap, head_palette = adafruit_imageload.load(
    "assets/tile_size_8/snake_head.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
head_palette.make_transparent(0)
background_bitmap, background_palette = adafruit_imageload.load(
    "assets/tile_size_8/background.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
background_tilegrid = displayio.TileGrid(
    background_bitmap,
    pixel_shader = background_palette,
    width= 160//tile_size,
    height=128//tile_size,
    tile_height=2,
    tile_width=2,
    default_tile= 5)
background = displayio.Group(scale=4)
background.append(background_tilegrid)
for y in range(2):
    for x in range(20):
        background_tilegrid[x,y]=0
for x in range(0,20,2):
    background_tilegrid[x,2]=5
for x in range(0,20,2):
    background_tilegrid[x+1,2]=6
for x in range(0,20,2):
    background_tilegrid[x,15]=17
for x in range(0,20,2):
    background_tilegrid[x+1,15]=18
for y in range(3,15,2):
    background_tilegrid[0,y]=12
for y in range(3,15,2):
    background_tilegrid[0,y+1]=8
for y in range(3,15,2):
    background_tilegrid[19,y]=15
for y in range(3,15,2):
    background_tilegrid[19,y+1]=11
for y in range(3,15):
    for x in range(1,19):
        if (x + y) % 2==0:
            background_tilegrid[x,y]=10
        else:
            background_tilegrid[x,y]=9
background_tilegrid[0,2]=4
background_tilegrid[19,2]=7
background_tilegrid[0,15]=16
background_tilegrid[19,15]=19
day = "day"
night = "night"
snow = "snow"
lava = "lava"
desert = "desert"
forest = "forest"
sea = "sea"
space = "space"
basic = "basic"
custom = "custom"
random_theme = "random"
random_option = None
options_list = [day,night,snow,lava,desert,forest,sea,space,basic]
def background_color(theme,part=None,hex=None):
    if theme == "day":
        background_palette[0] = 0x4A752C #score bar
        background_palette[1] = 0x568A34 #border
        background_palette[2] = 0xA2D148 #dark in checkerboard
        background_palette[3] = 0xAAD750 #light in checkerboard
        print("Theme selected:",theme)
    elif theme == "night":
        background_palette[0] = 0x262428 #score bar
        background_palette[1] = 0x2C2730 #border
        background_palette[2] = 0x443E4C #dark in checkerboard
        background_palette[3] = 0x494351 #light in checkerboard
        print("Theme selected:",theme)
    elif theme == "snow":
        background_palette[0] = 0x758A8A #score bar
        background_palette[1] = 0x879fA1 #border
        background_palette[2] = 0xD2E4E5 #dark in checkerboard
        background_palette[3] = 0xDFEBED #light in checkerboard
        print("Theme selected:",theme)
    elif theme == "lava":
        background_palette[0] = 0x762E2E #score bar
        background_palette[1] = 0xA33F3D #border
        background_palette[2] = 0x673231 #dark in checkerboard
        background_palette[3] = 0x6E3535 #light in checkerboard
        print("Theme selected:",theme)
    elif theme == "desert":
        background_palette[0] = 0x725E1D #score bar
        background_palette[1] = 0x977B26 #border
        background_palette[2] = 0xECCE79 #dark in checkerboard
        background_palette[3] = 0xF2D78C #light in checkerboard
        print("Theme selected:",theme)
    elif theme == "forest":
        background_palette[0] = 0x202823 #score bar
        background_palette[1] = 0x253227 #border
        background_palette[2] = 0x3B4F3F #dark in checkerboard
        background_palette[3] = 0x3F5543 #light in checkerboard
        print("Theme selected:",theme)
    elif theme == "sea":
        background_palette[0] = 0x1E457C #score bar
        background_palette[1] = 0x275BA5 #border
        background_palette[2] = 0xA3C5F5 #dark in checkerboard
        background_palette[3] = 0xB4D0F9 #light in checkerboard
        print("Theme selected:",theme)
    elif theme == "space":
        background_palette[0] = 0x442A6F #score bar
        background_palette[1] = 0x604096 #border
        background_palette[2] = 0x3D285D #dark in checkerboard
        background_palette[3] = 0x432C68 #light in checkerboard
        print("Theme selected:",theme)
    elif theme == "basic":
        background_palette[0] = 0x101010 #score bar
        background_palette[1] = 0x101010 #border
        background_palette[2] = 0x000000 #dark in checkerboard
        background_palette[3] = 0x000000 #also dark in checkerboard
        print("Theme selected:",theme)
    elif theme == "custom":
        if part == "score":
            background_palette[0] = hex
        if part == "border":
            background_palette[1] = hex
        if part == "grid":
            background_palette[2] =  hex
            #brighten the the secondary tiles
            r = (hex >> 16) & 0xFF
            g = (hex >> 8) & 0xFF
            b = hex & 0xFF
            f = 1.05
            r2, g2, b2 = [min(int(c * f), 255) for c in (r, g, b)]
            background_palette[3] = (r2 << 16) + (g2 << 8) + b2
    elif theme == "random":
        random_option = random.choice(options_list)
        print("Random theme")
        background_color(random_option)

background_color(random_theme)

game_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader= palette,
    width=(160-tile_size)//tile_size,
    height=(120-tile_size*2)//tile_size,
    tile_width=tile_size,
    tile_height=tile_size,
    default_tile=0,
    x = tile_size//2,
    y = tile_size*2+tile_size//2,)
apple_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader= palette,
    width=(160-tile_size)//tile_size,
    height=(120-tile_size*2)//tile_size,
    tile_width=tile_size,
    tile_height=tile_size,
    default_tile=0,
    x = tile_size//2,
    y = tile_size*2+tile_size//2,)
head_tilegrid = displayio.TileGrid(
    head_bitmap,
    pixel_shader= head_palette,
    width=(160-tile_size)//tile_size,
    height=(120-tile_size*2)//tile_size,
    tile_width=tile_size,
    tile_height=tile_size,
    default_tile=4,
    x = tile_size//2,
    y = tile_size*2+tile_size//2,)

#snake and body logic
segment = []
apples = []
head_x = None
head_y = None
apple_xy = None
def snake(operation,x=None,y=None):
    global last_color
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
new = "new" #add new segment at head location
tail = "tail" #removes tail
update = "update"#adds new segment at head and removes segment at tail
seg_xy = "seg_xy"#add segment at defined coordinates
remove = "remove"#removes apple

#game group
game_group = displayio.Group()
game_group.append(apple_tilegrid)
game_group.append(game_tilegrid)
lose_group = displayio.Group()

#root group
root_group = displayio.Group()
root_group.append(background)
root_group.append(game_group)
root_group.append(head_tilegrid)
display.root_group = root_group

input_cooldown = False
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
    old_head_x = 10
    old_head_y = 6
    head_x = 10
    head_y = 6
    snake(seg_xy,8,6)
    snake(seg_xy,9,6)
    snake(new)
    #speed that game runs at
    speed_level = 1
    game_speed = -0.1*speed_level + 1.1
        #speed_level = game_speed
        #         1  =  1
        #         2  = 0.9
        #         3  = 0.8
        #         4  = 0.7
        #         5  = 0.6
        #         6  = 0.5
        #         7  = 0.4
        #         8  = 0.3
        #         9  = 0.2
        #         10 = 0.1
lose = False
score = 0
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
        if lose == False:
            current_time = time.monotonic()
            if current_time - last_time > game_speed:
                last_time = time.monotonic()
                #game loop
                if direction_left:
                    old_head_x = head_x
                    old_head_y = head_y
                    head_x -= 1
                if direction_right:
                    old_head_x = head_x
                    old_head_y = head_y
                    head_x += 1
                if direction_up:
                    old_head_x = head_x
                    old_head_y = head_y
                    head_y -= 1
                if direction_down:
                    old_head_x = head_x
                    old_head_y = head_y
                    head_y += 1

                input_cooldown= False
                if 0 > head_x or head_x>= 19 or 0 > head_y or head_y >= 13:
                    lose = True
                    print("lose =",lose)
                    loseword =f"lose {lose}"
                    lose_text = label.Label(terminalio.FONT,text =loseword)
                    root_group.append(lose_text)
                else:
                    snake(new)
                    if direction_left:
                        head_tilegrid[head_x,head_y] =2
                    if direction_right:
                        head_tilegrid[head_x,head_y] =3
                    if direction_up:
                        head_tilegrid[head_x,head_y] =0
                    if direction_down:
                        print(True)
                        head_tilegrid[head_x,head_y] =1
                    head_tilegrid[old_head_x,old_head_y] =4
                    apple_snake = any(xy in apples for xy in segment)
                    if apple_snake:
                        apple(update)
                        score += 1
                    else:
                        snake(tail)





