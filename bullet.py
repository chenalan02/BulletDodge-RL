import pygame
import os
from math import sin, cos, degrees
from constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, coordinates, angle):
        super().__init__()

        self.image= pygame.image.load(os.path.join('game_assets','Bullet.png'))
        self.image= pygame.transform.scale(self.image,BULLET_SIZE)
        self.image= pygame.transform.rotate(self.image, degrees(angle)+270)
        self.rect= self.image.get_rect()

        self.speed= BULLET_SPEED
        self.rect.x= coordinates[0] + SHOOTER_SIZE[0]/2
        self.rect.y= coordinates[1] + SHOOTER_SIZE[1]/2
        self.x= coordinates[0]
        self.y= coordinates[1]
        self.angle= angle

    def move(self):
        self.x+= self.speed*cos(self.angle)
        self.y-= self.speed*sin(self.angle)

        self.rect.x= int(self.x)
        self.rect.y= int(self.y)

    def in_range(self):
        if self.rect.x < 0 or self.rect.x > SCREEN_SIZE[0] + 50:
            return False
        if self.rect.y < 0 or self.rect.y > SCREEN_SIZE[1] + 50:
            return False
        else:
            return True
        