import pygame as pg

FPS = 80
DELTA = 1/FPS
G = 98 * 15

pg.init()
pg.font.init()
font = pg.font.SysFont("TimesNewRoman",24)

def load_img(img,scale,colorkey=(0,0,0)):
    img = pg.image.load("images/" + img + ".png")
    img = pg.transform.scale(img, (img.get_width()*scale,img.get_height()*scale))
    img.set_colorkey(colorkey)

    return img.convert_alpha()

def draw_arrow(start, end_, display):
    pg.draw.aaline(display, (255,255,255), start, end_, 3)    
    pg.draw.aaline(display, (255,255,255), end_, end_ + (end_ - start).rotate(140) * .25, 3)
    pg.draw.aaline(display, (255,255,255), end_, end_ + (end_ - start).rotate(-140) * .25, 3)