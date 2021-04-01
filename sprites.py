import pygame as pg
import math as math

from pygame.math import *

from settings import *
from data import *
from animation import *

from random import seed, random, choice


class Entity(pg.sprite.Sprite):
    # Entity initialization

    def __init__(self, game, x, y, animation, data, groups):
        # Init data
        self.data = data

        # Init Sprite and Animation
        pg.sprite.Sprite.__init__(self, groups)

        self.walk_anim = animation[0]
        self.dodge_anim = animation[1]
        self.idle_anim = animation[2]

        self.animation = self.idle_anim

        self.image = self.animation.get_frame()
        self.original_image = self.image
        self.rect = self.image.get_rect()

        self.isFlipped = False
        
        # Set gamemanager
        self.game = game

        # Init velocity vector and position vector
        self.vel = Vector2(0, 0)
        self.pos = Vector2(x, y) * TILESIZE

        # Init weapon
        self.aim_direction = None
        self.gun = None
        
        # Sound
        self.footstep_sfx = None

        # State Machine
        self.isActive = False

        self.current_dodge_time = 0
        self.dodge_direction = Vector2(0,0)

        self.disponible_states = ["IDLE", "WALKING", "DODGING"]
        self.state = "IDLE"


    # Common functions

    def set_at_position(self, x, y):
        self.pos = Vector2(x, y) * TILESIZE

    def collide_with_walls(self, dir):
        # If we collide with walls we check the
        # direction of the collision and we put the player in the
        # tile closest to the wall he collided 
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls_gr, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls_gr, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
    
    def take_damage(self, ammount):
        # We will avoid taking damage when we are invulnerable (just after taking a hit)
        # and when we are doding
        if self.data.vulnerable and self.state!="DODGE":
            self.data.take_damage(ammount)

    def do_state(self):
        # If we are dodging, increase dodge time. When the dodge time reaches its max, exit dodge state
        if (self.state == "DODGE"):
            self.animation = self.dodge_anim
            if (self.current_dodge_time < self.data.dodge_time):
                self.current_dodge_time+=1 
            else:
                self.animation = self.idle_anim
                self.state = "IDLE"

            return

        # If we are not moving, set the state to idle, if we are, set it to walking
        if self.vel == Vector2(0,0):
            self.game.audio_mgr.stop_sfx(self.footstep_sfx)
            self.animation = self.idle_anim
            self.state = "IDLE"
        else:
            self.game.audio_mgr.play_sfx(self.footstep_sfx)
            self.animation = self.walk_anim
            self.state = "WALK"
        
        

    # Abstract functions

    def get_movement(self):
        pass

    def get_aim_direction(self):
        pass
        
    def do_die(self):
        pass

    # Update

    def update(self):
        # Get movement and aim
        self.get_movement()
        self.get_aim_direction()

        # Flip the image if needed
        self.image = pg.transform.flip(self.original_image, self.isFlipped, False)

        # State parsing
        self.do_state()

        # Apply movement
        self.pos += self.vel * self.game.dt

        self.rect.x = self.pos.x
        self.collide_with_walls('x')

        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        # Apply aim
        self.gun.update_position(self.pos.x, self.pos.y)
        self.gun.aim(self.aim_direction)

        # Check if alive
        if not self.data.isAlive:
            self.do_die()

        # Update data
        self.data.update()


