import pygame as pg

from pygame.math import *
from settings import *
from tilemap import *


class AudioManager:
    def __init__(self, game):
        self.game = game

        # Initialize channels
        self.sfx_channel = pg.mixer.Channel(1)
        
        self.footstep_channel = pg.mixer.Channel(2)
        self.footstep_channel.set_volume(0.5)
        
        self.gun_channel = pg.mixer.Channel(3)
        self.footstep_channel.set_volume(0.4)

        # Initialize audios
        # Initialize them with an isplaying variable
        self.footsteps = pg.mixer.Sound("./audio/sfx/footstep.wav")
        self.gun = pg.mixer.Sound("./audio/sfx/gun.wav")




    def play_sfx(self, sfx_name):
        # check audio name
        # and check if is playing
        # and play it
        if (sfx_name == "footsteps"):
            if not self.footstep_channel.get_busy():
                self.footstep_channel.play(self.footsteps)
        if (sfx_name == "gun"):
            if not self.gun_channel.get_busy():
                self.gun_channel.play(self.gun)

    def stop_sfx(self, sfx_name):
        # just stop them
        if (sfx_name == "footsteps"):
            self.footsteps.stop()
        if (sfx_name == "gun"):
            self.gun.stop()
        

    def play_bgm(self, sound):
        if (sound == "alarm"):
            pg.mixer.music.load("./audio/bgm/alarm.wav")
        if (sound == "gameplay"):
            pg.mixer.music.load("./audio/bgm/gameplay.wav")
        if (sound == "defeat"):
            pg.mixer.music.load("./audio/bgm/defeat.wav")
        if (sound == "victory"):
            pg.mixer.music.load("./audio/bgm/victory.wav")
        if (sound == "runaway"):
            pg.mixer.music.load("./audio/bgm/runaway.wav")

        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)

    def stop_bgm(self):
        pg.mixer.music.stop()

