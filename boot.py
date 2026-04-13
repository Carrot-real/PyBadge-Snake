import board
import digitalio
import storage
import time
import neopixel

latch = digitalio.DigitalInOut(board.BUTTON_LATCH)
latch.direction = digitalio.Direction.OUTPUT
clock = digitalio.DigitalInOut(board.BUTTON_CLOCK)
clock.direction = digitalio.Direction.OUTPUT
data = digitalio.DigitalInOut(board.BUTTON_OUT)
data.direction = digitalio.Direction.INPUT
data.pull = digitalio.Pull.UP

def check_for_high_signal():
    latch.value = False
    time.sleep(0.01)
    latch.value = True
    return data.value

time.sleep(0.5)
is_pressed = check_for_high_signal()

latch.deinit()
clock.deinit()
data.deinit()

leds = neopixel.NeoPixel(board.NEOPIXEL, 5)
if is_pressed: # If we finally saw a 'True'
    storage.remount("/", readonly=False)
    leds.fill((0, 255, 0)) # Green
    print("MODE: Badge Write (Saw High Signal)")
else:
    storage.remount("/", readonly=True)
    leds.fill((255, 0, 0)) # Red
    print("MODE: Computer Write (Stuck Low)")
