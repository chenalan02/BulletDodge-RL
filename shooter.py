import pygame
import os
from bullet import Bullet
from math import atan, pi, radians
from random import randint
from constants import *

class Shooter(pygame.sprite.Sprite):
    def __init__(self, spawnPos, speed, fileName):
        super().__init__()

        self.image = pygame.image.load(os.path.join(("game_assets"), fileName))
        self.image = pygame.transform.scale(self.image, SHOOTER_SIZE)
        
        self.spawnPos = spawnPos

        self.rect = self.image.get_rect()

        self.rect.x = spawnPos[0]
        self.rect.y = spawnPos[1]

        self.x = spawnPos[0]
        self.y = spawnPos[1]

        self.velocityX = 0
        self.velocityY = 0

        self.speed = speed

    def reinitialize(self):
        self.x = self.spawnPos[0]
        self.y = self.spawnPos[1]

    def moveLeft(self):
        self.velocityX = -self.speed

    def moveRight(self):
        self.velocityX = self.speed

    def moveUp(self):
        self.velocityY = -self.speed

    def moveDown(self):
        self.velocityY = self.speed

    def stopLeft(self):
        if self.velocityX < 0:
            self.velocityX = 0

    def stopRight(self):
        if self.velocityX > 0:
            self.velocityX = 0

    def stopUp(self):
        if self.velocityY < 0:
            self.velocityY = 0

    def stopDown(self):
        if self.velocityY > 0:
            self.velocityY = 0
        
    def stop(self):
        self.velocityX = 0
        self.velocityY = 0

    def update(self, bulletList):
        self.x += self.velocityX
        self.y += self.velocityY

        if self.x < 0 :
            self.x = 0
        elif self.x > SCREEN_SIZE[0] - self.rect.width:
            self.x = SCREEN_SIZE[0] - self.rect.width

        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_SIZE[1] - self.rect.height:
            self.y = SCREEN_SIZE[1] - self.rect.height

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def check_death(self, bullets):
        if pygame.sprite.spritecollide(self, bullets, False) != []:
            return True
        else:
            return False

class Player(Shooter):
    def __init__(self, spawnPos, speed):
        super().__init__(spawnPos, speed, "circle.png")
    
class HardCodedAI(Shooter):
    def __init__(self, spawnPos, speed, cooldown, movementFactor, target):
        super().__init__(spawnPos, speed, "triangle.png")
        self.enemies= pygame.sprite.Group()
        self.COOLDOWN = cooldown
        self.timer = cooldown
        self.movementFactor = movementFactor
        self.target = target

    def fire_gun(self, bulletList):
        enemyPos = self.target.rect.topleft

        deltaX = enemyPos[0] - self.x
        if deltaX == 0:
            deltaX = 1
        deltaY = self.y - enemyPos[1]
        angle = atan(deltaY/deltaX)

        if deltaX < 0:
            angle += pi

        randomness = radians(randint(-5, 5))
        angle += randomness
            
        bulletList.add(Bullet( (self.x + SHOOTER_SIZE[0]/2, self.y + SHOOTER_SIZE[0]/2), angle))

    def update(self, bulletList):
        
        if self.timer < 1:
            self.fire_gun(bulletList)
            self.timer = self.COOLDOWN
        else:
            self.timer -= 1

        moveX = randint(0, self.movementFactor)
        moveY = randint(0, self.movementFactor)
        if moveX == 0:
            self.velocityX = self.speed*randint(-1, 1)
        if moveY == 0:
            self.velocityY = self.speed*randint(-1, 1)

        self.x += self.velocityX
        self.y += self.velocityY

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.x < 0 :
            self.x = 0
        elif self.x > SCREEN_SIZE[0] -  self.rect.width:
            self.x = SCREEN_SIZE[0] -  self.rect.width

        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_SIZE[1] - self.rect.height:
            self.y = SCREEN_SIZE[1] - self.rect.height

        


    
    
