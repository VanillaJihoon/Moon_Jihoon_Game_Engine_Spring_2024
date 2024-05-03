# This file was created by Jihoon Moon
# Appreciatoin to Chris Bradfield
import pygame as pg
from settings import *
from utils import *
from random import choice
from os import path
from random import randint
import time


vec = pg.math.Vector2
SPRITESHEET = "spiderplayer.png"
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

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

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        #self.image.fill(GREEN)
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 300
        self.moneybag = 0
        self.status = ""
        self.cooling = False
        self.hitpoints = 100
        self.last_shot_time = 0
        self.last_molt_time = 0
        self.bigtime = 2
        self.weapon_drawn = False
        self.small = True
        self.pos = vec(0,0)
        self.dir = vec(0,0)
        self.map_pos = (self.x+280, self.y-1000)
        self.mapx, self.mapy = self.map_pos
        # needed for animated sprite
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False
    def set_dir(self, d):
        self.dir = d
        # return (0,0)
    def get_dir(self):
        return self.dir

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
            current_time = pg.time.get_ticks()
            if current_time - self.last_shot_time >= 5000:  # 5000 milliseconds = 5 seconds
                print("trying to shoot...")
                self.pew()
                self.last_shot_time = current_time  # Update the time of the last shot
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071      
        if keys[pg.K_r]:
            current_time = pg.time.get_ticks()
            if current_time - self.last_molt_time >= 20000:
                print("trying to molt")
                self.molt()
                self.last_molt_time = current_time

    def pew(self):
        p = PewPew(self.game, self.rect.x, self.rect.y)
        print(p.rect.x)
        print(p.rect.y)
    
    def molt(self):
        m = Molt(self.game, self.rect.x, self.rect.y)
        print(m.rect.x)
        print(m.rect.y)

    def collide_with_walls(self, dir):
        if self.small: 
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
                if effect == "I can fly":
                    self.speed += 500
                    self.small = False
                    self.hitpoints * 10


            if str(hits[0].__class__.__name__) == "Mob":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                #self.hitpoints -= 15
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "Mob2":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                #self.hitpoints -= 30
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "Ghost":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                self.hitpoints -= 0.1
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "Molt":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                self.hitpoints += 5
                self.speed = 0
                print(self.hitpoints)

    # needed for animated sprite
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    # UPDATE THE UPDATE
    def update(self):
        self.get_keys()
        # needed for animated sprite
        self.animate()
        self.get_keys()
        # self.power_up_cd.ticking()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.mapx += -self.vx * self.game.dt
        self.mapy += -self.vy * self.game.dt
        self.map_pos = self.mapx, self.mapy
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
        self.acc = vec(self.speed, 0).rotate(+self.rot)
        #adapted from ChatGPT - 3.5
        self.acc.x *= -1
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
        self.acc = vec(self.speed, 0).rotate(+self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        if self.hitpoints <= 0:
            pass



#New weapon... Holy water...
class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y, lifespan=150, movement=25):  # Lifespan is in frames
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE*1, TILESIZE*1))
        self.image.fill(BLEU)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.dir = self.game.player.dir
        self.lifespan = lifespan  # Number of frames before disappearing
        self.movement = movement
        self.timer = 0  # Initialize timer
        print("I created a pew pew...")

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                hits[0].hitpoints -= 1
                print(hits[0].hitpoints)
            if str(hits[0].__class__.__name__) == "Mob2":
                hits[0].hitpoints -= 1
                self.kill
            # self.kill()

    def update(self):
        self.collide_with_group(self.game.mobs, False)
        self.rect.x += self.dir[0]*self.speed
        self.rect.y += self.dir[1]*self.speed
        self.timer += 1  # Increment timer
        if self.timer >= self.movement:
            self.speed = 0
            self.image = pg.Surface((TILESIZE*1.5, TILESIZE*1.5))
            self.image.fill(BLEU)
        if self.timer >= self.lifespan:
            self.kill()  # Destroy the projectile if the timer exceeds lifespan

class Molt(pg.sprite.Sprite):
    def __init__(self, game, x, y, lifespan=10):  # Lifespan is in frames
        self.groups = game.all_sprites, game.molt
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE*1, TILESIZE*1))
        self.image.fill(MOLTCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.dir = self.game.player.dir
        self.lifespan = lifespan  # Number of frames before disappearing
        self.timer = 0
        print("I molted")
    def update(self):
        self.timer += 1  
        if self.timer >= self.lifespan:
            self.kill()  # Destroy the projectile if the timer exceeds lifespan

