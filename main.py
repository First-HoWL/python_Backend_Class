import math
from time import sleep
import random
import pygame as pg

class Bullet:
    def __init__(self, x=0, y=0, angle=0, speed=0.1):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        rad = math.radians(self.angle)

        self.vx = math.sin(rad) * self.speed
        self.vy = -math.cos(rad) * self.speed

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pg.draw.circle(screen, (255,255,255), (self.x, self.y), 5)

class Tank:
    def __init__(self, x=0, y=0, angle=0, speed=0.1):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        rad = math.radians(self.angle)
        self.vx = math.sin(rad) * self.speed
        self.vy = -math.cos(rad) * self.speed
        self.cooldown = 5


    def update(self, keys, game_object):
        if keys[pg.K_w]:
            self.x += self.vx
            self.y += self.vy
        if keys[pg.K_s]:
            self.x -= self.vx
            self.y -= self.vy
        if keys[pg.K_a]:
            self.angle -= 0.1
            rad = math.radians(self.angle)
            self.vx = math.sin(rad) * self.speed
            self.vy = -math.cos(rad) * self.speed
        if keys[pg.K_d]:
            self.angle += 0.1
            rad = math.radians(self.angle)
            self.vx = math.sin(rad) * self.speed
            self.vy = -math.cos(rad) * self.speed
        if keys[pg.K_SPACE] and self.cooldown == 0:
            game_object.append(self.shoot())
            self.cooldown = 5
        self.cooldown = max(0, self.cooldown - 0.07)

    def draw(self, screen):
        pg.draw.rect(screen, (0,128,0), pg.Rect(self.x - 20, self.y - 20, 40, 40))
        pg.draw.line(screen, (53, 94, 59), (self.x, self.y), (self.x + self.vx * 500, self.y + self.vy * 500), 12)

    def shoot(self):
        return Bullet(self.x + self.vx * 500, self.y + self.vy * 500, self.angle, 0.25)

class Frog_Tank(Tank):
    def __init__(self, x=0, y=0, angle=0, speed=0.1):
        Tank.__init__(self, x, y, angle, speed)
        self.jump_Cooldown = 0

    def update(self, keys, game_object):
        Tank.update(self, keys, game_object)
        if keys[pg.K_x] and self.jump_Cooldown == 0:
            self.x += self.vx * 500
            self.y += self.vy * 500
            self.jump_Cooldown = 5
        self.jump_Cooldown = max(0, self.jump_Cooldown - 0.005)



WINDOW_SIZE = (800, 600)

def run_game():
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Game")
    tank = Frog_Tank(200, 200, 30, 0.1)

    game_object = []

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        keys = pg.key.get_pressed()
        tank.update(keys, game_object)

        screen.fill((0,0,0))
        for obj in game_object:
            obj.update()
            obj.draw(screen)
            if obj.x < 0 or obj.x > WINDOW_SIZE[0] or obj.y < 0 or obj.y > WINDOW_SIZE[1]:
                game_object.remove(obj)
        tank.draw(screen)
        pg.display.update()

if __name__ == "__main__":
    run_game()