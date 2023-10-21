import math
import pygame as pg
import utils
import random

class Spear(): 
    def __init__(self,pos,velocity, display):
        self.pos = pos
        self.velocity = velocity
        self.display = display

        self.color = (255,255,255)
        self.timer = 0

        self.angle = 0

        self.size = pg.Vector2(0,0)

    def debug_draw(self):
        if self.velocity.length() != 0:
            self.angle = math.atan2(self.velocity.y, self.velocity.x)

        #pg.draw.aaline(self.display, self.color, self.pos, self.pos - pg.Vector2(1,0).rotate(self.angle/math.pi*180) * 40, 2)
        utils.draw_arrow(self.pos - pg.Vector2(1,0).rotate(self.angle/math.pi*180) * 40, self.pos, self.display)
    
    def collide(self, p_list, p1, p2):
        for p in p_list:
            differencex = self.pos.x - (p.pos.x + p.size.x/2)
            differencey = self.pos.y - (p.pos.y + p.size.y/2)

            if abs(differencex) < p.size.x/2 + self.size.x/2 and abs(differencey) < p.size.y/2 + self.size.y/2:
                self.timer = 5
                
        if abs(self.pos.x - p1.pos.x) < self.size.x/2 and abs(self.pos.y - p1.pos.y) < self.size.y/2:
            p1.take_dmg(random.randint(8,15))
            self.timer = 5
        if abs(self.pos.x - p2.pos.x) < self.size.x/2 and abs(self.pos.y - p2.pos.y) < self.size.y/2:
            p2.take_dmg(random.randint(8,15))
            self.timer = 5


    def move(self):
        self.pos += self.velocity * utils.DELTA
        self.velocity.y += utils.G * utils.DELTA

        if self.pos.y >= 730 - self.size.y/2:
            self.velocity *= 0
            self.timer += utils.DELTA

class Projectile(Spear):
    def __init__(self, pos, velocity, display, img):
        super().__init__(pos, velocity, display) 
        self.img = img
        self.angle = random.randint(0,360)
        self.angular_vel = random.randint(-15,15) * 10

        self.size = pg.Vector2(self.img.get_size()[0], self.img.get_size()[1])


    def debug_draw(self):

        if self.velocity.length() != 0:
            self.angle += self.angular_vel * utils.DELTA

        img = pg.transform.rotate(self.img, self.angle).convert_alpha()
        self.display.blit(img, self.pos - self.size/2)
    
