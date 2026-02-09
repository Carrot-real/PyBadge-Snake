import _stage
import displayio
try:
    import terminalio
except ImportError:
    pass

class Bank:
    def __init__(self, bitmap, palette):
        self.bitmap = bitmap
        self.palette = palette

    @classmethod
    def from_bmp16(cls, filename):
        with open(filename, "rb") as f:
            bitmap = displayio.OnDiskBitmap(f)
            # CircuitPython 10 compatibility
            palette = bitmap.pixel_shader
            return cls(bitmap, palette)

class Layer:
    def __init__(self, width, height, bank):
        self.width = width
        self.height = height
        self.bank = bank
        self.x = 0
        self.y = 0

    def move(self, x, y):
        self.x = x
        self.y = y

class Grid(Layer):
    def __init__(self, bank, width, height):
        super().__init__(width, height, bank)
        self._grid = _stage.Layer(width, height, bank.bitmap, bank.palette)

    def tile(self, x, y, tile=None):
        if tile is None:
            return self._grid.tile(x, y)
        self._grid.tile(x, y, tile)

class Sprite(Layer):
    def __init__(self, bank, frame, x, y):
        super().__init__(1, 1, bank)
        self._sprite = _stage.Layer(1, 1, bank.bitmap, bank.palette)
        self._sprite.tile(0, 0, frame)
        self.move(x, y)

    def set_frame(self, frame):
        self._sprite.tile(0, 0, frame)

class Stage:
    def __init__(self, display, fps=12):
        self.display = display
        self.fps = fps
        self.layers = []

    def render_block(self):
        # Passes the heavy lifting to the C-module _stage
        _stage.render(0, 0, self.display.width, self.display.height, 
                      [l._grid if hasattr(l, '_grid') else l._sprite for l in self.layers], 
                      self.display)

    def render_sprites(self, sprites):
        # High-speed dirty rectangle rendering
        _stage.render(0, 0, self.display.width, self.display.height, 
                      [l._grid if hasattr(l, '_grid') else l._sprite for l in self.layers], 
                      self.display)
