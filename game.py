import pygame
import os
from shooter import Shooter, HardCodedAI, Player
from bullet import Bullet

SCREEN_SIZE = (1280, 720)

class Map():
    def __init__ (self, backgroundFileName, userPlaying: bool):
        self.background = pygame.image.load(os.path.join(("game_assets"), backgroundFileName))
        self.background = pygame.transform.scale(self.background, SCREEN_SIZE)

        self.screenSize = SCREEN_SIZE
        self.shooters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.userPlaying = userPlaying
        if self.userPlaying:
            self.player = Player((SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
            self.shooters.add(self.player)
        
        pygame.init()
        pygame.display.set_caption('TopDownShooter')
        self.screen = pygame.display.set_mode(self.screenSize)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(1)
    
    def all_find_enemies(self):
        for shooter in self.shooters:
            if type(shooter) is not Player:
                shooter.find_enemies(self.shooters)


    def update(self):
        for event in pygame.event.get():

            if self.userPlaying:

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
                        
                if event.type==pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    self.player.fire_gun(self.bullets, mousePos)

                #quits game if x clicked on top right of screen
                if event.type == pygame.QUIT:
                    gameDone = True
                    return gameDone
        
        for shooter in self.shooters:
            shooter.update(self.bullets)
        for bullet in self.bullets:
            bullet.move()
            if not bullet.in_range():
                self.bullets.remove(bullet)
        
        self.draw()
        pygame.display.flip()
            
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.shooters.draw(self.screen)
        self.bullets.draw(self.screen)

    def addAI(self, coordinates: tuple, cooldown, movementFactor):
        self.shooters.add(HardCodedAI(coordinates, cooldown, movementFactor))