class Player(Entity):
    def __init__(self, game, x, y):
        # Set sprite and target
        target = game.enemy_gr
        data = PlayerData()

        walk_sheet = pg.image.load("./sprites/player_sheet_walk.png")
        idle_sheet = pg.image.load("./sprites/player_sheet_idle.png")
        dodge_sheet =  pg.image.load("./sprites/player_sheet_dodge.png")

        walk_anim = animation(walk_sheet,(SPRITESIZE,SPRITESIZE),5,0,6)
        dodge_anim = animation(dodge_sheet,(SPRITESIZE,SPRITESIZE),5,0,5)
        idle_anim =  animation(idle_sheet,(SPRITESIZE,SPRITESIZE),5,0,4)

        animations = [walk_anim, dodge_anim, idle_anim]
        
        super(Player, self).__init__(game, x, y, animations, data,(game.all_sprites, game.player_gr))

        self.footstep_sfx = "footsteps"
        self.gun = Gun(self.game, x, y, ShotGunData(GREEN),target)

    def get_movement(self):
        # If player is not active dont move
        if not self.isActive:
            return

        # Get keys
        keys = pg.key.get_pressed()
        
        # If the player is dodging, dont move
        # the movement will be the dodge direction
        if self.state == "DODGE":
            self.vel = self.dodge_direction
            return

        # If space pressed, change state to dodge and store velocity
        if keys[pg.K_SPACE]:
            self.state = "DODGE"
            self.current_dodge_time = 0
            self.dodge_direction = self.vel * self.data.dodge_multiplier
            return 

        # Reset the velocity
        self.vel = Vector2(0, 0)

        # Parse direction keys
        if keys[pg.K_a]:
            self.vel.x = -self.data.speed

            # If we are swaping direction, flip the sprite
            if self.vel.x < 0:
                self.isFlipped = True
            else: 
                self.isFlipped = False
        if keys[pg.K_d]:
            self.vel.x = self.data.speed

            # If we are swaping direction, flip the sprite
            if self.vel.x < 0:
                self.isFlipped = True
            else: 
                self.isFlipped = False
        if keys[pg.K_w]:
            self.vel.y = -self.data.speed
        if  keys[pg.K_s]:
            self.vel.y = self.data.speed
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.75

    def get_aim_direction(self):
        # If player is not active dont move
        if not self.isActive:
            return

        # If gun is not ready to shoot just ignore
        if not self.gun.can_shoot:
            return

        keys = pg.key.get_pressed()

        aim_direction = None

        if keys[pg.K_LEFT] :
            aim_direction = "L"

        if keys[pg.K_RIGHT] :
            aim_direction = "R"
        if keys[pg.K_UP] :
            aim_direction = "U"
        if keys[pg.K_DOWN] :
            aim_direction = "D"

        self.aim_direction = aim_direction

    def collide_with_warp(self):
        hits = pg.sprite.spritecollide(self, self.game.warp_gr, False)

        # If the player collides with the warp we regenerate the map
        if (hits):
            self.game.generate_current_map()

    def collide_with_rope(self):
        hits = pg.sprite.spritecollide(self, self.game.rope_gr, False)

        # If the player collides with the warp we go to the runaway screen
        if (hits):
            self.game.run_runaway_screen(self.data.money)

    def collide_with_money(self):
        hits = pg.sprite.spritecollide(self, self.game.money_gr, False)

        # If the player collides with the warp we go to the runaway screen
        if (hits):
            for hit in hits:
                self.data.money += hit.ammount
                hit.kill()

    def do_die(self):
        self.kill()
        self.gun.kill()
        self.game.run_gameover_screen()

    def update(self):
        self.original_image = self.animation.get_frame()

        super(Player, self).update()
        
        self.collide_with_warp()
        self.collide_with_rope()
        self.collide_with_money()

class Enemy(Entity):
    def __init__(self, game, x, y, animations, data):
        # Set money drop chance
        self.money_chance = 0
        self.money_range = range(0,0)
        # Initialize entity
        super(Enemy, self).__init__(game, x, y, animations, data,(game.all_sprites, game.enemy_gr))
        self.footstep_sfx = "footsteps"

    def get_target(self):
        player_pos = self.game.player.pos
        self_pos = self.pos
        return player_pos-self_pos
    
    def get_movement(self):
        if self.isActive:
            self.vel = self.get_target().normalize()*self.data.speed
        else:
            self.vel = Vector2(0,0)

    def get_aim_direction(self):
        if not self.gun.can_shoot:
            return
        if not self.isActive:
            return 
        
        delta_pos = self.get_target()

        aim_direction_x = None
        aim_direction_y = None

        # If the player is on the left of the enemy, flip the enemy
        if (delta_pos.x < 0):
            self.isFlipped = True
            aim_direction_x = "L"
        else:
            self.isFlipped = False
            aim_direction_x = "R"

        # If the player is above or below the enemy
        if (delta_pos.y>0):
            aim_direction_y="D"
        else:
            aim_direction_y="U"

        # Choose the best direction to shoot based on distance
        self.aim_direction = None
        if (abs(delta_pos.x) < abs(delta_pos.y)): 
            self.aim_direction = aim_direction_y
        else: 
            self.aim_direction = aim_direction_x

    def do_die(self):
        # Generate money as reward 
        seed()
        if (random()>self.money_chance):
            Money(self.game, self.pos.x, self.pos.y, choice(self.money_range))

        # And die
        super().kill()
        self.gun.kill()

    def kill(self):
        # override kill to delete the weapon too
        self.do_die()

    def update(self):
        self.original_image = self.animation.get_frame()
        super(Enemy, self).update()

