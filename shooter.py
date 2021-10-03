import pygame
import os
from bullet import Bullet
from math import atan, degrees, pi, dist
from random import randint

SCREEN_SIZE = (1280, 720)
SHOOTER_SIZE = (50, 50)

class Shooter(pygame.sprite.Sprite):
    def __init__(self, spawnPos):
        super().__init__()

        self.image = pygame.image.load(os.path.join(("game_assets"), "circle.png"))
        self.image = pygame.transform.scale(self.image, SHOOTER_SIZE)
        
        self.rect = self.image.get_rect()
        self.rect.x = spawnPos[0]
        self.rect.y = spawnPos[1]

        self.velocityX = 0
        self.velocityY = 0

    def moveLeft(self):
        self.velocityX = -1

    def moveRight(self):
        self.velocityX = 1

    def moveUp(self):
        self.velocityY = -1

    def moveDown(self):
        self.velocityY = 1

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
        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        if self.rect.x < 0 :
            self.rect.x = 0
        elif self.rect.x > SCREEN_SIZE[0] -  self.rect.width:
            self.rect.x = SCREEN_SIZE[0] -  self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_SIZE[1] - self.rect.height:
            self.rect.y = SCREEN_SIZE[1] - self.rect.height

class Player(Shooter):
    def __init__(self, spawnPos):
        super().__init__(spawnPos)
        

    def fire_gun(self, bulletList, mousePos:tuple):
        deltaX = mousePos[0] - self.rect.x
        deltaY = self.rect.y - mousePos[1]
        angle = atan(deltaY/deltaX)

        if deltaX < 0:
            angle += pi
            
        bulletList.add(Bullet( (self.rect.x, self.rect.y), angle))
    

class HardCodedAI(Shooter):
    def __init__(self, spawnPos, cooldown, movementFactor):
        super().__init__(spawnPos)
        self.enemies= pygame.sprite.Group()
        self.COOLDOWN = cooldown
        self.timer = cooldown
        self.movementFactor = movementFactor

    def find_enemies(self, shooters):
        for shooter in shooters:
            if shooter is not self:
                self.enemies.add(shooter)

    def closest_enemy_pos(self):
        closestEnemyDist = 10000
        closestEnemy = None

        for shooter in self.enemies:
            distance = dist((self.rect.x, self.rect.y), (shooter.rect.x, shooter.rect.y))
            if distance < closestEnemyDist:
                closestEnemy = shooter
                closestEnemyDist = distance

        return (closestEnemy.rect.x, closestEnemy.rect.y)

    def fire_gun(self, bulletList):
        enemyPos = self.closest_enemy_pos()

        deltaX = enemyPos[0] - self.rect.x
        if deltaX == 0:
            deltaX = 1
        deltaY = self.rect.y - enemyPos[1]
        angle = atan(deltaY/deltaX)

        if deltaX < 0:
            angle += pi
            
        bulletList.add(Bullet( (self.rect.x + SHOOTER_SIZE[0]/2, self.rect.y + SHOOTER_SIZE[0]/2), angle))

    def update(self, bulletList):
        
        if self.timer < 1:
            self.fire_gun(bulletList)
            self.timer = self.COOLDOWN
        else:
            self.timer -= 1

        moveX = randint(0, self.movementFactor)
        moveY = randint(0, self.movementFactor)
        if moveX == 0:
            self.velocityX = randint(-1, 1)
        if moveY == 0:
            self.velocityY = randint(-1, 1)

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        if self.rect.x < 0 :
            self.rect.x = 0
        elif self.rect.x > SCREEN_SIZE[0] -  self.rect.width:
            self.rect.x = SCREEN_SIZE[0] -  self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_SIZE[1] - self.rect.height:
            self.rect.y = SCREEN_SIZE[1] - self.rect.height

        


    
    
