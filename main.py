# This file was created by Jihoon Moon

# Goals: To kill every enemy, to not die
# Rules: HP goes to 0, die
# Feedback: Enemy hits you, HP goes down. Eat consumable, Buff/Debuff. 
# Freedom: Movement, Attack

# Health Bar, Weapons, Different enemies (moving)


# we are importing libraries
import pygame as pg
from settings import *
from sprites import *
import sys
from utils import *
from random import randint
from os import path
from math import floor
# We are creating a game class
        
        

class Game:
    
    #We define a method called init with the prameter called self. Init is basically making a new object of class and set its default state
    #init and run are both methods. that is why they are both on the same indent line
    def __init__(self):
        pg.init()
        #We set a screen and display and set parameters for it's width and height. Also responsible for FPS
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #We create a display and print a caption "My First Videogame"
        pg.display.set_caption("TITLE")
        #We set the parameter self with the variable clock to equal the pygame class Clock. (setting a clock)
        self.clock = pg.time.Clock() #Game tick
        self.load_data
        #Responsible for running the game (Run method)
        #Later on, game info is stored in this. 
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.snd_folder = path.join(game_folder, 'sounds')
        self.player_img = pg.image.load(path.join(img_folder, 'self.player_img.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, 'mob_img.png')).convert_alpha()
        self.map_data = []
        #WIth statement is a context manager
        #used to ensure a resource is properly closed or released after it is used
        #This helps to prevent errors.
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    def new(self):
        #pg.mixer.music.load(path.join(self.snd_folder, 'soundtrack2.mp3'))

        #makin the timer (i think)
        self.cooldown = Timer(self)
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.slash = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == '2':
                    self.player = Player(self, col, row)
                if tile == '3':
                    Coin(self, col, row)
                if tile == '4':
                    Mob(self, col, row)
                if tile == '5':
                    PowerUp(self, col, row)


    
    
    def run(self):
        #pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing: 
            self.dt = self.clock.tick(FPS) / 1000
            #This is input
            self.events()
            #This is processing
            self.update()
            #This is output
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
        #loop happens 30-60 times a second
    # method and functoins are blocks of code that you can tell it to do things whenever. mthods are like functions but they are tied to a class
            #pass means to skip over the code.
    def input(self):
        pass
    def update(self):
        self.cooldown.ticking()
        self.all_sprites.update()
#Drawing a grid
    def draw_grid(self):
        #if the x value goes out of range then nothing happens.
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
# Why does the defined draw also appear above itself?
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)


    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)
        pg.display.flip()
    
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)


    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True 
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    def show_go_screen(self):
        pass


#We instance game
g = Game()
g.show_start_screen()
while True:
# it is a method and it is a dependant part of
    g.new()
    g.run()
    # g.show_go_screen()