class FirstFloorEnemy(Enemy):
    def __init__(self, game, x, y):
        data = EnemyFirstFloorData()

        sheet = pg.image.load("./sprites/enemy_sheet_1.png")
        anim = animation(sheet,(SPRITESIZE,SPRITESIZE),5,0,6)

        animations = [anim, anim, anim]

        super(FirstFloorEnemy, self).__init__(game, x, y, animations, data)
        self.gun = Gun(self.game, x, y, ShotGunData(BLACK),game.player_gr)

        self.money_chance = 0.1
        self.money_range = range(1,10)

class SecondFloorEnemy(Enemy):
    def __init__(self, game, x, y):
        data = EnemySecondFloorData()

        sheet = pg.image.load("./sprites/enemy_sheet_2.png")
        anim = animation(sheet,(SPRITESIZE,SPRITESIZE),5,0,6)

        animations = [anim, anim, anim]

        super(SecondFloorEnemy, self).__init__(game, x, y, animations, data)
        self.gun = Gun(self.game, x, y, ShotGunData(BLACK),game.player_gr)

        self.money_chance = 0.4
        self.money_range = range(11,20)

class ThirdFloorEnemy(Enemy):
    def __init__(self, game, x, y):
        data = EnemyThirdFloorData()

        sheet = pg.image.load("./sprites/enemy_sheet_3.png")
        anim = animation(sheet,(SPRITESIZE,SPRITESIZE),5,0,6)

        animations = [anim, anim, anim]

        super(ThirdFloorEnemy, self).__init__(game, x, y, animations, data)
        self.gun = Gun(self.game, x, y, MachineGunData(BLACK),game.player_gr)

        self.money_chance = 0.3
        self.money_range = range(21,40)


class BossEnemy(Enemy):
    def __init__(self, game, x, y):
        # Set sprite and data
        data = BossEnemyData()

        sheet = pg.image.load("./sprites/boss_sheet.png")
        anim = animation(sheet,(64,64),10,0,5)
        animations = [anim, anim, anim]
        
        # Initialize entity
        super(BossEnemy, self).__init__(game, x, y, animations, data)
        self.gun = Gun(self.game, x, y, BossGunData(PINK),game.player_gr)

        # Initialize loot
        self.money_chance = 1           # The boss will not drop normal money

        self.n_bags = range(1,5)        # Ammount of bags dropped
        self.money_range = range(10,50)   # Ammount of money in bags
        

    def do_die(self):
        # Generate a rope
        Rope(self.game, self.pos.x, self.pos.y)

        # Generate money
        for i in self.n_bags:
            bag_x_pos = self.pos.x+(1+random()*4)*TILESIZE
            bag_y_pos = self.pos.y+(1+random()*4)*TILESIZE
            Money(self.game, bag_x_pos, bag_y_pos, choice(self.money_range))

        # Just die already
        super().do_die()

        


