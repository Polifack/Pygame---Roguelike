import pygame as pg
import string as s
from os import path
from settings import *
from sprites import * 
from random import seed, random, choice


class Floor:
    def __init__(self, game, floor_number):
        self.map = None
        self.game = game
        self.floor_number = floor_number

    
    def generate(self):
        game_folder = path.dirname(__file__)
        
        # this is useful in case we want different floors to have
        # different layouts
        if (self.floor_number == 0):
            floor_file = './rooms/rooms.txt'
        
        map_file = path.join(game_folder, './rooms/rooms.txt')
        boss_file = path.join(game_folder, './rooms/boss_rooms.txt')
        
        self.map = Map(self.game, self.floor_number+1, map_file, boss_file)

    def end_floor(self):
        # Kill map structure
        for gameobject in self.map.data:
            gameobject.kill()
        self.game.cleanup()
        
        
class Map:
    def __init__(self, game, floor, normal_rooms_file, boss_rooms_file):
        self.game = game
        self.floor = floor

        # List of the gameobjects in the map
        # List of the rooms in the map
        self.data = []
        self.rooms = []

        # Read rooms files and generate map
        rf = open(normal_rooms_file, 'rt')
        bf = open(boss_rooms_file, 'rt')
        self.generate_map(rf,bf)

        # Generate background
        Background(self.game, floor)
        
        # The size of the map will deppend on the number of rooms + 1
        # because of the boss room
        self.tilewidth = ROOMSIZE * (NROOMS + 1)
        self.tileheight = ROOMSIZE
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

        # isPlaying
        self.isPlaying = False

    def start_floor(self):
        self.isPlaying = True

    def read_rooms(self, rooms_file):
        # Read the rooms from the rooms file
        lines = rooms_file.readlines()
        disponible_rooms = []

        i = 0
        current_room = []
        for line in lines:
            current_room.append(line)
            i+=1

            if i == ROOMSIZE:
                disponible_rooms.append(current_room)
                current_room = []
                i = 0

        return disponible_rooms

    def generate_rooms(self, disponible_rooms):
        rooms = []
        for nroom in range(0, NROOMS):
            current_room = []
            seed()
            i=0

            room = choice(disponible_rooms)

            for line in room:
                # Parse the room lines 
                current_room.append(line)
                i+=1

                if i == ROOMSIZE:                   
                    # All rooms except the first one will have a entry door and exit door    
                    # The entry door will be represented by 'a' and exit by 'b'

                    half_row = current_room[int(ROOMSIZE/2)]
                    half_row = 'a'+half_row[1:-2]+'b'
                    current_room[int(ROOMSIZE/2)]=half_row

                    half_row = current_room[int(ROOMSIZE/2+1)]
                    half_row = 'a'+half_row[1:-2]+'b'
                    current_room[int(ROOMSIZE/2+1)]=half_row
                    

                    if nroom == 0:
                        # If we are in the first room we will only have a exit door
                        current_room[int(ROOMSIZE/2)]='4'+current_room[int(ROOMSIZE/2)][1:-1]+'b'
                        current_room[int(ROOMSIZE/2+1)]='4'+current_room[int(ROOMSIZE/2+1)][1:-1]+'b'


                    rooms.append(current_room)
                    current_room = []
                    i = 0

        return rooms

    def generate_boss_room(self, normal_rooms, boss_room):
        current_room = []
        i=0
        for line in boss_room[0]:
            current_room.append(line)
            i+=1
            if i == ROOMSIZE:
                # In the half of the room we will have the door to the
                # boss room and a warp to the next floor, that will
                # be locked until we kill the boss

                half_row = current_room[int(ROOMSIZE/2)]
                half_row = 'a'+half_row[1:-2]+'w'
                current_room[int(ROOMSIZE/2)]=half_row
                current_room[int(ROOMSIZE/2+1)]=half_row

        normal_rooms.append(current_room)

        return normal_rooms

    def generate_map(self, rooms_file, boss_file):
        disponible_rooms = self.read_rooms(rooms_file)
        boss_rooms = self.read_rooms(boss_file)

        rooms = self.generate_rooms(disponible_rooms)
        rooms = self.generate_boss_room(rooms, boss_rooms)

        room_center = (0,-2)

        i = 0
        for room in rooms:
            # Generate room to the right
            # And if it is the last room, generate boss room
            i+=1
            is_boss = (i==NROOMS+1)
            self.generate_gameobjects(room_center, room, is_boss)
            room_center = (room_center[0] + (ROOMSIZE), room_center[1])
            
    def generate_gameobjects(self, room_center, room_shape, is_boss):
        i = 0
        j = 0

        enemies = []
        enter_doors = []
        exit_doors = []
        warps = []
        room = None

        for row in room_shape:
            j = 0
            i +=1
            for col in row:
                j +=1

                # File parsing by chars
                if col in ('1','2','3','4','5','6','7','8','9','0'):
                    self.data.append(Wall(self.game, room_center[0]+j, room_center[1]+i, col, self.floor))
                if col == 'a':
                    enter_door = Door(self.game, room_center[0]+j, room_center[1]+i, False)
                    enter_door.open_door()

                    enter_doors.append(enter_door)

                    self.data.append(enter_door)
                if col == 'b':
                    exit_door = Door(self.game, room_center[0]+j, room_center[1]+i, True)
                    exit_doors.append(exit_door)
                    self.data.append(exit_door)
                if col == 'e':
                    enemy = None
                    
                    if self.floor == 1:
                        enemy = FirstFloorEnemy(self.game, room_center[0]+j, room_center[1]+i)
                    if self.floor == 2:
                        enemy = SecondFloorEnemy(self.game, room_center[0]+j, room_center[1]+i)
                    if self.floor == 3:
                        enemy = ThirdFloorEnemy(self.game, room_center[0]+j, room_center[1]+i)
                    
                    self.data.append(enemy)
                    enemies.append(enemy)
                if col == 'c':
                    boss = BossEnemy(self.game, room_center[0]+j, room_center[1]+i)
                    self.data.append(boss)
                if col == 'w':
                    warp = Warp(self.game, room_center[0]+j, room_center[1]+i)
                    
                    warps.append(warp)
                    
                    self.data.append(warp)
        
        # Use the room boundaries in x axis to determine if the player is in the room
        room_boundaries = (room_center[0]*TILESIZE, (room_center[0]+ROOMSIZE)*TILESIZE)
        
        room = None
        
        if not (is_boss):
            room = Room(self.game, self, room_boundaries, enemies, enter_doors, exit_doors)
        else:
            room = BossRoom(self.game, self, room_boundaries, boss, enter_doors, warps)
        
        self.rooms.append((room_boundaries,room))

    def update(self):
        # If the floor is still generating, wait
        if not self.isPlaying:
            return 
        
        # Update the active rooms
        for (boundaries, room) in self.rooms:
            if self.game.player.rect.x in range(boundaries[0]+2*TILESIZE, boundaries[1]):
                if room.state == "UNCLEARED":
                    room.start_room()
            
            room.update()


