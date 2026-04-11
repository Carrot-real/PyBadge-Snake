import time
import board
import digitalio
import storage
import keypad

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

keys=keypad.ShiftRegisterKeys(
    clock= board.BUTTON_CLOCK,
    data=  board.BUTTON_OUT,
    latch= board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
    interval=0.01,)

led.value = True
time.sleep(0.05)
led.value = False
time.sleep(1)
buttons = keys.events.get()
led.value = True
time.sleep(0.05)
led.value = False

if buttons:
    print("wwwwwwwwiewifjfj")
print(True)
if buttons:
    print("ryutryuyyureu")
    if buttons.key_number==3 and buttons.pressed:
        press = True
        print(True)

# D11 is pad #5, GND is pad #4 on the right-side row (looking at the back)
switch = digitalio.DigitalInOut(board.D11)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# BRIDGE PADS 4 & 5: The PyBadge takes control (PC is Read-Only)
# LEAVE THEM ALONE: Your PC takes control (Board is Read-Only)
storage.remount("/", readonly=press)