class Gun(pg.sprite.Sprite):
    def __init__(self, game, x, y, gun_data, target_group):
        # Init sprite and groups
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        # Init data
        self.data = gun_data

        # Set game instance and target_group
        self.game = game
        self.target_group = target_group
        
        # Init image and store it to rotate easilly
        self.image = pg.image.load("./sprites/gun.png").convert_alpha()
        self.orig_img = self.image
        self.rect = self.image.get_rect()

        # Init position and rotation
        self.pos = Vector2(x, y) * TILESIZE
        self.rotation = 0

        # Init shoot direction vector and shoot offset
        # The shoot vector indicates the bullet direction and
        # the offset indicates the spawn point
        self.shoot_vector = Vector2(0,1)
        self.shoot_offset = Vector2(16, 16)

        # Init gun stats (Cooldown and damage)
        # This stats will vary depending on the gun type
        # Cooldown -> wait time between shoots
        # Damage   -> damage dealt by bullet
        self.current_cd = 0
        self.can_shoot = True

        self.damage = 1
    
    def update_position(self, x, y):
        self.pos = Vector2(x,y)

    def aim(self, direction):
        keys = pg.key.get_pressed()

        # We rotate the gun possition 
        # and change the shoot direction and the shoot offset
        if direction == "L" :
            self.image = pg.transform.flip(self.orig_img, True, False)
            
            self.shoot_vector = Vector2(-1,0)
            self.shoot()
        
        if direction == "R" :
            self.image = self.orig_img
            
            self.shoot_vector = Vector2(1,0)
            self.shoot()
        
        if direction == "U" :
            self.image = pg.transform.rotate(self.orig_img, 90)

            self.shoot_vector = Vector2(0, -1)
            self.shoot()
        
        if direction == "D" :
            self.image = pg.transform.rotate(self.orig_img, 90)
            self.image = pg.transform.flip(self.image, False, True)
            
            self.shoot_vector = Vector2(0, 1)
            self.shoot()

    def shoot(self):
        if (self.can_shoot):
                self.game.audio_mgr.play_sfx("gun")

                shoot_pos_x = self.pos.x+self.shoot_offset.x 
                shoot_pos_y = self.pos.y+self.shoot_offset.y
                Bullet(shoot_pos_x, shoot_pos_y, self.shoot_vector, self.game, self.target_group, self.data)
                self.current_cd = 0
                self.can_shoot = False

    def update(self):

        self.current_cd += 1 

        if (self.current_cd >= self.data.cooldown):
            self.can_shoot = True
        
        self.rect.x = self.pos.x+(self.shoot_offset*0.5).x
        self.rect.y = self.pos.y+(self.shoot_offset*0.5).y

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, shoot_direction, game, target_group, gun_data):
        self.groups = game.all_sprites
        
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.image = pg.Surface((TILESIZE/8, TILESIZE/8))
        self.image.fill(gun_data.bullet_color)
        self.rect = self.image.get_rect()

        self.pos = Vector2(x, y)
        self.direction = shoot_direction
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
        self.speed = gun_data.bullet_speed
        self.target_group = target_group

        self.damage = gun_data.damage

        self.alive_time = 0
        self.max_alive_time = gun_data.reach

    
    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls_gr, False)
        if hits: 
            self.kill()
    
    def collide_with_enemy(self):
        hits = pg.sprite.spritecollide(self, self.target_group, False)
        if hits:
            for hit in hits:
                hit.take_damage(self.damage)
                self.kill()
        
    def move(self):
        self.pos.x += self.direction.x * self.speed
        self.pos.y += self.direction.y * self.speed

    def update(self):
        # Check for bullet dissapear
        self.alive_time+=1
        if (self.alive_time > self.max_alive_time):
            self.kill()

        # Check collisions
        self.collide_with_enemy()
        self.collide_with_walls()

        # Compute movement
        self.move()
        
        # Update render position
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y    


