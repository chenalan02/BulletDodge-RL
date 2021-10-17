import pygame
import os
import sys

from shooter import Shooter, HardCodedAI, Player
from bullet import Bullet
from constants import *
import numpy as np
import cv2


class Map():
    def __init__ (self, FPS):
        self.background = pygame.image.load(os.path.join(("game_assets"), "black.jpg"))
        self.background = pygame.transform.scale(self.background, SCREEN_SIZE)

        self.screenSize = SCREEN_SIZE
        self.dodger = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.FPS = FPS
        self.score = 0

        self.player = Player((SCREEN_SIZE[0]-5, SCREEN_SIZE[1]-5), 0.5)
        self.dodger.add(self.player)
    
        pygame.init()
        pygame.display.set_caption('TopDownShooter')
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(1)
    
    def move(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYUP:
                #stops movement in left direction when the left key is released
                if event.key==pygame.K_a:
                    self.player.stopLeft()
                #stops movement in right direction when the right key is released
                if event.key==pygame.K_d:
                    self.player.stopRight()
                if event.key==pygame.K_w:
                    self.player.stopUp()
                if event.key==pygame.K_s:
                    self.player.stopDown()
            
            #when a key is pressed down
            if event.type == pygame.KEYDOWN:
                #player movement in x axis using left and right arrow keys
                if event.key==pygame.K_a:
                    self.player.moveLeft()
                if event.key==pygame.K_d:
                    self.player.moveRight()
                if event.key==pygame.K_w:
                    self.player.moveUp()
                if event.key==pygame.K_s:
                    self.player.moveDown()
            
            pygame.event.wait()

            #quits game if x clicked on top right of screen
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, action=0):
        
        if action == 1:
            self.player.moveLeft()
        elif action == 2:
            self.player.moveRight()
        elif action == 3:
            self.player.moveUp()
        elif action == 4:
            self.player.moveDown()
        elif action == 5:
            self.player.stop()
        
        self.player.update(self.bullets)

        for enemy in self.enemies:
            enemy.update(self.bullets)

        reward = 0

        for bullet in self.bullets:
            bullet.move()
            if not bullet.in_range():
                self.bullets.remove(bullet)
                self.score += 1
                reward = 1

        self.draw()
        pygame.display.flip()
        self.clock.tick(self.FPS)

        nextFrame = pygame.surfarray.pixels3d(self.background)
        nextFrame = cv2.cvtColor(nextFrame, cv2.COLOR_BGR2GRAY)
        nextFrame = np.array(nextFrame, dtype="float")
        nextFrame = nextFrame.swapaxes(0,1)
        nextFrame /= 255

        playerDead = self.player.check_death(self.bullets)
        if playerDead:
            self.restart()
            done = True
            reward = -5
        else:
            done = False
        
        return nextFrame, reward, done

    def restart(self):
        self.player.reinitialize()
        for enemy in self.enemies:
            enemy.reinitialize()
        self.score = 0
        self.bullets.empty()
        self.draw()

        nextFrame = pygame.surfarray.pixels3d(self.background)
        nextFrame = cv2.cvtColor(nextFrame, cv2.COLOR_BGR2GRAY)
        nextFrame = np.array(nextFrame, dtype="float")
        nextFrame = nextFrame.swapaxes(0,1)
        nextFrame /= 255
        return nextFrame

    def draw(self):
        self.background.fill((0,0,0))
        self.background.blit(self.background, (0,0))
        self.dodger.draw(self.background)
        self.enemies.draw(self.background)
        self.bullets.draw(self.background)
        resized_screen = pygame.transform.scale(self.background, DISPLAY_SIZE) 
        self.screen.blit(resized_screen, (0,0))
        self.display_score()

    def display_score(self):
        font= pygame.font.SysFont('Calibri', 50, True, False)
        text= font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(text, [0,0])

    def addHardcodedAI(self, coordinates: tuple, speed, cooldown, movementFactor):
        self.enemies.add(HardCodedAI(coordinates, speed, cooldown, movementFactor, self.player))

class RLEnv(Map):
    def __init__ (self, FPS):
        super().__init__(FPS)
        self.addHardcodedAI( (0,0), speed=0.5, cooldown= 50, movementFactor=25)
