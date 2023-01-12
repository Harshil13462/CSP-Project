import sys
import pygame
import random
import math
import time
from pygame.locals import *

WIDTH = 1080
HEIGHT = 840


INVADER_HEIGHT = 25
INVADER_LENGTH = 75

INVADER_GAP = 25


BULLET_LENGTH = 5
BULLET_HEIGHT = 5
DEFENDER_HEIGHT = 25
DEFENDER_LENGTH = 75

LEFT = -0.3
RIGHT = 0.3

variables = [RIGHT]
bullets = []
invaders = []

def createBullet(x, y, screen, team):
    if team == 1:
        target = invaders
    if team == 2:
        target = player
    bullets.append(Bullet(x, y, screen, target))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, target):
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.screen = screen
        self.target = target
        self.speed = 2
        self.surf = pygame.Surface((BULLET_LENGTH, BULLET_HEIGHT))
        self.surf.fill((255, 0, 0))
        if self.target == 1:
            self.speed = -2
    
    def update(self):
        self.y += self.speed
        if self.y < 0 or self.y > HEIGHT:
            del self
        if type(self.target) == list:
            pass
        else:
            if self.x > self.target.x - BULLET_LENGTH and self.x < self.target.x + DEFENDER_LENGTH + BULLET_LENGTH and self.y > self.target.y - BULLET_HEIGHT and self.y < self.target.y + BULLET_HEIGHT:
                self.target.lives -= 1
                del self
        self.screen.blit(self.surf, (self.x, self.y))

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, lives):
        super(Character, self).__init__()
        self.x = x
        self.y = y
        self.screen = screen
        self.lives = lives

class Invader(Character):
    def __init__(self, x, y, screen, variables):
        super().__init__(x, y, screen, 1)
        self.team = 2
        self.surf = pygame.Surface((INVADER_LENGTH, INVADER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.variables = variables
        self.prev = 1
    
    def update(self):
        if self.prev != variables[0]:
            self.y = self.y + INVADER_HEIGHT + INVADER_GAP
        self.x = self.x + variables[0]
        if self.x <= 0 or self.x >= WIDTH - INVADER_LENGTH:
            variables[0] *= -1
            self.y = self.y + INVADER_HEIGHT + INVADER_GAP
        self.prev = variables[0]
        self.screen.blit(self.surf, (self.x, self.y))

        if random.randint(1, 10000) == 1:
            createBullet(self.x, self.y, self.screen, self.team)
    
    def shoot(self):
        pass

class Defender(Character):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, 3)
        self.team = 1
        self.surf = pygame.Surface((DEFENDER_LENGTH, DEFENDER_HEIGHT))
        self.surf.fill((255, 255, 255))
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.x = self.x - 5
            if self.x < 0:
                self.x = 0
        if pressed_keys[K_RIGHT]:
            self.x = self.x + 5
            if self.x > WIDTH - DEFENDER_LENGTH:
                self.x = WIDTH - DEFENDER_LENGTH
        self.screen.blit(self.surf, (self.x, self.y))

class Shield(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Shield, self).__init__()

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
player = Defender(30, 800, screen)
for i in range(10):
    for j in range(6):
        invaders.append(Invader(30 + i * (INVADER_GAP + INVADER_LENGTH), 0 + j * (INVADER_GAP + INVADER_HEIGHT), screen, variables))
while running:
    screen.fill((0, 0, 0))
    pressed_keys = pygame.key.get_pressed()
    for i in invaders:
        i.update()
    for i in bullets:
        i.update()
    player.update(pressed_keys)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    fpsClock.tick(fps)

pygame.quit()
sys.exit()
screen = pygame.display.set_mode([500, 500])
running = True

pygame.quit()