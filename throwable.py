import pygame as pg
import utils


class ThrowableObjA():
    def __init__(self,pos,display,img,name):
        self.pos = pos
        self.display = display
        self.img = img
        self.name = name
        self.terminate = False

        self.size = pg.Vector2(self.img.get_size()[0], self.img.get_size()[1])

    def draw(self):
        self.display.blit(self.img, self.pos - self.size/2)


    def fall(self):
        if self.pos.y < 720 - self.size.y/2:
            self.pos.y += utils.G * utils.DELTA * .5
        
    def get_picked_up(self,p1,p2):
        if abs(self.pos.x - p1.pos.x) < (self.size.x + p1.size.x)/2 and abs(self.pos.y - p1.pos.y) < (self.size.y + p1.size.y)/2:
            self.terminate = True
            p1.inventory.append(self.name)
        if abs(self.pos.x - p2.pos.x) < (self.size.x + p2.size.x)/2 and abs(self.pos.y - p2.pos.y) < (self.size.y + p2.size.y)/2:
            self.terminate = True
            p2.inventory.append(self.name)