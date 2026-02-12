import board
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
#initializing the display
display = board.DISPLAY

text = "test"
font = terminalio.FONT
color = 0x0000FF
#the text label
text_area = label.Label(font, text=text, color=color)

text_area.x = 20
text_area.y = 20

display.root_group = text_area

while True:
    pass

