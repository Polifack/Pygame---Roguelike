from settings import *

class EntityData:
    def __init__(self):
        self.isAlive = True

        self.hp = 100
        self.current_hp = 100

        self.speed = 100
        
        self.vulnerable = True
        self.invulnerability_time = 25
        self.current_vuln_time = 0
        self.dodge_time = 0

    def take_damage(self, ammount):
        self.current_hp = self.current_hp - ammount
        self.vulnerable = False
        
        if (self.current_hp <= 0):
            self.isAlive = False

    def update(self):
        if self.vulnerable == False:
            self.current_vuln_time+=1
            if self.current_vuln_time >=self.invulnerability_time:
                self.vulnerable = True
        else:
            self.current_vuln_time = 0

class PlayerData(EntityData):
    def __init__(self):
        super(PlayerData, self).__init__()
        self.hp = 200
        self.current_hp = self.hp
        self.speed = 250

        self.dodge_time = 20
        self.dodge_multiplier = 2

        self.money = 0

class EnemyFirstFloorData(EntityData):
    def __init__(self):
        super(EnemyFirstFloorData, self).__init__()
        self.hp = 10
        self.current_hp = self.hp
        self.speed = 80

class EnemySecondFloorData(EntityData):
    def __init__(self):
        super(EnemySecondFloorData, self).__init__()
        self.hp = 30
        self.current_hp = self.hp
        self.speed = 100

class EnemyThirdFloorData(EntityData):
    def __init__(self):
        super(EnemyThirdFloorData, self).__init__()
        self.hp = 30
        self.current_hp = self.hp
        self.speed = 120

class BossEnemyData(EntityData):
    def __init__(self):
        super(BossEnemyData, self).__init__()
        self.hp = 50
        self.current_hp = self.hp
        self.speed = 50



class GunData:
    def __init__(self):
        self.bullet_speed = 0
        self.bullet_color = WHITE
        self.damage = 0
        self.reach = 0
        self.cooldown = 0

class ShotGunData(GunData): 
    def __init__(self, color):
        self.bullet_speed = 10
        self.bullet_color = color
        self.damage = 20
        self.reach = 20
        self.cooldown = 50
        
class MachineGunData(GunData):
    def __init__(self, color):
        self.bullet_speed = 20
        self.bullet_color = color
        self.damage = 5
        self.reach = 25
        self.cooldown = 10

class BossGunData(GunData):
    def __init__(self, color):
        self.bullet_speed = 15
        self.bullet_color = color
        self.damage = 10
        self.reach = 20
        self.cooldown = 20
