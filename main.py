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

    def update(self, keys):
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
        if keys[pg.K_SPACE]:
            return self.shoot()
        return False

    def draw(self, screen):
        pg.draw.rect(screen, (125,125,125), pg.Rect(self.x - 20, self.y - 20, 40, 40))

    def shoot(self):
        return Bullet(self.x, self.y, self.angle, 0.2)



WINDOW_SIZE = (800, 600)

def run_game():
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Game")
    tank = Tank(200, 200, 30, 0.1)
    bullet = Bullet(0, 0, speed=0.15, angle=0)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        keys = pg.key.get_pressed()
        updated = tank.update(keys)
        if updated != False:
            bullet = updated
        screen.fill((0,0,0))
        bullet.update()
        bullet.draw(screen)
        tank.draw(screen)
        pg.display.update()

if __name__ == "__main__":
    run_game()