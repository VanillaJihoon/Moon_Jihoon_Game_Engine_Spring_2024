# This file was created by Jihoon Moon
# Appreciatoin to Chris Bradfield
import pygame as pg
from settings import *
from utils import *
from random import choice

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
        self.material = True
        self.pos = vec(0,0)
        self.dir = vec(0,0)
        self.weapon = Sword(self.game, self.rect.x, self.rect.y, 16, 16, (0,0))
    def set_dir(self, d):
        self.dir = d
        # return (0,0)
    def get_dir(self):
        return self.dir
    def get_mouse(self):
        if pg.mouse.get_pressed()[0]:
            # mx = pg.mouse.get_pos()[0]
            # my = pg.mouse.get_pos()[1]
            if self.weapon_drawn == False:
                self.weapon_drawn = True
                if abs(pg.mouse.get_pos()[0]-self.rect.x) > abs(pg.mouse.get_pos()[1]-self.rect.y):
                    if pg.mouse.get_pos()[0]-self.rect.x > 0:
                        print("swing to pos x")
                        self.weapon = Sword(self.game, self.rect.x+TILESIZE, self.rect.y, 32, 5, (1,0))
                    if pg.mouse.get_pos()[0]-self.rect.x < 0:
                        print("swing to neg x")
                        self.weapon = Sword(self.game, self.rect.x-TILESIZE, self.rect.y, 32, 5, (-1,0))
                else:
                    if pg.mouse.get_pos()[1]-self.rect.y > 0:
                        print("swing to pos y")
                        self.weapon = Sword(self.game, self.rect.x, self.rect.y+self.rect.height, 5, 32, (0,1))
                    if pg.mouse.get_pos()[1]-self.rect.y < 0:
                        print("swing to neg y")
                        self.weapon = Sword(self.game, self.rect.x, self.rect.y-self.rect.height, 5, 32, (0,-1))

    def set_dir(self, d):
        self.dir = d
        # return (0,0)
    def get_dir(self):
        return self.dir

        

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
         
        if keys[pg.K_t]:
            # for a in self.game.mobs:
            #     a.kill()
            self.game.change_level("level3.txt")
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
            self.set_dir((-1,0))
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
            self.set_dir((1,0))
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
            self.set_dir((0,-1))
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
            self.set_dir((0,1))
        if keys[pg.K_e]:
            print("trying to shoot...")
            self.pew()
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def pew(self):
        p = HolyWater(self.game, self.rect.x, self.rect.y)
        print(p.rect.x)
        print(p.rect.y)

    def collide_with_walls(self, dir):
        if self.material: 
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
        if not self.material:
                self.game.flying.cd = 5
                self.cooling = True
                if self.game.flying.cd < 0:
                    self.cooling = False
                if not self.cooling:
                    self.material = True
                

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
                    self.material = False
            if str(hits[0].__class__.__name__) == "Mob":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                self.hitpoints -= 15
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "Mob2":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                self.hitpoints -= 30
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "Ghost":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                self.hitpoints -= 0.1
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
        self.collide_with_group(self.game.mobs2, False)


#This is the wall
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WALLCOLOR)
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
            

#This is the coin. Currently useless
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

#Powerups. 
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


#This is the first mob. It is weak.
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
        #This is the mob's health
        self.hitpoints = 5

#This is how the mob tracks the player
    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.walls, 'y')
        #This will kill the mob if it's health reaches 0...
        if self.hitpoints <= 0:
            self.kill()


#Same as mob but stronger and has more health
class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mob2_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # added
        self.speed = 100
        self.hitpoints = 15

#Same as 1st mob...
    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.walls, 'y')
        #Same as first mob... gl killing it tho
        if self.hitpoints <= 0:
            self.kill()

#This mob phases through walls
class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ghost
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.ghost_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # added
        self.speed = 100
        #Health is redundant because it cannot be hit with sword...
        self.hitpoints = 1
        #Removed the wall collision to let it phase. 

#Same as regular mob...
    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        if self.hitpoints <= 0:
            pass

#This is the sword. It kills mobs...
class Sword(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, dir):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.rect.width = w
        self.rect.height = h
        self.pos = vec(x,y)
        self.dir = dir
        print("I created a sword")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        #Hitting the mobs does what? Determines what happens when you hit x mob.
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                print("you hurt a mob!")
                hits[0].hitpoints -= 5
                self.kill()
            if str(hits[0].__class__.__name__) == "Mob2":
                print("you hurt a mob!")
                hits[0].hitpoints -= 5
                self.kill()
                #Remember ghost can only be hit with water
            if str(hits[0].__class__.__name__) == "Ghost":
                print("You hit nothing...")
        #Tracking for the sword so it spawns correctly
    def track(self, obj):
        self.vx = obj.vx
        self.vy = obj.vy
        self.rect.width = obj.rect.x+self.dir[0]*32+5
        self.rect.width = obj.rect.y*self.dir[1]*32+5
        #Check to see if sword exists or not...
    def update(self):
        if self.game.player.weapon_drawn == False:
            self.kill()
        self.track(self.game.player)
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_group(self.game.mobs, False)

#New weapon... Holy water...
class HolyWater(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.holy_water
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLEU)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        print("spray...")
        #Made it so it only kills the ghost...
    def update(self):
        self.rect.y -= self.speed
        self.collide_with_group(self.game.ghost, True)
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            pass
