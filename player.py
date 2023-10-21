import pygame as pg
import math,numpy,random
import utils, spear, dmgmarker



class Player():
    def __init__(self, pos, display, spears, id, markers):
        self.pos = pos
        self.display = display
        self.spears = spears

        self.id = id

        if self.id == 0:
            self.img = utils.load_img("frog1",scale=2)
        if self.id == 1:
            self.img = utils.load_img("frog2",scale=2)

        self.size = pg.Vector2(self.img.get_width(),self.img.get_height())

        self.flip_h = False

        self.a_d_dict = {
            "a": 0,
            "d": 0,
            "q": 0
        }
        self.jump_force = 500
        self.speed = 950

        self.velocity = pg.Vector2(0,0)
        self.force = pg.Vector2(0,0)


        self.hp = 100

        self.shooting_angle = -20

        self.inventory = []

        self.name_img = {
            "rock": utils.load_img("rock", scale=2),
            "axe": utils.load_img("axe", scale=2),
            "knife": utils.load_img("knife", scale=2),
            "extinguisher": utils.load_img("extinguisher", scale=2)
        }

        self.name_img_ui = {
            "rock": utils.load_img("rock", scale=2),
            "axe": utils.load_img("axe", scale=1.5),
            "knife": utils.load_img("knife", scale=1.5),
            "extinguisher": utils.load_img("extinguisher", scale=1.5)
        }
        
        self.markerlist = markers

        self.jumps = 0

        self.aiming = False

    def debug_draw(self):
        pg.draw.rect(self.display, (255,0,0), (self.pos - self.size/2, self.size))

    def draw(self):

        img = pg.transform.flip(self.img, self.flip_h, False).convert_alpha()

        self.display.blit(img, self.pos - self.size/2)

    def draw_ui(self):
        pg.draw.rect(self.display, (255,0,0), (self.pos + pg.Vector2(-25,-30), (self.hp/2,12)))

        idx = 0
        if self.id == 0:
            origin = pg.Vector2(20,20)
        if self.id == 1:
            origin = pg.Vector2(800,20)

        for ob in self.inventory:
            ob_img = self.name_img_ui[ob]

            self.display.blit(ob_img, origin + pg.Vector2(16,16) + pg.Vector2(idx*40,0) - pg.Vector2(ob_img.get_width(), ob_img.get_height())/2)

            pg.draw.rect(self.display, (255,255,255), (origin + pg.Vector2(idx*40,0) - pg.Vector2(4,4), pg.Vector2(40,40)),3)
            idx += 1

        if self.aiming:
            for i in range(20):
                virtual_projectile = pg.Vector2(self.pos)
                virtual_vel = pg.Vector2(1,0).rotate(self.shooting_angle - (i/2+5)) * 800
                virtual_vel.x *= numpy.sign(self.velocity.x)

                for i in range(135):
                    virtual_projectile += virtual_vel * utils.DELTA * 2.5
                    pg.draw.circle(self.display, (255,0,0), virtual_projectile, 2)
                    virtual_vel.y += utils.G * utils.DELTA * 2.5


    def move(self, p_list):
        if self.a_d_dict["a"]:
            self.force.x = -1
            self.flip_h = True
        if self.a_d_dict["d"]:
            self.force.x = 1
            self.flip_h = False
        self.aiming = self.a_d_dict["q"]


        self.velocity += self.force * self.speed * utils.DELTA
        #self.pos += self.velocity * utils.DELTA
        self.collide_platforms(p_list, self.velocity.x * utils.DELTA, self.velocity.y * utils.DELTA)


        self.velocity.x -= self.velocity.x * .99 * utils.DELTA * 5
           
        self.force *= 0
                    


    def apply_gravity(self):
        self.velocity.y += utils.G * utils.DELTA

    def collide_floor(self):
        if self.pos.y > 720 - self.size.y/2:
            self.pos.y = 720 - self.size.y/2
            if self.velocity.y > 0:
                self.velocity.y = 0
                self.on_floor = True
                self.jumps = 2

    def collide_platforms(self, p_list, dx, dy):

        self.on_floor = False
        self.pos.x += dx
        for p in p_list:
            differencex = self.pos.x - (p.pos.x + p.size.x/2)
            differencey = self.pos.y - (p.pos.y + p.size.y/2)

            if abs(differencex) < p.size.x/2 + self.size.x/2 and abs(differencey) < p.size.y/2 + self.size.y/2:
                self.pos.x = (p.pos.x + p.size.x/2) + (p.size.x/2 + self.size.x/2) * numpy.sign(differencex)
                if differencex > 0 and self.velocity.x < 0:
                    self.velocity.x = 0
                    self.jumps = 1

                elif differencex < 0 and self.velocity.x > 0:
                    self.velocity.x = 0
                    self.jumps = 1
        
        self.pos.y += dy
        for p in p_list:
            differencex = self.pos.x - (p.pos.x + p.size.x/2)
            differencey = self.pos.y - (p.pos.y + p.size.y/2)

            if abs(differencex) < p.size.x/2 + self.size.x/2 and abs(differencey) < p.size.y/2 + self.size.y/2:
                self.pos.y = (p.pos.y+ p.size.y/2) + (p.size.y/2 + self.size.y/2) * numpy.sign(differencey)
                if differencey > 0 and self.velocity.y < 0:
                    self.velocity.y = 0
                elif differencey < 0 and self.velocity.y > 0:
                    self.velocity.y = 0
                    self.on_floor = True
                    self.jumps = 2
        

    def take_dmg(self,amount):
        self.hp -= amount

        dmarker = dmgmarker.DamageMarker(self.pos.copy() - pg.Vector2(0,50), self.display, amount)
        self.markerlist.append(dmarker)

    def take_input(self,key,is_pressed):
        if self.id == 0:
            if key == pg.K_a:
                self.a_d_dict["a"] = is_pressed
            if key == pg.K_d:
                self.a_d_dict["d"] = is_pressed
            if key == pg.K_q:
                self.a_d_dict["q"] = is_pressed

            if key == pg.K_w and is_pressed and self.jumps > 0:
                self.velocity.y -= self.jump_force
                self.jumps -= 1

            if key == pg.K_s and is_pressed:
                if len(self.inventory) != 0:
                    ob_img = self.name_img[self.inventory[0]]
                    spear_ = spear.Projectile(self.pos.copy() + pg.Vector2(0,-30), pg.Vector2(1,0).rotate(self.shooting_angle + random.randint(-5,5)) * 800, self.display, ob_img)
                    spear_.velocity.x *= numpy.sign(self.velocity.x)
                    self.spears.append(spear_)

                    self.inventory.remove(self.inventory[0])

        if self.id == 1:
            if key == pg.K_LEFT:
                self.a_d_dict["a"] = is_pressed
            if key == pg.K_RIGHT:
                self.a_d_dict["d"] = is_pressed
            if key == pg.K_p:
                self.a_d_dict["q"] = is_pressed

            if key == pg.K_UP and is_pressed and self.jumps > 0:
                self.velocity.y -= self.jump_force
                self.jumps -= 1

            if key == pg.K_DOWN and is_pressed:
                if len(self.inventory) != 0:
                    ob_img = self.name_img[self.inventory[0]]
                    spear_ = spear.Projectile(self.pos.copy() + pg.Vector2(0,-30), pg.Vector2(1,0).rotate(self.shooting_angle + random.randint(-5,5)) * 800, self.display, ob_img)
                    spear_.velocity.x *= numpy.sign(self.velocity.x)
                    self.spears.append(spear_)

                    self.inventory.remove(self.inventory[0])