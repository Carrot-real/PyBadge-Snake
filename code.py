import time
#-------In the repl displays how long each part takes to load-------
def mark(name, start_time):
    # Calculate duration in milliseconds
    duration = (time.monotonic_ns() - start_time)/1000000
    print(f"{name}: {duration:.2f} ms")
    return time.monotonic_ns()
t = time.monotonic_ns()

#-------Importing Modules-------
import board, keypad, random
import audioio, synthio #for the buzzer
import displayio, digitalio
import supervisor, microcontroller
import adafruit_imageload
import gc
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
t = mark("Load Modules", t)

#-------Initializing Display-------
display = board.DISPLAY
root_group = displayio.Group()
display.root_group = root_group
#I recompiled circuit python without the auto enable to prevent
#the screen from flickering on start for a clearer experience
backlight = digitalio.DigitalInOut(microcontroller.pin.PA01)
backlight.direction = digitalio.Direction.OUTPUT

backlight.value = False #keep screen off

t = mark("Initializing the Display", t)

#-------Load Font-------
font = bitmap_font.load_font("fonts/font.pcf")
glyphs = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ: "
font.load_glyphs(glyphs)
t = mark("Font Load", t)

#-------Initialize Speaker-------
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True
audio = audioio.AudioOut(board.SPEAKER)
synth = synthio.Synthesizer(sample_rate=22050)
audio.play(synth)
def play(frequency, duration):
    # 'press' starts the note
    note = synthio.Note(frequency=frequency)
    synth.press(note)
    time.sleep(duration)
    # 'release' stops it
    synth.release(note)
t = mark("Initialize Speaker", t)

#-------rand-------
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
rand=randclass()
t = mark("rand", t)

#-------Button Setup-------
keys=keypad.ShiftRegisterKeys(
    clock= board.BUTTON_CLOCK,
    data=  board.BUTTON_OUT,
    latch= board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
    interval=0.01,)
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
button=buttonhandler()
t = mark("Button Setup", t)

#-------Initialize Read/Write to "highscore.txt"-------
def get_high_score():
    try:
        with open("/highscore.txt", "r") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0
def save_high_score(score):
    try:
        with open("/highscore.txt", "w") as f:
            f.write(str(score))
    except OSError:
        print("ERROR: Cannot save. Did you bridge the pads at boot?")
high_score = get_high_score()
print(f"Current High Score: {high_score}")
score = 0
t = mark("Initialize Read/Write to \"highscore.txt\"", t)