class Room:
    def __init__(self, game, tilemap, room_boundaries, enemies, enter_door, exit_door):
        # Class that defines a room
        # It contains references to the ENEMIES and the DOOR
        # the ENTER DOOR will close once the player enters the room and wont open until he finishes it
        # the EXIT DOOR will open once all enemies are defeated

        # Init reference to the game and the map
        self.game = game
        self.map = tilemap

        # Set the room boundaries in x axis
        self.boundaries = room_boundaries

        # The enemies in the room will begin attacking the player once he enters the room
        # they will ignore him otherwise
        self.enemies = enemies
        
        # Set the enter and exit door references
        self.exit_door = exit_door
        self.enter_door = enter_door

        # State of the room can be UNCLEARED, PLAYING or CLEARED
        self.state = "UNCLEARED"


    def start_room(self):
        # close the doors
        for door in self.enter_door:
            door.close_door()
        for door in self.exit_door:
            door.close_door()
                
        # acitate the enemies
        for enemy in self.enemies:
            enemy.isActive = True
                
        # and move to state to playing
        self.map.current_room = self
        self.state = "PLAYING"
    
    def switch_state(self):
        # If the room is uncleared...
        if self.state == "UNCLEARED":
            pass
        
        # If we are playing...
        if self.state == "PLAYING":
            # ...and we kill all enemies...
            if self.enemies == []:
                self.state = "CLEARED"
                
                # we open the doors...
                for door in self.enter_door:
                    door.open_door()
                for door in self.exit_door:
                    door.open_door()

        if self.state == "CLEARED":
            pass
    
    def update(self):
        self.switch_state()

        # Check the enemies, if they are in 0 groups that means they are dead
        # so remove them
        for enemy in self.enemies:
            if not enemy.data.isAlive:
                self.enemies.remove(enemy)

class BossRoom():
    def __init__(self, game, tilemap, room_boundaries, boss, enter_door, warp_door):
        # Class that defines a boss room
        # We keep track of the boss, the enter door and the warp

        # Init reference to the game and the map
        self.game = game
        self.map = tilemap

        # Set the room boundaries in x axis
        self.boundaries = room_boundaries

        # The enemies in the room will begin attacking the player once he enters the room
        # they will ignore him otherwise
        self.boss = boss
        
        # Set the enter and exit door references
        self.warp = warp_door
        self.enter_door = enter_door

        # State of the room can be UNCLEARED, PLAYING or CLEARED
        self.state = "UNCLEARED"

    def start_room(self):
        # close the doors
        for door in self.enter_door:
            door.close_door()
                
        # acitate the enemies
        self.boss.isActive = True
                
        # and move to state to playing
        self.map.current_room = self
        self.state = "PLAYING"

    def switch_state(self):
        # If the room is uncleared...
        if self.state == "UNCLEARED":
            pass
        
        # If we are playing...
        if self.state == "PLAYING":
            # ...and we kill all enemies...
            if not self.boss.data.isAlive:
                self.state = "CLEARED"
                
                # we open the warp...
                for warp in self.warp:
                    warp.open_warp()

        if self.state == "CLEARED":
            pass
    
    def update(self):
        self.switch_state()


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Move all the other gameobjects to make them fit the camera
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # move the camera with the player (target)
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        
        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
