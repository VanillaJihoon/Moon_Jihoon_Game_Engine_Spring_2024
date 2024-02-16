# This file was created by Jihoon Moon
# Appreciatoin to Chris Bradfield
import pygame as pg
from settings import *

# write a player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.groups = self.game.all_sprites
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
#moving the Player class
    
    #negative and positive player speeds
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED

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
    
    
    def collide_with_killbrick(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.Killbrick, False)
            if self.vx > 0:
                self.x = hits[0].rect.top - self.rect.height
            if self.vx < 0:
                self.x = hits[0].rect.bottom
            self.vx = 0
            self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.Killbrick, False )
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
        
                

             
    
    #Old motion
    #def move(self, dx=0, dy=0):
        #self.x += dx
        #self.y += dy
#Making it update when it moves
    #New update
        #Update the update
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        #self.rect.x = self.x * TILESIZE
        #self.rect.y = self.y * TILESIZE
# another class
class Wall(pg.sprite.Sprite):
    #game is inside of the class again alongside self
    def __init__(self, game, x, y):
        #all sprites used, 
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #making surface equal to tilesize
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #filling the surface yellow
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 0
    def update(self):
        self.rect.x += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1

class Killbrick(pg.sprite.Sprite):
    #game is inside of the class again alongside self
    def __init__(self, game, x, y):
        #all sprites used, 
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #making surface equal to tilesize
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #filling the surface yellow
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 1
    def update(self):
        self.rect.x += TILESIZE * self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
