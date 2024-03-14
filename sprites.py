# This file was created by Jihoon Moon
# Appreciatoin to Chris Bradfield
import pygame as pg
from settings import *
from utils import *
from random import choice

MOBHEALTH = 1
MOBHEALTH2 = 2
vec =pg.math.Vector2

# write a player class
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.player_img
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 300
        self.moneybag = 0
        self.status = ""
        self.cooling = False
        self.hitpoints = 100
        self.weapon_drawn = False
        self.pos = vec(0,0)
        self.dir = vec(0,0)
    def set_dir(self, d):
        self.dir = d
        # return (0,0)
    def get_dir(self):
        return self.dir
    def get_mouse(self):
        if pg.mouse.get_pressed()[0]:
            print("left click")
        if pg.mouse.get_pressed()[1]:
            print("middle click")
        if pg.mouse.get_pressed()[2]:
            print("right click")
        self.weapon_drawn = False
        


    def get_keys(self):
        self.vx, self.vy = 0, 0 
        keys = pg.key.get_pressed()
        if keys[pg.K_t]:
            self.game.test_method()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_e]:
            if not self.weapon_drawn:
                Sword(self.game, self.rect.x + self.dir[0]*32, self.rect.y + self.dir[1]*32, abs(32*self.dir[0])+5, abs(32*self.dir[1])+5)
                self.weapon_drawn = True
    def draw_weapon(self):
        if self.weapon_drawn:
            Sword(self.game, self.rect.x, self.rect.y)
        

            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    


    # old motion
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                #self.game.collect_sound.play()
                effect = choice(POWER_UP_EFFECTS)
                self.game.cooldown.cd = 5
                self.cooling = True
                print(effect)
                print(self.cooling)
                if effect == "Invincible":
                    self.status = "Invincible"
                if effect == "I can fly":
                    self.speed += 500
                    
            if str(hits[0].__class__.__name__) == "Mob":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                # self.hitpoints -= 1
                if self.status == "Invincible":
                    print("you can't hurt me")
                
    # UPDATE THE UPDATE
    def update(self):
        self.get_keys()
        # self.power_up_cd.ticking()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        if self.game.cooldown.cd < 1:
            self.cooling = False
        if not self.cooling:
            self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLEU)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
    def update(self):
        # self.rect.x += 1
        self.rect.x += TILESIZE * self.speed
        # self.rect.y += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
        # if self.rect.y > HEIGHT or self.rect.y < 0:
        #     self.speed *= -1
            


class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mob_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # added
        self.speed = 150
        self.health = MOBHEALTH

    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.walls, 'y')
        if self.health <= 0:
             self.kill()

class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mob_img2
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE * 1.5
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # added
        self.speed = 100
        self.health = MOBHEALTH2
        if self.health <= 0:
            self.kill()

    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.walls, 'y')

class Sword(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.rect.w = w
        self.rect.h = h
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        print("I created a sword")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                
                self.kill()
            if str(hits[0].__class__.__name__) == "Mob2"

                self.kill()
    def update(self):
        # self.collide_with_group(self.game.coins, True)
        # if self.game.player.dir
        self.rect.x = self.game.player.rect.x + self.game.player.dir[0]*32
        self.rect.y = self.game.player.rect.y + self.game.player.dir[1]*32
        self.rect.width = abs(self.game.player.get_dir()[0]*32)+5
        self.rect.width = abs(self.game.player.get_dir()[1]*32)+5
        self.image.get_rect()
        self.collide_with_group(self.game.mobs, True)
        if not self.game.player.weapon_drawn:
            print("killed the sword")
            self.kill()