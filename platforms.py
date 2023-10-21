import pygame as pg


class Platform():
    def __init__(self,pos,w,h,display):
        self.pos = pos
        self.size = pg.Vector2(w,h)
        self.display = display

    def debug_draw(self):
        pg.draw.rect(self.display, (25,25,25), (self.pos, self.size))
        pg.draw.rect(self.display, (255,0,0), (self.pos, self.size), 3)