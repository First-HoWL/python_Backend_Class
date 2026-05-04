from time import sleep
import random

class Character:
    def __init__(self, name, damage, evasion=0, armor=0, lifesteal=0., hp=100.):
        self.name = name
        self._hp = hp
        self.armor = armor
        self.damage = damage
        self.evasion = evasion
        self.lifesteal = lifesteal

    def __str__(self):
        return f"{self.name} - {self._hp} HP"

    def __repr__(self):
        return f"{self.name=} \t | {self._hp=} \t | {self.damage=} \t | {self.evasion=} \t | {self.armor=} \t | {self.lifesteal=}"

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value < 0:
            self._hp = 0
        else:
            self._hp = round(value, 3)


    def take_damage(self, damage):
        if random.randint( 1, 100) < self.evasion:
            return -1
        else:
            new_damage = damage - min((damage * (self.armor / 100)), damage)
            self.hp -= new_damage
            return new_damage



    def attack(self, other):
        if self.hp > 0:
            damage_modify = self.damage + self.damage * (random.randint(-20, 20) / 100)
            responce = other.take_damage(damage_modify)
            if responce != -1:
                self.hp += (responce / 100) * self.lifesteal
                return responce
            else:
                return -1
        else:
            return -2

    @property
    def is_alive(self):
        return self.hp > 0

player = Character("Unit 1", 13, 95)
player2 = Character("Unit 2", 13,  0,7, 50)

while player.is_alive and player2.is_alive:
    print(player.__repr__())
    print(player2.__repr__())

    attack = player.attack(player2)

    if attack == -1:
        print(f"{player2.name} evaded from attack {player.name}")
    elif attack == -2:
        print(player2)
    else:
        print(f"{player.name} attacks {player2.name}")
        print(player2)
        # sleep(1)

    attack = player2.attack(player)
    if attack == -1:
        print(f"{player.name} evaded from attack {player2.name}")
    elif attack == -2:
        print(player)
    else:
        print(f"{player2.name} attacks {player.name}")
        print(player)
        # sleep(1)

    print("\n")
    #sleep(1)
    if not player.is_alive:
        print(f"{player2.name} - WIN!")
    if not player2.is_alive:
        print(f"{player.name} - WIN!")