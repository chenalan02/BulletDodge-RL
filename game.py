import pygame
import os
from shooter import Shooter, HardCodedAI, Player
from bullet import Bullet
from constants import *

class Map():
    def __init__ (self, backgroundFileName, FPS):
        self.background = pygame.image.load(os.path.join(("game_assets"), backgroundFileName))
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
    
    def update(self):
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

            #quits game if x clicked on top right of screen
            if event.type == pygame.QUIT:
                gameDone = True
                return gameDone
        
        self.player.update(self.bullets)

        for enemy in self.enemies:
            enemy.update(self.bullets)

        for bullet in self.bullets:
            bullet.move()
            if not bullet.in_range():
                self.bullets.remove(bullet)

        playerDead = self.player.check_death(self.bullets)
        if playerDead:
            self.restart()

        self.score += 1
        self.draw()
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def restart(self):
        self.player.reinitialize()
        for enemy in self.enemies:
            enemy.reinitialize()
        self.score = 0
        self.bullets.empty()

    def draw(self):
        self.background.fill((0,0,0))
        self.background.blit(self.background, (0,0))
        self.dodger.draw(self.background)
        self.enemies.draw(self.background)
        self.bullets.draw(self.background)
        resized_screen = pygame.transform.scale(self.background, (800, 600)) 
        self.screen.blit(resized_screen, (0,0))
        self.display_score()

    def display_score(self):
        font= pygame.font.SysFont('Calibri', 50, True, False)
        text= font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(text, [0,0])

    def addAI(self, coordinates: tuple, speed, cooldown, movementFactor):
        self.enemies.add(HardCodedAI(coordinates, speed, cooldown, movementFactor, self.player))
