import pygame as pg
import sys
from os import path
from manager import *
from settings import *
from sprites import *
from tilemap import *
import time as t

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        
        self.max_time = -1
        self.current_time = -1

        self.max_time = INITIAL_MAX_TIME
        self.init_data()
        
    def init_data(self):
        # Init managers
        self.audio_mgr = AudioManager(self)
        self.floor_mgr = FloorManager(self)
        self.hud = HudManager(self)
        
        # Init time
        self.current_time = self.max_time
        
        # Init GAMESTATE
        self.gamestate = "START_SCREEN"

        # Init sprites group
        self.background = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.walls_gr = pg.sprite.Group()
        self.enemy_gr = pg.sprite.Group()
        self.player_gr = pg.sprite.Group()
        self.warp_gr = pg.sprite.Group()
        self.rope_gr = pg.sprite.Group()
        self.money_gr = pg.sprite.Group()
    
    def generate_current_map(self):
        # Disable player controls and reset velocity
        self.player.vel = Vector2(0,0)
        self.player.isActive = False

        # Get next floor
        self.map = self.floor_mgr.request_floor().map

        # Set player position 
        self.player.set_at_position(ROOMSIZE/2-2, ROOMSIZE/2-2)

        # Reset camera
        self.camera = Camera(self.map.width+2*TILESIZE, self.map.height+2*TILESIZE)

    def start_floor(self):
        # Enable player controls
        self.player.isActive = True

        # Start map
        self.map.start_floor()

    def new(self):        
        # Generate player
        self.player = Player(self, ROOMSIZE/2-2, ROOMSIZE/2-2)
        self.player.data.current_hp = self.player.data.hp

        # Generate map
        self.generate_current_map()

        # Start music
        self.audio_mgr.stop_bgm()
        self.audio_mgr.play_bgm("gameplay")

    def cleanup(self):
        # Clear collectibles from this floor
        for sprite in self.money_gr:
            sprite.kill()
        for sprite in self.rope_gr:
            sprite.kill()
        for sprite in self.background:
            sprite.kill()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.map.update()
        self.camera.update(self.player)
        self.hud.update()

        if not (self.map.isPlaying):
            if pg.key.get_pressed()[pg.K_BACKSPACE]:
                self.start_floor()
        else:
            self.current_time = self.current_time-self.dt

            if (self.current_time <=0):
                self.run_gameover_screen()


    def draw(self):
        self.screen.fill(BLACK)

        for bkg in self.background:
            self.screen.blit(bkg.image, bkg.rect)

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for element in self.hud.hud:
            data = element[0]
            pos = element[1]

            self.screen.blit(data,pos)

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


    def run(self):        
        while self.gamestate == "PLAYING":
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def run_start_screen(self):
        self.audio_mgr.stop_bgm()
        self.audio_mgr.play_bgm("alarm")

        while (self.gamestate == "START_SCREEN"):
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.hud.update()
            self.draw()
            
            if pg.key.get_pressed()[pg.K_BACKSPACE]:
                self.gamestate = "PLAYING"

    def run_gameover_screen(self):        
        self.audio_mgr.stop_bgm()
        self.audio_mgr.play_bgm("defeat")

        self.gamestate = "GAME_OVER_SCREEN"
        for sprite in self.all_sprites:
            sprite.kill()
        self.cleanup()
        while (self.gamestate == "GAME_OVER_SCREEN"):
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.hud.update()
            self.draw()
        
    def run_victory_screen(self):
        self.audio_mgr.stop_bgm()
        self.audio_mgr.play_bgm("victory")

        self.gamestate = "VICTORY_SCREEN"
        for sprite in self.all_sprites:
            sprite.kill()
        self.cleanup()
        while (self.gamestate == "VICTORY_SCREEN"):
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.hud.update()
            self.draw()

            if pg.key.get_pressed()[pg.K_BACKSPACE]:
                self.quit()

    def run_runaway_screen(self, earned):
        self.audio_mgr.stop_bgm()
        self.audio_mgr.play_bgm("runaway")

        self.gamestate = "RUNAWAY_SCREEN"
        for sprite in self.all_sprites:
            sprite.kill()
        self.cleanup()

        while (self.gamestate == "RUNAWAY_SCREEN"):
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.hud.update()
            self.draw()

            if pg.key.get_pressed()[pg.K_BACKSPACE]:
                # If play again is pressed restart the game with
                # the new maxtime
                self.max_time = self.max_time + earned/10
                self.init_data()
                self.new()
                self.gamestate = "PLAYING"
        pass

# create the game object
g = Game()
g.gamestate = "START_SCREEN"
while True:
    if (g.gamestate=="START_SCREEN"):
        g.run_start_screen()
    if (g.gamestate=="PLAYING"):
        g.new()
        g.run()