class Background(pg.sprite.Sprite):
    def __init__(self, game, floor):
        self.groups = game.background
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = pg.Surface((WIDTH, HEIGHT-3*TILESIZE))
        color = WHITE
        if (floor == 1):
            color = BG_BLUE
        if (floor == 2):
            color = BG_YELLOW
        if (floor == 3):
            color = BG_RED
        
        self.image.fill(color)
        self.rect = self.image.get_rect()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, side, floor):
        # Set group and init sprite
        self.groups = game.all_sprites, game.walls_gr
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # Set game manager reference
        self.game = game
        
        # Init sprite and rect
        sprite_sheet = "./sprites/wall_sheet_"+str(floor)+".png" 
        wall_sheet = pg.image.load(sprite_sheet).convert_alpha()

        # The side is determined by the numpad
        # for example, number 7 will be top left corner
        if (side == '8'):
            self.image = wall_sheet.subsurface(pg.Rect((32,0),(32,32)))
        if (side == '7'):
            self.image = wall_sheet.subsurface(pg.Rect((0,0),(32,32)))
        if (side == '9'):
            self.image = wall_sheet.subsurface(pg.Rect((0,0),(32,32)))
            self.image = pg.transform.flip(self.image, True, False)
        if (side == '4'):
            self.image = wall_sheet.subsurface(pg.Rect((64,0),(32,32)))
        if (side == '6'):
            self.image = wall_sheet.subsurface(pg.Rect((64,0),(32,32)))
            self.image = pg.transform.flip(self.image, True, False)
        if (side == '1'):
            self.image = wall_sheet.subsurface(pg.Rect((96,0),(32,32)))
        if (side == '3'):
            self.image = wall_sheet.subsurface(pg.Rect((96,0),(32,32)))
            self.image = pg.transform.flip(self.image, True, False)

        self.image = pg.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.rect = pg.Rect((0,0),(TILESIZE,TILESIZE))
        
        # Init position 
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, isExit):
        # Assing the groups and init sprite
        self.groups = game.all_sprites, game.walls_gr
        pg.sprite.Sprite.__init__(self, self.groups)

        # Assign game manager reference
        self.game = game

        # Init sprite and rect
        sprite_sheet = "./sprites/door_sprite.png" 
        self.original_image = pg.image.load(sprite_sheet).convert_alpha()
        self.original_image = pg.transform.scale(self.original_image, (TILESIZE,TILESIZE))
        if (isExit):
            self.original_image = pg.transform.flip(self.original_image, True, False)
        self.image = self.original_image

        self.rect = pg.Rect((0,0),(TILESIZE,TILESIZE))
        
        
        # Set position in tilemap
        self.x = x
        self.y = y

        # Set position in world
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def open_door(self):
        # In order to open the door we remove the image and 
        # remove it from "walls" group
        self.game.walls_gr.remove(self)
        self.game.all_sprites.remove(self)

    def close_door(self):
        # In order to close the door we add the image and
        # add it to the "walls" group
        self.game.walls_gr.add(self)
        self.game.all_sprites.add(self)

        self.groups = self.game.all_sprites, self.game.walls_gr
        
        self.image = self.original_image

class Warp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Assing the groups and init sprite
        self.groups = game.all_sprites, game.walls_gr
        pg.sprite.Sprite.__init__(self, self.groups)

        # Assign game manager reference
        self.game = game

        # Init sprite and rect
        sprite_sheet = "./sprites/closed_warp_sprite.png" 
        self.image = pg.image.load(sprite_sheet).convert_alpha()
        self.image = pg.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.rect = pg.Rect((0,0),(TILESIZE,TILESIZE))
        
        # Set position in tilemap
        self.x = x
        self.y = y

        # Set position in world
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def open_warp(self):
        # In order to open the door we remove the image and 
        # remove it from "walls" group and add it to the warp_gr
        self.game.walls_gr.remove(self)
        self.game.warp_gr.add(self)
        self.groups = self.game.all_sprites, self.game.warp_gr

        sprite_sheet = "./sprites/open_warp_sprite.png" 
        self.image = pg.image.load(sprite_sheet).convert_alpha()
        self.image = pg.transform.scale(self.image, (TILESIZE,TILESIZE))

class Rope(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Assing the groups and init sprite
        self.groups = game.all_sprites, game.rope_gr
        pg.sprite.Sprite.__init__(self, self.groups)

        # Assign game manager reference
        self.game = game

        # Init sprite and rect
        sprite_sheet = "./sprites/rope.png" 
        self.image = pg.image.load(sprite_sheet).convert_alpha()
        self.image = pg.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.rect = pg.Rect((0,0),(TILESIZE,TILESIZE))

        # Set position in world
        self.rect.x = x 
        self.rect.y = y

class Money(pg.sprite.Sprite):
    def __init__(self, game, x,y, ammount):
        # Assing the groups and init sprite
        self.groups = game.all_sprites, game.money_gr
        pg.sprite.Sprite.__init__(self, self.groups)

        # Assign game manager reference
        self.game = game

        # Init sprite and rect
        sprite_sheet = "./sprites/money.png" 
        self.image = pg.image.load(sprite_sheet).convert_alpha()
        self.image = pg.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.rect = pg.Rect((0,0),(TILESIZE,TILESIZE))

        # Set position in world
        self.rect.x = x 
        self.rect.y = y

        self.ammount = ammount