import pygame as pg
import math
from random import randint as rint
import utils
import player
import platforms
import throwable
import random

class Game():
    def __init__(self):
        self.window_w, self.window_h = 1440, 720
        self.display = pg.display.set_mode((self.window_w, self.window_h))

        self.clock = pg.time.Clock()
        self.running = True

        self.spears = []
        self.markers = []

        self.player = player.Player(pg.Vector2(0,200), self.display, self.spears, 0, self.markers)
        self.player2 = player.Player(pg.Vector2(1000,200), self.display, self.spears, 1, self.markers)


        self.platforms = []

        for i in range(4):
            x,y = random.randint(0,1200), random.randint(200,400)
            w,h = random.randint(100,300), random.randint(100,300)
            p = platforms.Platform(pg.Vector2(x,y), w, h, self.display)
            self.platforms.append(p)

        self.names = ["rock", "axe", "knife", "extinguisher"]


        self.floor_items = []
        for i in range(10):
            given_name = self.names[random.randint(0, len(self.names)-1)]
            objA = throwable.ThrowableObjA(pg.Vector2(random.randint(200,1200),400), self.display, utils.load_img(given_name,scale=2), given_name)
            self.floor_items.append(objA)

        self.bg_surf = pg.Surface((2000,2000))
        self.bg_value = 2
        self.bg_black = True

        self.spawn_timer = 10


    def run(self):
        while self.running:
            self.display.fill((25,25,25))
    
            #Background shenanigans
            if self.bg_black:
                self.bg_surf.fill((25,25,25))
            else:
                self.bg_surf.fill((125,125,155))

            for y in range(0,20):
                for x in range(y%2,40,2):
                    #pg.draw.rect(self.bg_surf, (225,225,255), (x*40, y*40, 40,40))

                    points = []
                    for i in range(4):
                        points.append(pg.Vector2(x*40,y*40) + pg.Vector2(self.bg_value,0).rotate(-i/4*360 + self.bg_value/35*90))
                    if self.bg_black:
                        pg.draw.polygon(self.bg_surf, (125,125,155), points)
                    else:
                        pg.draw.polygon(self.bg_surf, (25,25,25), points)

            self.bg_value += utils.DELTA * 8
            if self.bg_value > 40:
                self.bg_value = 2
                self.bg_black = not self.bg_black

            self.display.blit(self.bg_surf, (0,0))

            #Spawn items
            self.spawn_timer -= utils.DELTA
            if self.spawn_timer <= 0 and len(self.floor_items) < 30:
                self.spawn_timer = 10
                for i in range(10):
                    given_name = self.names[random.randint(0, len(self.names)-1)]
                    objA = throwable.ThrowableObjA(pg.Vector2(random.randint(200,1200),400), self.display, utils.load_img(given_name,scale=2), given_name)
                    self.floor_items.append(objA)

            #Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    self.player.take_input(event.key, True)
                    self.player2.take_input(event.key, True)

                if event.type == pg.KEYUP:
                    self.player.take_input(event.key, False)
                    self.player2.take_input(event.key, False)
            #Players
            self.player.draw()
            self.player.draw_ui()
            self.player.move(self.platforms)
            self.player.apply_gravity()
            self.player.collide_floor()

            self.player2.draw()
            self.player2.draw_ui()
            self.player2.move(self.platforms)
            self.player2.apply_gravity()
            self.player2.collide_floor()

            #Spears
            to_remove = []
            for spear_ in self.spears:
                spear_.debug_draw()
                spear_.move()
                spear_.collide(self.platforms,self.player,self.player2)

                if spear_.timer >= 5:
                    to_remove.append(spear_)

            for spear_ in to_remove:
                self.spears.remove(spear_)

            #Platforms
            for p in self.platforms:
                p.debug_draw()

            #Objects (ground)
            to_remove = []
            for ob in self.floor_items:
                ob.draw()
                ob.fall()
                ob.get_picked_up(self.player, self.player2)

                if ob.terminate:
                    to_remove.append(ob)

            for ob in to_remove:
                self.floor_items.remove(ob)

            #Damage markers
            to_remove = []
            for m in self.markers:
                m.draw()
                
                if m.terminate:
                    to_remove.append(m)

            for m in to_remove:
                self.markers.remove(m)

               
            self.clock.tick(utils.FPS)
            pg.display.set_caption("FPS: " + str(round(self.clock.get_fps(),2)))
            pg.display.update()


game = Game()
game.run()