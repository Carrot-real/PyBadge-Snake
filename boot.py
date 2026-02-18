import board
import digitalio
import storage

# D11 is pad #5, GND is pad #4 on the right-side row (looking at the back)
switch = digitalio.DigitalInOut(board.D11)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# BRIDGE PADS 4 & 5: The PyBadge takes control (PC is Read-Only)
# LEAVE THEM ALONE: Your PC takes control (Board is Read-Only)
storage.remount("/", readonly=switch.value)