class HudManager:
    def __init__(self, game):
        self.hud = []
        self.game = game

    def show_game_gui(self):
        self.hud = []        
        hp_bar = pg.font.SysFont('Consolas', 25).render("hp: "+str(self.game.player.data.current_hp), False, WHITE)
        current_floor = pg.font.SysFont('Consolas', 25).render("floor: "+str(self.game.floor_mgr.current_floor), False, WHITE)
        money_indicator = pg.font.SysFont('Consolas', 25).render("money: "+str(self.game.player.data.money), False, WHITE)
        time_indicator = None
        if (self.game.map.isPlaying):
            time_indicator = pg.font.SysFont('Consolas', 25).render("time: "+str(int(self.game.current_time)), False, WHITE)
        else:
            time_indicator =pg.font.SysFont('Consolas', 25).render("press backspace to start", False, WHITE)

        self.hud.append((hp_bar, (0.1*WIDTH, HEIGHT-0.1*HEIGHT)))
        self.hud.append((current_floor, (0.1*WIDTH, HEIGHT-0.05*HEIGHT)))
        self.hud.append((time_indicator, (0.5*WIDTH, HEIGHT-0.05*HEIGHT)))
        self.hud.append((money_indicator, (0.5*WIDTH, HEIGHT-0.1*HEIGHT)))

    def show_init_gui(self):
        self.hud = []       
        text_1 = "The alarm has been activated..."
        text_2 = "Take everything you can..."
        text_3 = "You have "+str(self.game.current_time)+" seconds..."

        text_4 = "Press backspace to start"

        msg_1 = pg.font.SysFont('Consolas', 25).render(text_1, False, WHITE)
        msg_2 = pg.font.SysFont('Consolas', 25).render(text_2, False, WHITE)
        msg_3 = pg.font.SysFont('Consolas', 25).render(text_3, False, WHITE)
        msg_4 = pg.font.SysFont('Consolas', 25).render(text_4, False, WHITE)

        self.hud.append((msg_1, (0.2*WIDTH, 0.1*HEIGHT)))
        self.hud.append((msg_2, (0.2*WIDTH, 0.2*HEIGHT)))
        self.hud.append((msg_3, (0.2*WIDTH, 0.3*HEIGHT)))
        self.hud.append((msg_4, (0.2*WIDTH, 0.6*HEIGHT)))

    def show_end_gui(self):
        self.hud = []       
        text_1 = "You could not escape..."
        text_2 = "There is no second chance."

        msg_1 = pg.font.SysFont('Consolas', 25).render(text_1, False, WHITE)
        msg_2 = pg.font.SysFont('Consolas', 25).render(text_2, False, WHITE)

        self.hud.append((msg_1, (0.2*WIDTH, 0.1*HEIGHT)))
        self.hud.append((msg_2, (0.2*WIDTH, 0.2*HEIGHT)))

    def show_runaway_gui(self):
        self.hud = []       
        text_1 = "You escaped."
        text_2 = "You can live another day"
        text_3 = "You earned "+str(self.game.player.data.money)+"$"
        text_4 = "Now you have "+str(self.game.player.data.money/10)+" aditional seconds"

        
        text_5 = "Press backspace to start"

        msg_1 = pg.font.SysFont('Consolas', 25).render(text_1, False, WHITE)
        msg_2 = pg.font.SysFont('Consolas', 25).render(text_2, False, WHITE)
        msg_3 = pg.font.SysFont('Consolas', 25).render(text_3, False, WHITE)
        msg_4 = pg.font.SysFont('Consolas', 25).render(text_4, False, WHITE)
        msg_5 = pg.font.SysFont('Consolas', 25).render(text_5, False, WHITE)

        self.hud.append((msg_1, (0.2*WIDTH, 0.1*HEIGHT)))
        self.hud.append((msg_2, (0.2*WIDTH, 0.2*HEIGHT)))
        self.hud.append((msg_3, (0.2*WIDTH, 0.3*HEIGHT)))
        self.hud.append((msg_4, (0.2*WIDTH, 0.5*HEIGHT)))
        self.hud.append((msg_5, (0.2*WIDTH, 0.6*HEIGHT)))
    
    def show_victory_gui(self):
        self.hud = []       
        text_1 = "You reached the last floor."
        text_2 = "Congratulations!"
        
        text_5 = "Press backspace to exit the game"

        msg_1 = pg.font.SysFont('Consolas', 25).render(text_1, False, WHITE)
        msg_2 = pg.font.SysFont('Consolas', 25).render(text_2, False, WHITE)
        msg_5 = pg.font.SysFont('Consolas', 25).render(text_5, False, WHITE)

        self.hud.append((msg_1, (0.3*WIDTH, 0.1*HEIGHT)))
        self.hud.append((msg_2, (0.3*WIDTH, 0.2*HEIGHT)))
        self.hud.append((msg_5, (0.3*WIDTH, 0.6*HEIGHT)))


    def update(self):
        if (self.game.gamestate == "START_SCREEN"):
            self.show_init_gui()
        elif (self.game.gamestate == "PLAYING"):
            self.show_game_gui()
        elif (self.game.gamestate == "GAME_OVER_SCREEN"):
            self.show_end_gui()
        elif (self.game.gamestate == "RUNAWAY_SCREEN"):
            self.show_runaway_gui()
        elif (self.game.gamestate == "VICTORY_SCREEN"):
            self.show_victory_gui()


class FloorManager:
    def __init__(self, game):
        self.game = game
        self.floors = []
        self.current_floor = 0

        for i in range(0, NFLOORS):
            temp_floor = Floor(self.game, i)
            self.floors.append(temp_floor)

    def end_floor(self):
        last_floor = self.floors[(self.current_floor-1)]
        last_floor.end_floor()
        

    def request_floor(self):
        # End the old floor (skip if we are in the first one)
        if (self.current_floor!=0):
            self.end_floor()

        if (self.current_floor == NFLOORS):
            self.game.run_victory_screen()
            return
        
        # Generate new
        next_floor = self.floors[self.current_floor]
        next_floor.generate()

        # Increase current floor
        self.current_floor+=1

        return next_floor