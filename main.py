from time import sleep
import random
import pygame as pg


class Circle:
    def __init__(self, color, position, radius):
        self.position = position
        self.color = color
        self.radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = max(value, 0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def __gt__(self, other):
        return self.radius > other.radius

    def __ge__(self, other):
        return self.radius >= other.radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __le__(self, other):
        return self.radius <= other.radius

    def __add__(self, other):
        if self >= other :
            return Circle(self.color, self.position, self.radius + other.radius)
        else:
            return Circle(other.color, other.position, self.radius + other.radius)
    def __sub__(self, other):
        if self < other:
            return Exception("First circle is less then seccond")
        return Circle(self.color, self.position, self.radius - other.radius)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.position, self.radius)

class Rectangle:
    def __init__(self, color, position, rect):
        self.position = position
        self.color = color
        self.rect = rect

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = (max(value[0], 0), max(value[1], 0))

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def __gt__(self, other):
        return self.rect[0] * self.rect[1] > other.rect[0] * other.rect[1]

    def __ge__(self, other):
        return self.rect[0] * self.rect[1] >= other.rect[0] * other.rect[1]

    def __lt__(self, other):
        return self.rect[0] * self.rect[1] < other.rect[0] * other.rect[1]

    def __le__(self, other):
        return self.rect[0] * self.rect[1] <= other.rect[0] * other.rect[1]

    def __add__(self, other):
        if self >= other :
            return Rectangle(self.color, self.position, (self.rect[0] + other.rect[0], self.rect[1] + other.rect[1]))
        else:
            return Rectangle(other.color, other.position, (self.rect[0] + other.rect[0], self.rect[1] + other.rect[1]))
    def __sub__(self, other):
        if self < other:
            return Exception("First rectangle is less then seccond")
        return Rectangle(self.color, self.position, (max(self.rect[0] - other.rect[0], 0), max(self.rect[1] - other.rect[1], 0)))

    def draw(self, screen):
        pg.draw.rect(screen, self.color, pg.Rect(
            self.position[0], self.position[1], self.rect[0], self.rect[1]
        ))

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
        if self.is_alive:
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

class Berserk(Character):
    def __init__(self, name, damage, evasion=0, armor=0, lifesteal=0., hp=100.):
        Character.__init__(self, name, damage, evasion, armor, lifesteal, hp)
        self._max_hp = self.hp

    def attack(self, other):
        if self.is_alive:
            damage_modify = self.damage + self.damage * (random.randint(-20, 20) / 100) + self.damage * (self._max_hp - self.hp) / self._max_hp
            responce = other.take_damage(damage_modify)
            if responce != -1:
                self.hp += (responce / 100) * self.lifesteal
                return responce
            else:
                return -1
        else:
            return -2



player = Character("Unit 1", 13, 10, 10, 40)
player2 = Berserk("Unit 2", 13,  0,7, 0)

while player.is_alive and player2.is_alive:
    print(player.__repr__())
    print(player2.__repr__())

    attack = player.attack(player2)

    if attack == -1:
        print(f"{player2.name} evaded from attack {player.name}")
    elif attack == -2:
        print(player2)
    else:
        print(f"{player.name} attacks {player2.name} with {round(attack, 3)} damage")
        print(player2)
        # sleep(1)

    attack = player2.attack(player)
    if attack == -1:
        print(f"{player.name} evaded from attack {player2.name} ")
    elif attack == -2:
        print(player)
    else:
        print(f"{player2.name} attacks {player.name} with {round(attack, 3)} damage")
        print(player)
        # sleep(1)

    print("\n")
    #sleep(1)
    if not player.is_alive:
        print(f"{player2.name} - WIN!")
    if not player2.is_alive:
        print(f"{player.name} - WIN!")