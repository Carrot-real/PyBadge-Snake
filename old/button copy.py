# button.py
import ugame

class ButtonHandler:
    @property
    def up(self):
        # Checks bitmask and returns True/False
        return bool(ugame.buttons.get_pressed() & ugame.K_UP)

    @property
    def down(self):
        return bool(ugame.buttons.get_pressed() & ugame.K_DOWN)

    @property
    def left(self):
        return bool(ugame.buttons.get_pressed() & ugame.K_LEFT)

    @property
    def right(self):
        return bool(ugame.buttons.get_pressed() & ugame.K_RIGHT)

    @property
    def select(self):
        return bool(ugame.buttons.get_pressed() & ugame.K_SELECT)

    @property
    def start(self):
        return bool(ugame.buttons.get_pressed() & ugame.K_START)

    @property
    def a(self):
        return bool(ugame.buttons.get_pressed() & ugame.K_X)

    @property
    def b(self):
        return bool(ugame.buttons.get_pressed() & ugame.K_O)

# Create the object right here in the library
button = ButtonHandler()