#size of tile   UI scale
tile_size = 8 # 8 = default   10 = big
#-------Setup Snake and Apple Palettes and Bitmaps-------
segment_color=1
apple_color=2
shadow_color=3
#defining the colors in the palette
palette = displayio.Palette(4)
palette[0] = 0xFF00FF #magenta
palette[1] = 0x652F8F #snake    652F8F Blinka purple
palette[2] = 0xE7471D #apple
palette[3] = 0x1F1F0F
palette.make_transparent(0)
#set the bitmap size according to tile_size
bitmap = displayio.Bitmap(tile_size,tile_size*4,4)
#color palette
for y in range(tile_size,2*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = segment_color
for y in range(2*tile_size,3*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = apple_color
for y in range(3*tile_size,4*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = shadow_color
#round apple corners
bitmap[0,tile_size*2] = 0;bitmap[tile_size-1,tile_size*2] = 0
bitmap[0,tile_size*3-1] = 0;bitmap[tile_size-1,tile_size*3-1] = 0
for y in range(3*tile_size,4*tile_size):
    for x in range(tile_size):
        bitmap[x,y] = 3
t = mark("Setup Snake and Apple Palettes and Bitmaps", t)


#-------Load Images-------
print("Load Bitmap Image:")
icons_bitmap, icons_palette = adafruit_imageload.load(
    "assets/tile_size_8/score_icons.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
icons_palette.make_transparent(0)
t = mark("    score_icons.bmp", t)
head_bitmap, head_palette = adafruit_imageload.load(
    "assets/tile_size_8/snake_head.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
head_palette.make_transparent(0)
t = mark("    snake_head.bmp", t)
background_bitmap, background_palette = adafruit_imageload.load(
    "assets/tile_size_8/background.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
t = mark("    background.bmp", t)


#-------Background-------
print("Background")
#---Score Icons---
score_tilegrid = displayio.TileGrid(
    icons_bitmap,
    pixel_shader = icons_palette,
    width=4,
    height=1,
    tile_height=16,
    tile_width=16,
    default_tile=3)
score_tilegrid[0,0] = 0
score_tilegrid[3,0] = 1
#---Setting Up the Background tilegrid and Group---
background_tilegrid = displayio.TileGrid(
    background_bitmap,
    pixel_shader = background_palette,
    width= 160//tile_size*2,
    height=128//tile_size*2,
    tile_height=2,
    tile_width=2,
    default_tile=0)
foreground_tilegrid = displayio.TileGrid(
    background_bitmap,
    pixel_shader = background_palette,
    width= 160//tile_size*2,
    height=128//tile_size*2,
    tile_height=1,
    tile_width=1,
    default_tile= 7)
background_palette.make_transparent(4)
background = displayio.Group(scale=4)
foreground = displayio.Group(scale=4)
background.append(background_tilegrid)
foreground.append(foreground_tilegrid)
t = mark("    Setting Up Groups for Background", t)
#---Assembling the Background Segments--
for y in range(2,16):
    for x in range(0,20):
        if (x + y) % 2==0:
            background_tilegrid[x,y]=0
        else:
            background_tilegrid[x,y]=1
for x in range(40):
    foreground_tilegrid[x,31]=4
    foreground_tilegrid[x,4]=4
for y in range(5,32):
    foreground_tilegrid[39,y]=4
    foreground_tilegrid[0,y]=4
for x in range(40):
    foreground_tilegrid[x,0]=5
    foreground_tilegrid[x,1]=5
    foreground_tilegrid[x,2]=5
    foreground_tilegrid[x,3]=5
t = mark("    Assembling the Background", t)
day = "Day"
night = "Night"
snow = "Snow"
lava = "lava"
desert = "Desert"
forest = "Forest"
sea = "Sea"
space = "Space"
basic = "Basic"
custom = "custom"
random_theme = "random"
random_option = None
backgrounds_list = [day,night,snow,lava,desert,forest,sea,space,basic]
background_index = 0
next_background_index = 1
last_background_index = 8
current_theme= None
#---background_color Function---
def background_color(theme,part=None,hex=None):
    global current_theme
    if theme == "Day":
        background_palette[0] = 0x4A752C #score bar
        background_palette[1] = 0x568A34 #border
        background_palette[2] = 0xA2D148 #dark in checkerboard
        background_palette[3] = 0xAAD750 #light in checkerboard
    elif theme == "Night":
        background_palette[0] = 0x262428 #score bar
        background_palette[1] = 0x2C2730 #border
        background_palette[2] = 0x443E4C #dark in checkerboard
        background_palette[3] = 0x494351 #light in checkerboard
    elif theme == "Snow":
        background_palette[0] = 0x758A8A #score bar
        background_palette[1] = 0x879fA1 #border
        background_palette[2] = 0xD2E4E5 #dark in checkerboard
        background_palette[3] = 0xDFEBED #light in checkerboard
    elif theme == "Lava":
        background_palette[0] = 0x762E2E #score bar
        background_palette[1] = 0xA33F3D #border
        background_palette[2] = 0x673231 #dark in checkerboard
        background_palette[3] = 0x6E3535 #light in checkerboard
    elif theme == "Desert":
        background_palette[0] = 0x725E1D #score bar
        background_palette[1] = 0x977B26 #border
        background_palette[2] = 0xECCE79 #dark in checkerboard
        background_palette[3] = 0xF2D78C #light in checkerboard
    elif theme == "Forest":
        background_palette[0] = 0x202823 #score bar
        background_palette[1] = 0x253227 #border
        background_palette[2] = 0x3B4F3F #dark in checkerboard
        background_palette[3] = 0x3F5543 #light in checkerboard
    elif theme == "Sea":
        background_palette[0] = 0x1E457C #score bar
        background_palette[1] = 0x275BA5 #border
        background_palette[2] = 0xA3C5F5 #dark in checkerboard
        background_palette[3] = 0xB4D0F9 #light in checkerboard
    elif theme == "Space":
        background_palette[0] = 0x442A6F #score bar
        background_palette[1] = 0x604096 #border
        background_palette[2] = 0x3D285D #dark in checkerboard
        background_palette[3] = 0x432C68 #light in checkerboard
    elif theme == "Basic":
        background_palette[0] = 0x101010 #score bar
        background_palette[1] = 0x101010 #border
        background_palette[2] = 0x000000 #dark in checkerboard
        background_palette[3] = 0x000000 #also dark in checkerboard
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
        random_option = random.choice(backgrounds_list)
        background_color(random_option)
    current_theme = theme
    print("    Theme Selected:",current_theme)
background_color(day)
t = mark("    background_color Function", t)

#-------Score and Highscore-------
high_score_text = bitmap_label.Label(
    font,
    text="   ",
    x=68,
    y=10,
    scale=3,
    max_characters=3)
score_text = bitmap_label.Label(
    font,
    text="   ",
    x=19,
    y=10,
    scale=3,
    max_characters=3)
score_group = displayio.Group()
score_group.append(score_tilegrid)
score_group.append(high_score_text)
score_group.append(score_text)
score_group.hidden = True
t = mark("Add Score and High Score Numbers to Score Bar", t)

#--------Lose screen--------
lose_text = bitmap_label.Label(
    font,
    text="    ",
    scale= 4)
lose_text_score = bitmap_label.Label(
    font,
    text="    ",
    scale= 3)
lose_text_high_score = bitmap_label.Label(
    font,
    text="    ",
    scale= 2)
lose_text_tip = bitmap_label.Label(
    font,
    text="    ",
    scale= 1)
print("Lose Screen")
t = mark("    Text Label Creation", t)
lose_text.anchor_point = (0.5,0.5)
lose_text.anchored_position = (80,52)
lose_text_score.anchor_point = (0.5,0.5)
lose_text_score.anchored_position = (80,74)
lose_text_high_score.anchor_point = (0.5,0.5)
lose_text_high_score.anchored_position = (80,90)
lose_text_tip.anchor_point = (0.5,0.5)
lose_text_tip.anchored_position = (80,110)
lose_group = displayio.Group()
lose_group.append(lose_text)
lose_group.append(lose_text_score)
lose_group.append(lose_text_high_score)
lose_group.append(lose_text_tip)
lose_group.hidden = True
loseword_list = ["YOU LOSE","OUCH"]
def show_lose_screen():
    lose_text.text = random.choice(loseword_list)
    lose_text_score.text =f"Score:{score}"
    lose_text_tip.text = "Press A to play again"
    if score > high_score:
        lose_text_high_score.text="!!NEW HIGH SCORE!!"
    lose_group.hidden = False
t = mark("    Label Positioning and Grouping", t)

gc.collect()
t = mark("Garbage Collection", t)


print("Settings")
setting_text = bitmap_label.Label(
    font,
    text="Settings",
    scale= 3)
setting_current_text = bitmap_label.Label(
    font,
    text="Background",
    scale= 3)
setting_current_option_text = bitmap_label.Label(
    font,
    text="Day",
    scale= 3,)
setting_next_option_text = bitmap_label.Label(
    font,
    text="Basic",
    scale= 2)
setting_last_option_text = bitmap_label.Label(
    font,
    text="Night",
    scale= 2)
t = mark("    Text Label Creation", t)
setting_text.anchor_point = (0.5,0.5)
setting_text.anchored_position = (80,10)
setting_current_text.anchor_point = (0.5,0.5)
setting_current_text.anchored_position = (80,30)
setting_current_option_text.anchor_point = (0.5,0.5)
setting_current_option_text.anchored_position = (80,85)
setting_next_option_text.anchor_point = (0.5,0.5)
setting_next_option_text.anchored_position = (80,100)
setting_last_option_text.anchor_point = (0.5,0.5)
setting_last_option_text.anchored_position = (80,60)
setting_group = displayio.Group()
setting_group.append(setting_text)
setting_group.append(setting_current_text)
setting_group.append(setting_current_option_text)
setting_group.append(setting_next_option_text)
setting_group.append(setting_last_option_text)
t = mark("    Label Positioning and Grouping", t)

gc.collect()
t = mark("Garbage Collection", t)

#--------tilegrids for Game, Apples, Head--------
game_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader= palette,
    width=20,
    height=14,
    tile_width=1,
    tile_height=1,
    default_tile=0,
    #x = tile_size//2//8,
    y = 2,
    )
shadow_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader= palette,
    width=20,
    height=14,
    tile_width=1,
    tile_height=1,
    default_tile=9,
    x =0,
    y = 2)
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
t = mark("Creating tilegrids", t)

#--------Snake, Body, and Apple Logic--------
segment = []
apples = None
head_x = None
head_y = None
apple_xy = None
snakecolor = 7
snakecolor_next = 8
snakecolor_last = 6
snakecolor_list = ["Red","Orange","Yellow","Pure Green","Green","Pure Blue","Blue","Blinka Purple","Pink","White","Black"]
def snake(operation,x=None,y=None):
    if operation == "new":
        segment.insert(0,(head_x,head_y))
        game_tilegrid[head_x, head_y] = 64
        shadow_tilegrid[head_x, head_y] = 192
    if operation == "tail":
        oldx,oldy = segment.pop()
        game_tilegrid[oldx,oldy] = 0
        shadow_tilegrid[oldx, oldy] = 0
    if operation == "update":
        segment.insert(0,(head_x,head_y))
        oldx,oldy = segment.pop()
        game_tilegrid[oldx,oldy] = 0
        shadow_tilegrid[oldx, oldy] = 0
        game_tilegrid[head_x, head_y] = 64
        shadow_tilegrid[head_x, head_y] = 192
    if operation == "seg_xy":
        segment.insert(0,(x,y))
        game_tilegrid[x,y] = 64
        shadow_tilegrid[x,y] = 192
def snake_color():
        if snakecolor == 0:
            palette[1] = 0xFF0000#Red
        elif snakecolor == 1:
            palette[1] = 0xFF8000#Orange
        elif snakecolor == 2:
            palette[1] = 0xFFFF00#Yellow
        elif snakecolor == 3:
            palette[1] = 0x00FF00#Pure Green
        elif snakecolor == 4:
            palette[1] = 0x009000#Green
        elif snakecolor == 5:
            palette[1] = 0x0000FF#Pure Blue
        elif snakecolor == 6:
            palette[1] = 0x4169E1#Blue
        elif snakecolor == 7:
            palette[1] = 0x652F8F#Blinka Purple
        elif snakecolor == 8:
            palette[1] = 0xFF00FF#Pink
        elif snakecolor == 9:
            palette[1] = 0xFFFFFF#White
        elif snakecolor == 10:
            palette[1] = 0x000000#Black
def apple(operation,x=None,y=None):
    global apple_xy, apples
    if operation == "new":
        apples = rand.xy()
        apple_tilegrid[apples[0], apples[1]] = apple_color
        apple_xy = apples
    if operation == "remove":
        apple_tilegrid[apples[0], apples[1]] = 0
        apples = None
    if operation == "update":
        if apples:
            apple_tilegrid[apples[0], apples[1]] = 0
        apples = None
        apples = rand.xy()
        apple_tilegrid[apples[0], apples[1]] = apple_color
        apple_xy = apples
    if operation == "seg_xy":
        apples = rand.xy()
        apple_tilegrid[x, y] = apple_color
        apple_xy = apples
    print("apple is located at",apple_xy)

new = "new" #add new segment at head location
tail = "tail" #removes tail
update = "update"#adds new segment at head and removes segment at tail
seg_xy = "seg_xy"#add segment at defined coordinates
remove = "remove"#removes apple
t = mark("Snake, Body, and Apple Logic", t)
gc.collect()
t = mark("Garbage Collection", t)
#-------Put the tilegrids, Text Labels, and Sub-Groups into root_group-------
#---Game Group---


#game_group = displayio.Group()
#game_group.append(apple_tilegrid)

shadow_group = displayio.Group(x=5,y=6,scale=8)
shadow_group.append(shadow_tilegrid)
snake_shadow_status = True
snake_group = displayio.Group(x=4,y=4,scale=8)
snake_group.append(game_tilegrid)

#game_group.append(shadow_group)
#game_group.append(snake_group)
#game_group.append(head_tilegrid)

gc.collect()
t = mark("Garbage Collection", t)



#---background Group---
#foreground_group = displayio.Group()
#foreground_group.append(foreground)


#---Root Group---
root_group.append(background)


#root_group.append(game_group)
root_group.append(apple_tilegrid)
root_group.append(shadow_group)
root_group.append(snake_group)
root_group.append(head_tilegrid)
snake_head_status = True

root_group.append(foreground)



root_group.append(lose_group)
root_group.append(score_group)

display.root_group = root_group

t = mark("Grouping", t)

gc.collect()
t = mark("Garbage Collection", t)

#-------Initializing Input Detection-------
if True:
    #---Snake directions---
    direction_up = False
    direction_down = False
    direction_left = True
    direction_right = False
    #---Button held---
    left_held = False
    right_held = False
    up_held = False
    down_held = False
    select_held = False

    start_pressed = False
    start_sequence = False
    input_cooldown = False

#-------Initializing Game Variables-------
if True:
    #---snake---
    head_x = 10
    head_y = 6
    old_head_x = 10
    old_head_y = 6
    for x in range(head_x-2,head_x+1):
        snake(seg_xy,x,head_y)
    pre_game = True
    #---speed---
    speed_level =5
    menu_speed = 0.3
    game_speed =  0.65 * (speed_level ** -0.77)
        #speed_level = game_speed
        #         1  = 0.65
        #         2  = 0.381171
        #         3  = 0.278952
        #         4  = 0.223525
        #         5  = 0.188238
        #         6  = 0.163582
        #         7  = 0.145274
        #         8  = 0.131079
        #         9  = 0.119714
        #         10 = 0.110386
t = mark("Game Variables", t)
current_setting = ["Background","Snake Color","Snake Shadow","Snake Head"]
setting_index=0
setting_changed = False
lose = False
is_flashing = True
backlight.value = True
last_time = time.monotonic()
print(gc.mem_free())
select_pressed = False
while pre_game:
    buttons = keys.events.get()
    if buttons:
        if not input_cooldown :
            if select_pressed:
                if button.left and buttons.pressed:
                    left_held = buttons.pressed
                    input_cooldown = True
                if button.right and buttons.pressed:
                    right_held = buttons.pressed
                    input_cooldown = True
                if button.up and buttons.pressed:
                    up_held = buttons.pressed
                    input_cooldown = True
                if button.down and buttons.pressed:
                    down_held = buttons.pressed
                    input_cooldown = True
            elif button.select:
                select_pressed = True
                root_group.append(setting_group)
                gc.collect()
        if button.start:
            start_pressed = True
            pre_game = False
            setting_group.hidden = True
            score_group.hidden = False
            high_score_text.text = str(high_score)
            score_text.text = str(score)
            gc.collect()
    if select_pressed:
        current_time = time.monotonic()
        if current_time - last_time > menu_speed:
            last_time = time.monotonic()
            #menu loop
            #-----Check if Switch to Next Setting-----
            if right_held or left_held:
                if right_held:
                    setting_index = (setting_index +1) % len(current_setting)
                if left_held:
                    setting_index = (setting_index -1) % len(current_setting)
                setting_current_text.text = current_setting[setting_index]
                setting_changed = True
            #-----Background-----
            if current_setting[setting_index] == "Background":
                if setting_changed:
                    setting_changed = False
                    setting_current_option_text.text = backgrounds_list[background_index]
                    setting_next_option_text.text = backgrounds_list[next_background_index]
                    setting_last_option_text.text = backgrounds_list[last_background_index]
                    gc.collect()
                if up_held or down_held:
                    if up_held:
                        background_index = (background_index -1) % len(backgrounds_list)
                    if down_held:
                        background_index = (background_index +1) % len(backgrounds_list)
                    next_background_index = (background_index +1) % len(backgrounds_list)
                    last_background_index = (background_index -1) % len(backgrounds_list)
                    setting_current_option_text.text = backgrounds_list[background_index]
                    setting_next_option_text.text = backgrounds_list[next_background_index]
                    setting_last_option_text.text = backgrounds_list[last_background_index]
                    background_color(backgrounds_list[background_index])
                    gc.collect()

            #-----Snake Color-----
            if current_setting[setting_index] == "Snake Color":
                if setting_changed:
                    setting_changed = False
                    setting_current_option_text.text = snakecolor_list[snakecolor]
                    setting_next_option_text.text = snakecolor_list[snakecolor_next]
                    setting_last_option_text.text = snakecolor_list[snakecolor_last]
                    gc.collect()
                if up_held or down_held:
                    if up_held:
                        snakecolor = (snakecolor -1) % len(snakecolor_list)
                    if down_held:
                        snakecolor = (snakecolor +1) % len(snakecolor_list)
                    snakecolor_next = (snakecolor +1) % len(snakecolor_list)
                    snakecolor_last = (snakecolor -1) % len(snakecolor_list)
                    setting_current_option_text.text = snakecolor_list[snakecolor]
                    setting_next_option_text.text = snakecolor_list[snakecolor_next]
                    setting_last_option_text.text = snakecolor_list[snakecolor_last]
                    snake_color()
                    gc.collect()
            if current_setting[setting_index] == "Snake Shadow":
                if setting_changed:
                    setting_changed = False
                    setting_current_option_text.text = str(snake_shadow_status)
                    setting_next_option_text.text = "   "
                    setting_last_option_text.text = "   "
                    gc.collect()
                if up_held or down_held:
                    if up_held:
                        snake_shadow_status = True
                        shadow_group.hidden = False
                    if down_held:
                        snake_shadow_status = False
                        shadow_group.hidden = True
                    setting_current_option_text.text = str(snake_shadow_status)
                    gc.collect()
            if current_setting[setting_index] == "Snake Head":
                if setting_changed:
                    setting_changed = False
                    setting_current_option_text.text = str(snake_head_status)
                    setting_next_option_text.text = "   "
                    setting_last_option_text.text = "   "
                    gc.collect()
                if up_held or down_held:
                    if up_held:
                        snake_head_status = True
                        head_tilegrid.hidden = False
                    if down_held:
                        snake_head_status = False
                        head_tilegrid.hidden = True
                    setting_current_option_text.text = str(snake_head_status)
                    gc.collect()
            input_cooldown= False
            left_held = False
            right_held = False
            up_held = False
            down_held = False


apple_snake = False
while start_pressed and lose == False:
    buttons = keys.events.get()
    if buttons:
        if button.left:   left_held = buttons.pressed
        if button.right:  right_held = buttons.pressed
        if button.up:     up_held = buttons.pressed
        if button.down:   down_held = buttons.pressed
        if button.start:  start_pressed = True
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

    if start_sequence!= True:
        #sets all snake directions to false except for left
        start_sequence = True
        direction_up = False
        direction_down = False
        direction_right = True
        direction_left =False
        apple(new)
        gc.collect()

    current_time = time.monotonic()
    if current_time - last_time > game_speed:
        last_time = time.monotonic()
        #game loop
        old_head_x = head_x
        old_head_y = head_y
        input_cooldown= False
        if direction_left:  head_x -= 1
        if direction_right: head_x += 1
        if direction_up:    head_y -= 1
        if direction_down:  head_y += 1
        if len(segment) == len(set(segment)):
            if head_x in range(0,19) and head_y in range(0,13):
                snake(new)
                if direction_left:
                    head_tilegrid[head_x,head_y] =2
                if direction_right:
                    head_tilegrid[head_x,head_y] =3
                if direction_up:
                    head_tilegrid[head_x,head_y] =0
                if direction_down:
                    head_tilegrid[head_x,head_y] =1
                head_tilegrid[old_head_x,old_head_y] =4

                if apple_xy in segment:
                    apple(update)
                    apple_snake = False
                    score += 1
                    score_text.text = str(score)
                    play(400,0.00001)
                    gc.collect()

                else:
                    snake(tail)
                    gc.collect()
            else:
                lose = True
        else:
            lose = True
if lose:
    show_lose_screen()
    if score > high_score:
        print("New High Score!")
        high_score = score
        save_high_score(high_score)
    while True:
        buttons = keys.events.get()
        if buttons:
            print(True)
            if button.a :
                time.sleep(0.1)
                gc.collect()
                supervisor.reload()
        current_time = time.monotonic()
        if current_time - last_time > 0.5:
            last_time = time.monotonic()
            lose_text_high_score.hidden = not lose_text_high_score.hidden


