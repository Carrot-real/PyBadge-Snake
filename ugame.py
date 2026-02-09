import board
import digitalio
import keypad
import displayio

# PyBadge button bitmask constants
K_UP = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_SELECT = 0x10
K_START = 0x20
K_A = 0x80
K_B = 0x40

class UGame:
    def __init__(self):
        self.display = board.DISPLAY
        
        # Initialize buttons using modern keypad module
        self._keys = keypad.ShiftRegisterKeys(
            clock=board.BUTTON_CLOCK,
            data=board.BUTTON_OUT,
            latch=board.BUTTON_LATCH,
            key_count=8,
            value_when_pressed=True,
        )
        
        # Audio safety check for 10.x firmware
        self.audio = None
        try:
            import audiopwmio
            self.audio = audiopwmio.PWMAudioOut(board.SPEAKER)
        except (ImportError, AttributeError):
            try:
                import audiobusio
                # Some boards use different audio paths
                pass 
            except ImportError:
                print("Audio module not found; running in silent mode.")

    @property
    def buttons(self):
        state = 0
        for i in range(8):
            if self._keys.pressed[i]:
                state |= (1 << i)
        return state

game = UGame()
display = game.display