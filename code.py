import ugame
import stage 
from button import button

bank = stage.Bank.from_bmp16("ball.bmp")
background = stage.Grid(bank, 10, 8)
ball = stage.Sprite(bank, 1, 8, 8)
game = stage.Stage(ugame.display, 12)
game.layers = [ball, background]
game.render_block()

#
dx = 2
while True:
    ball.update()
    if button.right:
        ball.move(ball.x + dx, ball.y)
        if not ball.x <= 144:
            ball.x -= 2
    elif button.left:
        ball.move(ball.x - dx, ball.y)
        if not ball.x >= 0:
            ball.x += 2
    ball.move(ball.x, ball.y)
    game.render_sprites([ball])
    game.tick()
