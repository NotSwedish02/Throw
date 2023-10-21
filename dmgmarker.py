import utils
import pygame as pg


class DamageMarker():
    def __init__(self, pos, display, amount):
        self.pos = pos
        self.display = display
        self.amount = amount
        self.timer = 2
        self.terminate = False

    def draw(self):
        txt = utils.font.render(str(-self.amount),True,(225,25,25))
        self.display.blit(txt, self.pos - pg.Vector2(txt.get_width(), txt.get_height())/2)
        self.pos.y -= utils.DELTA * 20
        self.timer -= utils.DELTA
        if self.timer <= 0:
            self.terminate = True